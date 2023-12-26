from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, TypeVar
import abc
import sys
import hashlib
import statistics
import enum
import dataclasses
import functools
import itertools
import numbers
import pprint
import random
import re
import string
import functools
import dataclasses

import ray.rllib.env.multi_agent_env
from ray.rllib.algorithms.ppo import PPO # pytype: disable=import-error
import gymnasium
import gymnasium.spaces
from frozendict import frozendict
import numpy as np
from scipy import stats
import more_itertools

from chicken_coop.coop_config import CoopConfig
from .zeitgeisting import Zeitgeist, Dialog
from chicken_coop import county
from chicken_coop.county import misc
from chicken_coop.county.typing import Agent, RealNumber
from chicken_coop.county.constants import ALL_AGENTS


class Move(enum.Enum):
    DOVE = 'dove'
    HAWK = 'hawk'

    @staticmethod
    def from_neural(neural: int) -> Move:
        if neural == 0:
            return Move.DOVE
        else:
            assert neural == 1
            return Move.HAWK

    def to_neural(self) -> int:
        if self == Move.DOVE:
            return 0
        else:
            assert self == Move.HAWK
            return 1

    @staticmethod
    def get_random() -> Move:
        return random.choice((Move.HAWK, Move.DOVE))

    @property
    def as_letter(self) -> str:
        return self.value[0]



@dataclasses.dataclass(frozen=True, kw_only=True)
class State(county.BaseState):

    coop_config: CoopConfig
    i_turn: int
    joint_moves: tuple[tuple[Move, Move], ...]
    joint_rewards: tuple[tuple[RealNumber, RealNumber], ...]
    i_agent_pairs: tuple[tuple[int, int], ...]
    episode_seed: int


    def __post_init__(self) -> None:
        assert set(itertools.chain.from_iterable(self.i_agent_pairs)) == set(self.i_agents)
        assert all(map(more_itertools.is_sorted, self.i_agent_pairs))

    @property
    def n_agents(self) -> int:
        return self.coop_config.n_agents

    @property
    def i_agents(self) -> tuple[int, ...]:
        return self.coop_config.i_agents


    @functools.cached_property
    def agents(self) -> tuple[Agent, ...]:
        return tuple(self.coop_config.policy_by_agent)



    @functools.cached_property
    def observation_by_agent(self) -> dict[Agent, dict]:
        observation_by_agent = {}
        for i_agent, agent in enumerate(self.agents):
            i_observed_opponent = self.i_observed_opponent_by_i_agent[i_agent]
            observation_by_agent[agent] = {
                'i_opponent': (
                    np.array(
                        [i_observed_opponent,
                         self.coop_config.n_agents - 1 - i_observed_opponent],
                        dtype=int
                    ) if self.coop_config.identity_is_linear else
                    misc.make_one_hot(i_observed_opponent, self.coop_config.n_agents)
                )
            }

            if self.coop_config.episode_length >= 2:
                observation_by_agent[agent] |= {
                    'i_turn': np.array([self.i_turn], dtype=int),
                    'n_victory_rewards': np.array(
                        [self.rewards_by_i_agent[i_agent].count(self.coop_config.victory_reward)],
                        dtype=int,
                    ),
                    'n_boredom_rewards': np.array(
                        [self.rewards_by_i_agent[i_agent].count(self.coop_config.boredom_reward)],
                        dtype=int,
                    ),
                    'n_defeat_rewards': np.array(
                        [self.rewards_by_i_agent[i_agent].count(self.coop_config.defeat_reward)],
                        dtype=int,
                    ),
                    'n_anguish_rewards': np.array(
                        [self.rewards_by_i_agent[i_agent].count(self.coop_config.anguish_reward)],
                        dtype=int,
                    ),
                }

        return observation_by_agent

    @functools.cached_property
    def i_opponent_by_i_agent(self) -> dict[int, int]:
        opponent_by_agent = {}
        for (agent_0, agent_1) in self.i_agent_pairs:
            opponent_by_agent[agent_0] = agent_1
            opponent_by_agent[agent_1] = agent_0
        return opponent_by_agent

    @functools.cached_property
    def i_observed_opponent_by_i_agent(self) -> dict[int, int]:
        if self.coop_config.observation_accuracy == 1:
            return self.i_opponent_by_i_agent
        else:
            whether_resolution = 100
            randomishes_whether = misc.int_to_base(
                int(hashlib.sha1(f'{self.episode_seed}?'.encode()).hexdigest(), 16),
                whether_resolution,
            )
            assert max(randomishes_whether) <= whether_resolution - 1
            assert len(randomishes_whether) >= self.coop_config.n_agents + 1
            randomishes_which = misc.int_to_base(
                int(hashlib.sha1(f'{self.episode_seed}#'.encode()).hexdigest(), 16),
                self.coop_config.n_agents - 1,
            )
            assert max(randomishes_which) <= self.coop_config.n_agents - 2
            assert len(randomishes_which) >= self.coop_config.n_agents + 1
            i_observed_opponent_by_i_agent = self.i_opponent_by_i_agent.copy()
            for i_agent in self.i_agents:
                whether = randomishes_whether[i_agent] / whether_resolution
                if whether >= self.coop_config.observation_accuracy:
                    i_observed_opponent_by_i_agent[i_agent] = i_observed_opponent = \
                                          (i_agent + randomishes_which[i_agent] + 1) % self.n_agents
                    assert i_observed_opponent != i_agent
                    assert i_observed_opponent in self.i_agents

            return i_observed_opponent_by_i_agent

    @functools.cached_property
    def moves_by_i_agent(self) -> tuple[tuple[Move, ...], tuple[Move, ...]]:
        if self.i_turn == 0:
            return ((),) * len(self.agents)
        return tuple(zip(*self.joint_moves, strict=True))

    @functools.cached_property
    def rewards_by_i_agent(self) -> tuple[tuple[RealNumber, ...], tuple[RealNumber, ...]]:
        if self.i_turn == 0:
            return ((),) * len(self.agents)
        return tuple(zip(*self.joint_rewards, strict=True))

    @functools.cached_property
    def reward_by_agent(self) -> dict[Agent, RealNumber]:
        return dict(zip(self.agents, self.joint_rewards[-1], strict=True))

    @functools.cached_property
    def terminated_by_agent(self) -> dict[Agent, bool]:
        return {agent: False for agent in self.agents + (ALL_AGENTS,)}

    @functools.cached_property
    def truncated_by_agent(self) -> dict[Agent, bool]:
        return {agent: (self.i_turn >= self.coop_config.episode_length)
                for agent in self.agents + (ALL_AGENTS,)}

    @staticmethod
    def make_initial(coop_config: CoopConfig) -> State:
        return State(
            coop_config=coop_config,
            i_turn=0,
            joint_moves=(),
            joint_rewards=(),
            i_agent_pairs=tuple(
                map(tuple,
                    map(sorted,
                        more_itertools.chunked(misc.shuffled(range(coop_config.n_agents)), 2)
                    )
                )
            ),
            episode_seed=random.randint(0, sys.maxsize),
        )

    def step(self, actions: Mapping[Agent, np.ndarray]) -> State:

        i_turn = self.i_turn + 1

        joint_move = tuple(Move.from_neural(actions[agent]) for agent in self.agents)
        joint_reward = [None] * len(self.agents)

        for i_left_agent, i_right_agent in self.i_agent_pairs:
            match (joint_move[i_left_agent], joint_move[i_right_agent]):
                case (Move.HAWK, Move.HAWK):
                    joint_reward[i_left_agent] = self.coop_config.anguish_reward
                    joint_reward[i_right_agent] = self.coop_config.anguish_reward
                case (Move.HAWK, Move.DOVE):
                    joint_reward[i_left_agent] = self.coop_config.victory_reward
                    joint_reward[i_right_agent] = self.coop_config.defeat_reward
                case (Move.DOVE, Move.HAWK):
                    joint_reward[i_left_agent] = self.coop_config.defeat_reward
                    joint_reward[i_right_agent] = self.coop_config.victory_reward
                case (Move.DOVE, Move.DOVE):
                    joint_reward[i_left_agent] = self.coop_config.boredom_reward
                    joint_reward[i_right_agent] = self.coop_config.boredom_reward
                case _:
                    raise RuntimeError

        assert None not in joint_reward

        return State(
            coop_config=self.coop_config,
            i_turn=i_turn,
            joint_moves=self.joint_moves + (joint_move,),
            joint_rewards=self.joint_rewards + (tuple(joint_reward),),
            i_agent_pairs=self.i_agent_pairs,
            episode_seed=self.episode_seed,
        )


    @functools.cached_property
    def text(self) -> str:
        if self.i_turn == 0:
            return ','.join(f'{self.coop_config.pad_i_agent(i_left_agent)} '
                            f'{self.coop_config.pad_i_agent(i_right_agent)}'
                            for i_left_agent, i_right_agent in self.i_agent_pairs
            )
        else:
            return ','.join(
                (self.joint_moves[-1][i_left_agent].as_letter +
                 self.joint_moves[-1][i_right_agent].as_letter)
                for i_left_agent, i_right_agent in self.i_agent_pairs
            )
        # if self.i_turn == 0:
            # return '--'
        # else:
            # return f'{self.joint_moves[-1][0].as_letter}{self.joint_moves[-1][1].as_letter}'


    @functools.cached_property
    def zeitgeist(self) -> Zeitgeist:
        if self.i_turn == 0:
            return dict(zip(itertools.combinations(self.i_agents, 2),
                            itertools.repeat(Dialog.make_zero(self.coop_config))))
        dialog_by_i_agent_pair = {}
        for i_agent_a, i_agent_b in self.coop_config.i_agent_pairs_increasing:
            if (i_agent_a, i_agent_b) in self.i_agent_pairs:
                agent_a_rewards = self.rewards_by_i_agent[i_agent_a]
                agent_b_rewards = self.rewards_by_i_agent[i_agent_b]
                dialog_by_i_agent_pair[i_agent_a, i_agent_b] = Dialog(
                    n_agent_a_victories=agent_a_rewards.count(self.coop_config.victory_reward),
                    n_agent_b_victories=agent_b_rewards.count(self.coop_config.victory_reward),
                    n_anguishes=agent_a_rewards.count(self.coop_config.anguish_reward),
                    n_boredoms=agent_a_rewards.count(self.coop_config.boredom_reward),
                    coop_config=self.coop_config,
                )
            else:
                dialog_by_i_agent_pair[i_agent_a, i_agent_b] = Dialog.make_zero(self.coop_config)
        for i_agent_a, i_agent_b in self.coop_config.i_agent_pairs_decreasing:
            dialog_by_i_agent_pair[i_agent_a, i_agent_b] = -dialog_by_i_agent_pair[i_agent_b,
                                                                                   i_agent_a]
        for i_agent_a, i_agent_b in self.coop_config.i_agent_pairs_diagonal:
            assert i_agent_a == i_agent_b
            dialog_by_i_agent_pair[i_agent_a, i_agent_b] = Dialog.make_zero(self.coop_config)


        return Zeitgeist.make_from_dialog_by_i_agent_pair(
            dialog_by_i_agent_pair=dialog_by_i_agent_pair
        )


from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Iterator
import abc
import dataclasses
import functools
import itertools
import numbers
import pprint
import random
import re
import string

import ray.rllib.env.multi_agent_env
import ray.rllib.utils.spaces
from ray import rllib
from ray.rllib.algorithms.ppo import PPO # pytype: disable=import-error
import gymnasium
import gymnasium.spaces
import numpy as np


from chicken_coop import county
from chicken_coop.county.constants import ALL_AGENTS
from .stating import State
from chicken_coop.coop_config import CoopConfig



class Env(county.BaseEnv):

    def __init__(self, config: Optional[Mapping] = None) -> None:
        county.BaseEnv.__init__(self, config)
        self.coop_config: CoopConfig = self.config.setdefault('coop_config', CoopConfig())

        self.agents = tuple(self.coop_config.policy_by_agent)
        self.policies = tuple(self.coop_config.policy_by_agent.values())

        self.action_space = gymnasium.spaces.Discrete(2)
        if self.coop_config.identity_is_linear:
            opponent_observation_space = gymnasium.spaces.Box(
                low=0,
                high=self.coop_config.n_agents - 1,
                shape=(2,),
                dtype=int,
            )
        else:
            opponent_observation_space = gymnasium.spaces.MultiBinary(self.coop_config.n_agents)

        observation_space_dict = {
            'i_opponent': opponent_observation_space,
        }

        if self.coop_config.episode_length >= 2:
            observation_space_dict |= {
                'i_turn': gymnasium.spaces.Box(
                    low=0,
                    high=self.coop_config.episode_length,
                    shape=(1,),
                    dtype=int,
                ),
                'n_victory_rewards': gymnasium.spaces.Box(
                    low=0,
                    high=self.coop_config.episode_length,
                    shape=(1,),
                    dtype=int,
                ),
                'n_boredom_rewards': gymnasium.spaces.Box(
                    low=0,
                    high=self.coop_config.episode_length,
                    shape=(1,),
                    dtype=int,
                ),
                'n_defeat_rewards': gymnasium.spaces.Box(
                    low=0,
                    high=self.coop_config.episode_length,
                    shape=(1,),
                    dtype=int,
                ),
                'n_anguish_rewards': gymnasium.spaces.Box(
                    low=0,
                    high=self.coop_config.episode_length,
                    shape=(1,),
                    dtype=int,
                ),
            }

        self.observation_space = gymnasium.spaces.Dict(observation_space_dict)

        self._agent_ids = set(self.agents)
        self.reset()


    def make_initial_state(self) -> State:
        return State.make_initial(coop_config=self.coop_config)

    @staticmethod
    def sample_episode_to_text(algorithm: ray.rllib.algorithms.Algorithm,
                               coop_config: CoopConfig) -> str:
        states = tuple(Env.sample_episode(algorithm))
        return '\n'.join(state.text for state in states)

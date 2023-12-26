# pytype: disable=module-attr
from __future__ import annotations

import collections
from typing import Tuple, Optional, Dict, Mapping, Iterable, Callable, Any
import itertools
import abc
import ray.rllib.env.multi_agent_env

from .base_state import BaseState
from chicken_coop.county.constants import ALL_AGENTS
from chicken_coop.county.typing import Agent, Action, Observation
from chicken_coop.county.misc import compute_actions_for_all_agents


class BaseEnv(ray.rllib.env.multi_agent_env.MultiAgentEnv, abc.ABC):

    def __init__(self, config: Optional[Mapping] = None) -> None:
        ray.rllib.env.multi_agent_env.MultiAgentEnv.__init__(self)
        self.config = config = (config or {})
        self.states = []

    @abc.abstractmethod
    def make_initial_state(self) -> BaseState:
        raise NotImplementedError

    def reset(self, *, seed: Optional[int] = None,
              options: Optional[Mapping] = None) -> Tuple[Mapping[Agent, Observation],
                                                          Mapping[Agent, Any]]:
        match (initial_states_raw := (options or {}).get('initial_states', None)):
            case BaseState():
                self.states[:] = (initial_states_raw,)
            case collections.abc.Iterable():
                self.states[:] = initial_states_raw
            case None:
                self.states[:] = [self.make_initial_state()]
            case _:
                raise RuntimeError

        return (self.state.observation_by_agent, collections.defaultdict(lambda: None))

    @property
    def state(self) -> BaseState:
        return self.states[-1]

    @property
    def observation_by_agent(self) -> Mapping[Agent, Observation]:
        return self.states[-1].observation_by_agent

    def step(self, actions: Mapping[Agent, Action]) -> tuple[Mapping, Mapping, Mapping, Mapping]:
        self.states.append(self.state.step(actions))
        return (self.state.observation_by_agent, self.state.reward_by_agent,
                self.state.terminated_by_agent, self.state.truncated_by_agent, {})

    def render(self, mode: Optional[str] = None) -> str:
        return self.state.text

    def play(self,
             algorithm: ray.rllib.algorithms.Algorithm,
             n: Optional[int] = None,
             stop_condition: Optional[Callable[BaseState, bool]] = None,
             ) -> Iterator[BaseState]:
        for i in (range(n) if n else itertools.count()):
            if stop_condition is not None and stop_condition(self.state):
                return
            actions = compute_actions_for_all_agents(algorithm, self)
            _, _, terminated_by_agent, truncated_by_agent, _ = self.step(actions)
            yield self.state
            if terminated_by_agent[ALL_AGENTS] or truncated_by_agent[ALL_AGENTS]:
                return

    @classmethod
    def sample_episode(cls,
                       algorithm: ray.rllib.algorithms.Algorithm,
                       n: Optional[int] = None,
                       stop_condition: Optional[Callable[BaseState, bool]] = None,
                       initial_states: None | BaseState | Iterable[BaseState] = None,
                       ) -> Iterator[BaseState]:
        env = cls(config=algorithm.config['env_config'])
        env.reset(options={'initial_states': initial_states})
        yield env.state
        new_n = None if (n is None) else (n - 1)
        yield from env.play(algorithm, n=new_n, stop_condition=stop_condition)



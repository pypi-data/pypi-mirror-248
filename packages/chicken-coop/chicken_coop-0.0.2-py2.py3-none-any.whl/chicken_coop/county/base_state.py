from __future__ import annotations

from typing import Mapping
import abc

from chicken_coop.county.typing import Agent, Action, AgentOrAll, Observation, Reward, RealNumber


class BaseState(abc.ABC):

    observation_by_agent: Mapping[Agent, Observation]

    reward_by_agent: Mapping[Agent, Reward]

    terminated_by_agent: Mapping[AgentOrAll, bool]

    truncated_by_agent: Mapping[AgentOrAll, bool]

    text: str

    @abc.abstractstaticmethod
    def make_initial() -> BaseState: # In the future: `-> Self:`
        raise NotImplementedError

    @abc.abstractmethod
    def step(self, actions: Mapping[Agent, Action]) -> BaseState: # In the future: `-> Self:`
        raise NotImplementedError




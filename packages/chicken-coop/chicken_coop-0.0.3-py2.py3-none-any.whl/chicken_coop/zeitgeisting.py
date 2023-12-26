from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, TypeVar
import abc
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

from chicken_coop import county
from chicken_coop.county import misc
from chicken_coop.county.typing import Agent, RealNumber
from chicken_coop.county.constants import ALL_AGENTS

from chicken_coop.coop_config import CoopConfig
from .dominance_hierarching import DominanceHierarchy

_T = TypeVar('_T')


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseArt(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def sum(items, /) -> BaseArt:
        raise NotImplementedError

    def __add__(self, other: Any) -> BaseArt:
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self).sum(self, other)

    @classmethod
    @functools.cache
    def _get_summable_fields(cls):
        return {field_name: field for field_name, field in cls.__dataclass_fields__.items()
                if field_name != 'coop_config'}




@dataclasses.dataclass(frozen=True, kw_only=True)
class AgentPortrait(BaseArt):
    output_fields = (
        'aggressiveness', 'reward', 'weight', #'rapport',
        # 'anguish', 'boredom',
    )

    n_victories: int
    n_defeats: int
    n_anguishes: int
    n_boredoms: int

    coop_config: CoopConfig

    @functools.cached_property
    def weight(self) -> int:
        return (self.n_victories + self.n_defeats + self.n_anguishes + self.n_boredoms)

    # This definition might not be equivalent to the rapport definition for a dialog, so
    # it's commented out.
    # @functools.cached_property
    # def rapport(self) -> RealNumber:
        # if self.weight == 0:
            # return 0
        # else:
            # return (self.n_victories + self.n_defeats) / self.weight

    @functools.cached_property
    def anguish(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_anguishes / self.weight

    @functools.cached_property
    def boredom(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_boredoms / self.weight

    @functools.cached_property
    def aggressiveness(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return (self.n_victories + self.n_anguishes) / self.weight

    @functools.cached_property
    def reward(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return (
                self.n_victories * self.coop_config.victory_reward +
                self.n_defeats * self.coop_config.defeat_reward +
                self.n_anguishes * self.coop_config.anguish_reward +
                self.n_boredoms * self.coop_config.boredom_reward
            ) / self.weight

    @staticmethod
    def sum(items: Iterable[AgentPortrait], /) -> AgentPortrait:
        agent_portraits = tuple(items)
        (coop_config,) = {agent_portrait.coop_config for agent_portrait in agent_portraits}
        return AgentPortrait(
            **{
                field: sum(getattr(agent_portrait, field) for agent_portrait in agent_portraits)
                for field in AgentPortrait._get_summable_fields()
            },
            coop_config=coop_config,
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Dialog(BaseArt):
    output_fields = (
        #'anguish', 'boredom',
        'aggressiveness', 'reward', 'polarity', 'purity', 'rapport', 'weight',
        'left_aggressiveness', 'right_aggressiveness',
    )

    n_agent_a_victories: int
    n_agent_b_victories: int
    n_anguishes: int
    n_boredoms: int

    coop_config: CoopConfig

    @functools.cached_property
    def n_agent_a_hawks(self) -> int:
        return (self.n_agent_a_victories + self.n_anguishes)

    @functools.cached_property
    def n_agent_b_hawks(self) -> int:
        return (self.n_agent_b_victories + self.n_anguishes)

    @functools.cached_property
    def left_aggressiveness(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_agent_a_hawks / self.weight

    @functools.cached_property
    def right_aggressiveness(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_agent_b_hawks / self.weight

    @functools.cached_property
    def weight(self) -> int:
        return (self.n_agent_a_victories + self.n_agent_b_victories + self.n_anguishes +
                self.n_boredoms)

    @functools.cached_property
    def polarity(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return (self.n_agent_b_hawks - self.n_agent_a_hawks) / self.weight

    @functools.cached_property
    def rapport(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return abs(self.n_agent_a_hawks - self.n_agent_b_hawks) / self.weight
            # return (self.n_agent_b_victories + self.n_agent_a_victories) / self.weight

    @functools.cached_property
    def anguish(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_anguishes / self.weight

    @functools.cached_property
    def boredom(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return self.n_boredoms / self.weight

    @functools.cached_property
    def aggressiveness(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return ((self.n_agent_a_victories + self.n_agent_b_victories + self.n_anguishes) /
                                                                                        self.weight)

    @functools.cached_property
    def purity(self) -> RealNumber:
        return abs(self.polarity)

    @functools.cached_property
    def agent_portraits(self) -> tuple[AgentPortrait, AgentPortrait]:
        return (
            AgentPortrait(
                n_victories=self.n_agent_a_victories,
                n_defeats=self.n_agent_b_victories,
                n_anguishes=self.n_anguishes,
                n_boredoms=self.n_boredoms,
                coop_config=self.coop_config,
            ),
            AgentPortrait(
                n_victories=self.n_agent_b_victories,
                n_defeats=self.n_agent_a_victories,
                n_anguishes=self.n_anguishes,
                n_boredoms=self.n_boredoms,
                coop_config=self.coop_config,
            ),
        )


    @functools.cached_property
    def reward(self) -> RealNumber:
        return statistics.mean(agent_portrait.reward for agent_portrait in self.agent_portraits)


    @staticmethod
    def make_zero(coop_config: CoopConfig) -> Dialog:
        return Dialog(n_agent_a_victories=0, n_agent_b_victories=0, n_anguishes=0, n_boredoms=0,
                      coop_config=coop_config)

    @staticmethod
    def sum(items: Iterable[Dialog], /) -> Dialog:
        '''
        Sum a few dialog objects, adding all the metrics together.

        This should only be used on dialogs between the same two agents, in the same order. This
        isn't enforced so you should be careful to only feed dialogs of the same agent pair to this
        function.
        '''
        dialogs = tuple(items)
        return Dialog(
            **{
                field: sum(getattr(dialog, field) for dialog in dialogs)
                for field in Dialog._get_summable_fields()
            },
            coop_config=dialogs[0].coop_config
        )

    def to_array(self) -> np.ndarray:
        return np.array(
            tuple(getattr(self, field) for field in Dialog._get_summable_fields()),
            dtype=float
        )

    @staticmethod
    def from_array(array: np.ndarray, coop_config: CoopConfig) -> Dialog:
        return Dialog(
            **dict(
                zip(
                    Dialog._get_summable_fields(),
                    map(float, array)
                )
            ),
            coop_config=coop_config,
        )

    @staticmethod
    def _dict_to_array(dialog_by_i_agent_pair: dict[_T, Dialog]) -> np.ndarray:
        (coop_config,) = {dialog.coop_config for dialog in dialog_by_i_agent_pair.values()}
        assert tuple(dialog_by_i_agent_pair) == tuple(coop_config.i_agent_pairs_full)
        return np.array(
            [dialog.to_array() for dialog in dialog_by_i_agent_pair.values()],
            dtype=float
        )

    @staticmethod
    def _array_to_dict(array: np.ndarray, coop_config: CoopConfig) -> dict[_T, Dialog]:
        n_agents = misc.int_sqrt(array.shape[0])
        i_agent_pairs_full = itertools.product(range(n_agents), repeat=2)
        from_array = lambda a_: Dialog.from_array(a_, coop_config=coop_config)
        return dict(zip(i_agent_pairs_full, map(from_array, array)))

    def __neg__(self) -> Dialog:
        return Dialog(
            n_agent_a_victories=self.n_agent_b_victories,
            n_agent_b_victories=self.n_agent_a_victories,
            n_anguishes=self.n_anguishes,
            n_boredoms=self.n_boredoms,
            coop_config=self.coop_config
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Zeitgeist(BaseArt):
    dialog_by_i_agent_pair: dict[tuple[int, int], Dialog]

    def __post_init__(self) -> None:
        assert more_itertools.is_sorted(self.dialog_by_i_agent_pair)


    @functools.cached_property
    def coop_config(self) -> CoopConfig:
        (coop_config,) = {dialog.coop_config for dialog in self.dialog_by_i_agent_pair.values()}
        return coop_config

    @functools.cached_property
    def n_agents(self) -> int:
        return self.coop_config.n_agents

    # @staticmethod
    # def make_zero(coop_config: CoopConfig) -> Dialog:
        # return Zeitgeist(
            # dialog_by_i_agent_pair=dict(zip(coop_config.i_agent_pairs_full,
                                            # itertools.repeat(Dialog.make_zero()))),
        # )

    @functools.cached_property
    def dialog_by_rising_i_agent_pair(self) -> dict[tuple[int, int], Dialog]:
        return {(i_agent_a, i_agent_b): dialog for (i_agent_a, i_agent_b), dialog
                in self.dialog_by_i_agent_pair.items() if i_agent_a < i_agent_b}

    @functools.cached_property
    def weight(self) -> int:
        return sum(dialog.weight for (i_agent_a, i_agent_b), dialog in
                   self.dialog_by_rising_i_agent_pair.items())

    @functools.cached_property
    def agent_portraits(self) -> tuple[AgentPortrait, ...]:
        addend_agent_portraits_by_i_agent = [[] for _ in range(self.n_agents)]
        for (i_agent, _), dialog in self.dialog_by_i_agent_pair.items():
            addend_agent_portraits_by_i_agent[i_agent].append(dialog.agent_portraits[0])
        return tuple(
            map(
                AgentPortrait.sum,
                addend_agent_portraits_by_i_agent,
            )
        )

    @functools.cached_property
    def population_portrait(self) -> PopulationPortrait:
        return PopulationPortrait(self)

    @staticmethod
    def sum(items: Iterable[Zeitgeist], /) -> Zeitgeist:
        zeitgeists = tuple(items)
        (coop_config,) = {zeitgeist.coop_config for zeitgeist in zeitgeists}
        return Zeitgeist.make_from_dialog_by_i_agent_pair(
            {i_agent_pair: Dialog.sum(zeitgeist.dialog_by_i_agent_pair[i_agent_pair]
                                       for zeitgeist in zeitgeists)
            for i_agent_pair in coop_config.i_agent_pairs_full}
        )

    @staticmethod
    def make_from_dialog_by_i_agent_pair(dialog_by_i_agent_pair: dict[tuple[int, int], Dialog]
                                         ) -> Zeitgeist:
        dialog_by_i_agent_pair = dict(sorted(dialog_by_i_agent_pair.items()))
        return Zeitgeist(dialog_by_i_agent_pair=dialog_by_i_agent_pair)


    def to_array(self) -> np.ndarray:
        assert tuple(self.dialog_by_i_agent_pair) == tuple(self.coop_config.i_agent_pairs_full)
        return np.array(
            [dialog.to_array() for dialog in self.dialog_by_i_agent_pair.values()],
            dtype=float
        )

    @staticmethod
    def from_array(array: np.ndarray, coop_config: CoopConfig) -> Dialog:
        # todo: This array could be shortened by using something with less redundancies than
        # `i_agent_pairs_full`
        n_agents = misc.int_sqrt(array.shape[0])
        i_agent_pairs_full = itertools.product(range(n_agents), repeat=2)
        from_array = lambda a_: Dialog.from_array(a_, coop_config=coop_config)
        return Zeitgeist.make_from_dialog_by_i_agent_pair(
            dict(zip(i_agent_pairs_full, map(from_array, array), strict=True))
        )

    @functools.cached_property
    def output(self) -> dict[str, RealNumber]:
        return {
            **{
                f'population.{output_field}': getattr(self.population_portrait, output_field)
                for output_field in PopulationPortrait.output_fields
            },
            **{
                f'dialog.{i_agent_a}.{i_agent_b}.{field}':
                    getattr(self.dialog_by_i_agent_pair[i_agent_a, i_agent_b], field)
                for i_agent_a, i_agent_b in self.coop_config.i_agent_pairs_without_diagonal
                for field in Dialog.output_fields
            },
            **{
                f'agent.{i_agent}.{field}': getattr(self.agent_portraits[i_agent], field)
                for i_agent in range(self.n_agents)
                for field in AgentPortrait.output_fields
            },
        }

@dataclasses.dataclass(frozen=True)
class PopulationPortrait:
    output_fields = (
        # 'anguish', 'boredom',
        'aggressiveness', 'reward', 'polarity', 'purity', 'pairwise_purity', 'transitivity',
        'rapport', 'weight', 'dominance_hierarchy',
        'restricted_distance_from_visitor_dominance_hierarchy',
    )

    zeitgeist: Zeitgeist

    @functools.cached_property
    def coop_config(self) -> CoopConfig:
        return self.zeitgeist.coop_config

    @functools.cached_property
    def n_agents(self) -> int:
        return self.zeitgeist.n_agents

    @functools.cached_property
    def weight(self) -> int:
        return self.zeitgeist.weight

    @functools.cached_property
    def polarity(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.polarity for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )


    @functools.cached_property
    def rapport(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.rapport for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )

    @functools.cached_property
    def anguish(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.anguish for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )

    @functools.cached_property
    def boredom(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.boredom for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )

    @functools.cached_property
    def aggressiveness(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.aggressiveness for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )


    @functools.cached_property
    def purity(self) -> RealNumber:
        return abs(self.polarity)


    @functools.cached_property
    def pairwise_purity(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            return np.average(
                tuple(dialog.purity for dialog in
                      self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
                weights=tuple(dialog.weight for dialog in
                              self.zeitgeist.dialog_by_rising_i_agent_pair.values()),
            )

    @functools.cached_property
    def transitivity(self) -> RealNumber:
        if self.weight == 0:
            return 0
        else:
            agent_gifts = [
                abs(
                    sum(self.zeitgeist.dialog_by_i_agent_pair[j_agent, i_agent].polarity
                        for j_agent in set(range(self.n_agents)) - {i_agent})
                ) for i_agent in range(self.n_agents)
            ]
            max_agent_gifts = tuple(map(abs,
                                        range(self.n_agents - 1, -self.n_agents, -2)))
            assert len(agent_gifts) == len(max_agent_gifts)
            assert max_agent_gifts[0] == max_agent_gifts[-1] == self.n_agents - 1
            transitivity = sum(agent_gifts) / sum(max_agent_gifts)
            assert 0 <= transitivity <= 1.000001, (f"Transitivity must be between 0 and 1 but it's "
                                                   f"{transitivity}")
            return transitivity

    @functools.cached_property
    def reward(self):
        return statistics.mean(agent_portrait.reward for agent_portrait in
                               self.zeitgeist.agent_portraits)

    @functools.cached_property
    def dominance_hierarchy(self) -> DominanceHierarchy:

        return DominanceHierarchy(
            (
                i_agent_pair for (i_agent_pair,
                                  dialog) in self.zeitgeist.dialog_by_i_agent_pair.items()
                if dialog.polarity <= - self.coop_config.dominance_hierarchy_polarity_threshold
            ),
            n_agents=self.n_agents
        )

    @functools.cached_property
    def restricted_distance_from_visitor_dominance_hierarchy(self) -> Optional[RealNumber]:
        visitor_dominance_hierarchy = self.coop_config.visitor_dominance_hierarchy
        if visitor_dominance_hierarchy is None:
            return None
        else:
            return self.dominance_hierarchy.get_distance(
                visitor_dominance_hierarchy, i_agents=self.coop_config.i_resident_agents
            )




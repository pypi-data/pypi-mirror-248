from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, TypeVar, Annotated
import collections
import pathlib
import abc
import math
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
import networkx as nx
import plotly.graph_objects as go

from chicken_coop import county
from chicken_coop.county import misc
from chicken_coop.county import nx_tools
from chicken_coop.county.typing import Agent, RealNumber
from chicken_coop.county.constants import ALL_AGENTS

from .exceptions import CoopException


class DominanceHierarchyException(CoopException):
    pass

class InvalidDominanceHierarchy(DominanceHierarchyException):
    pass

class AttemptedTransitiveOperationOnIntransitiveDominanceHierarchy(DominanceHierarchyException):
    pass

class AttemptedCompleteOperationOnIncompleteDominanceHierarchy(DominanceHierarchyException):
    pass

class DominanceRole(enum.Enum):
    DOMINANT = 'dominant'
    SUBORDINATE = 'subordinate'


class DominanceHierarchy:

    _initialized = False

    def __init__(self, edges_or_concise_text: Iterable[tuple[int, int]] | str = (), /, *,
                 n_agents: Optional[int] = None) -> None:
        self.di_graph = nx.DiGraph()
        if isinstance(edges_or_concise_text, str):
            self.di_graph = nx_tools.concise_text_to_oriented_graph(edges_or_concise_text)
        else:
            self.di_graph = nx.DiGraph(edges_or_concise_text)
            if n_agents is not None:
                self.di_graph.add_nodes_from(tuple(i for i in range(n_agents)
                                                   if i not in self.di_graph))
            else:
                self.isolated_i_agents = ()
        self.isolated_i_agents = tuple(nx_tools.nx.isolates(self.di_graph))
        if n_agents is not None:
            assert set(self.di_graph) == set(range(n_agents))

        self.condensed_di_graph = nx.condensation(self.di_graph)
        self.i_agents = tuple(sorted(self.di_graph.nodes))
        assert len(self.i_agents) == self.i_agents[-1] + 1
        self._rising_agent_pairs = tuple(itertools.combinations(self.i_agents, 2))
        self.n_agents = len(self.i_agents)
        if n_agents is not None:
            assert self.n_agents == n_agents
        self.edges = tuple(sorted(self.di_graph.edges))
        for (i_agent, j_agent) in self._rising_agent_pairs:
            assert not (self.di_graph.has_edge(i_agent, j_agent) and
                        self.di_graph.has_edge(j_agent, i_agent))
        self._initialized = True

    def __len__(self) -> int:
        return self.n_agents

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DominanceHierarchy):
            return False
        return (type(self) is type(other)) and nx.utils.graphs_equal(self.di_graph, other.di_graph)

    def __hash__(self) -> int:
        return hash((type(self), str(self)))

    def __or__(self, other: Any) -> DominanceHierarchy:
        if not isinstance(other, DominanceHierarchy):
            return NotImplemented
        return DominanceHierarchy(set(self.edges) | set(other.edges))

    def __sub__(self, other: Any) -> int:
        if not isinstance(other, DominanceHierarchy):
            return NotImplemented
        return self.get_distance(other)


    def __str__(self) -> str:
        return nx_tools.oriented_graph_to_concise_text(self.di_graph)

    def __repr__(self) -> str:
        if self._initialized:
            return f'{type(self).__name__}({repr(str(self))})'
        else:
            return f'<{type(self).__name__} (uninitialized)>'

    # def __json__(self) -> list[Annotated[list[int], 2]]:
        # return list(map(list, self.edges))

    def __json__(self) -> str:
        return str(self)

    def get_distance(self, other_dominance_hierarchy: DominanceHierarchy, /, *,
                     i_agents: Optional[tuple[int, ...]] = None) -> int:
        if self.n_agents != other_dominance_hierarchy.n_agents:
            raise NotImplementedError

        if i_agents is None:
            i_agents = self.i_agents
        else:
            assert set(i_agents) <= set(self.i_agents)

        assert len(i_agents) >= 2

        rising_agent_pairs = tuple(itertools.combinations(i_agents, 2))

        result = sum((self.get_relationship(i_agent, j_agent) !=
                                       other_dominance_hierarchy.get_relationship(i_agent, j_agent))
                     for (i_agent, j_agent) in rising_agent_pairs) / len(rising_agent_pairs)
        assert 0 <= result <= 1
        return result

    @functools.cached_property
    def simple_cycles(self) -> tuple[tuple[int, ...], ...]:
        return tuple(map(tuple, nx.simple_cycles(self.di_graph)))

    @functools.cached_property
    def is_transitive(self) -> bool:
        return not self.simple_cycles

    @functools.cached_property
    def is_complete(self) -> bool:
        assert self._initialized
        return nx_tools.is_tournament(self.di_graph)

    @functools.cached_property
    def i_agent_by_rank(self) -> tuple[int, ...]:
        if not self.is_transitive:
            raise AttemptedTransitiveOperationOnIntransitiveDominanceHierarchy
        return tuple(nx.topological_sort(self.di_graph))

    @functools.cached_property
    def linear_ranks(self) -> tuple[int, ...]:
        linear_ranks = []
        i_agent_needle = 0
        for condensed_node in nx.topological_sort(self.condensed_di_graph):
            nodes = self.condensed_di_graph.nodes.data()[condensed_node]['members']
            if len(nodes) == 1:
                linear_ranks.append(i_agent_needle)
            i_agent_needle += len(nodes)

        assert i_agent_needle == self.n_agents
        return tuple(linear_ranks)

    @functools.cached_property
    def non_linear_ranks(self) -> tuple[int, ...]:
        return tuple(i for i in self.i_agents if i not in self.linear_ranks)

    @functools.cached_property
    def condensed_plot_svg(self) -> go.Figure:
        from .plotting.plotting_dominance_hierarchies import make_condensed_plot_svg
        return make_condensed_plot_svg(self)

    @staticmethod
    def get_from_rollout_jsonl(rollout_jsonl_path: pathlib.Path) -> DominanceHierarchy:
        return DominanceHierarchy(
            misc.get_last_entry_from_jsonl(rollout_jsonl_path)['population']['dominance_hierarchy']
        )

    def get_relationship(self, i_agent: int, i_other_agent: int) -> Optional[DominanceRole]:
        assert i_agent != i_other_agent
        assert {i_agent, i_other_agent} <= set(self.i_agents)
        if self.di_graph.has_edge(i_agent, i_other_agent):
            return DominanceRole.DOMINANT
        elif self.di_graph.has_edge(i_other_agent, i_agent):
            return DominanceRole.SUBORDINATE
        return None

    @staticmethod
    def get_trivial(n_agents: int) -> DominanceHierarchy:
        return DominanceHierarchy(' => '.join(map(str, range(n_agents))))


    @staticmethod
    def get_mean_rank_linearity(
        dominance_hierarchies: Iterable[DominanceHierarchy] | DominanceHierarchy
        ) -> tuple[RealNumber, ...]:
        dominance_hierarchies = misc.to_tuple(dominance_hierarchies, item_type=DominanceHierarchy)
        (n_ranks,) = set(map(len, dominance_hierarchies))
        linear_ranks = tuple(
            itertools.chain.from_iterable(dominance_hierarchy.linear_ranks for
                                          dominance_hierarchy in dominance_hierarchies)
        )
        counter = collections.Counter(linear_ranks)
        return tuple(counter[i] / len(dominance_hierarchies) for i in range(n_ranks))








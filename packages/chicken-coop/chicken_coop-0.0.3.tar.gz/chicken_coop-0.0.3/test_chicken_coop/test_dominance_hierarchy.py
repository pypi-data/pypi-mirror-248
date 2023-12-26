from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, TypeVar, Annotated
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

import chicken_coop # Imported first to filter out warnings.

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

from chicken_coop import DominanceHierarchy
from chicken_coop.county import nx_tools


def test():
    dominance_hierarchy = DominanceHierarchy('0 => 1 => 2')
    assert dominance_hierarchy == DominanceHierarchy(((0, 1), (0, 2), (1, 2)))
    assert dominance_hierarchy != DominanceHierarchy(((0, 1), (0, 2)))
    assert dominance_hierarchy != DominanceHierarchy(((0, 1), (2, 0), (1, 2)))
    assert str(dominance_hierarchy) == '0 => 1 => 2'
    assert repr(dominance_hierarchy) == "DominanceHierarchy('0 => 1 => 2')"
    assert dominance_hierarchy.is_transitive
    assert dominance_hierarchy.is_complete


def test_distance():
    dh_0 = DominanceHierarchy('0 => 1 => 2 => 3')
    dh_1 = DominanceHierarchy('0 => 3 => 2 => 1')
    dh_2 = DominanceHierarchy('(0 -> 1 -> 2 -> 0) => 3')

    assert (dh_0 - dh_0) == (dh_1 - dh_1) == (dh_2 - dh_2) == 0
    assert (dh_0 - dh_1) == (dh_1 - dh_0) == 3
    assert (dh_0 - dh_2) == (dh_2 - dh_0) == 1
    assert (dh_1 - dh_2) == (dh_2 - dh_1) == 4


def test_isolated():
    dh_0 = DominanceHierarchy('0 => 1 => 2 <3? 4?>')
    dh_1 = DominanceHierarchy('0 => 1 => 2')
    assert dh_0 == dh_0
    assert dh_0.n_agents == 5
    assert dh_1 == dh_1
    assert dh_1.n_agents == 3

    assert dh_0 == DominanceHierarchy(((0, 1), (0, 2), (1, 2)), n_agents=5)
    assert dh_0 != DominanceHierarchy(((0, 1), (0, 2), (1, 2)), n_agents=6)
    assert str(dh_0) == '0 => 1 => 2 <3? 4?>'

def make_di_graph(edges_and_extra_nodes: Iterable[tuple[int, int] | int]):
    edges = []
    extra_nodes = []
    for edge_or_extra_node in edges_and_extra_nodes:
        if isinstance(edge_or_extra_node, tuple):
            edges.append(edge_or_extra_node)
        else:
            assert isinstance(edge_or_extra_node, int)
            extra_nodes.append(edge_or_extra_node)

    di_graph = nx.DiGraph(edges)
    di_graph.add_nodes_from(extra_nodes)
    return di_graph


def test_str():
    def test_case(di_graph: nx.DiGraph, concise_text: str) -> None:
        assert nx_tools.oriented_graph_to_concise_text(di_graph) == concise_text
        assert nx.utils.graphs_equal(di_graph,
                                     nx_tools.concise_text_to_oriented_graph(concise_text))

    test_case(
        nx.DiGraph([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                    (4, 1), (4, 2), (4, 3), (4, 5),
                    (1, 2), (1, 3), (1, 5),
                    (2, 3), (2, 5),
                    (5, 3)]),
        '0 => 4 => 1 => 2 => 5 => 3',
    )
    test_case(
        nx.DiGraph([
            (1, 2), (2, 3), (3, 1),
            (1, 4), (1, 0), (1, 5),
            (2, 4), (2, 0), (2, 5),
            (3, 4), (3, 0), (3, 5),
            (4, 0), (4, 5), (0, 5)
        ]),
        '(1 -> 2 -> 3 -> 1) => 4 => 0 => 5',
    )
    test_case(
        nx.DiGraph([(1, 2), (2, 3), (3, 1),
                    (1, 0), (1, 4), (1, 5),
                    (2, 0), (2, 4), (2, 5),
                    (3, 0), (3, 4), (3, 5),
                    (0, 4), (4, 5), (5, 0)]),
        '(1 -> 2 -> 3 -> 1) => (0 -> 4 -> 5 -> 0)',
    )
    test_case(
        nx.DiGraph([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 3), (1, 4),
            (2, 1),
            (3, 2),
            (4, 2), (4, 3),
            (1, 5), (2, 5), (3, 5), (4, 5),
        ]),
        '0 => (1 -> 3 -> 2 -> 1 -> 4 -> 2 | 4 -> 3) => 5',
    )
    test_case(
        make_di_graph([
            0,
            (1, 3),
            (2, 1),
            (3, 2),
            (4, 1), (4, 2), (4, 3),
        ]),
        '4 => (1 -> 3 -> 2 -> 1) <0?>',
    )
    test_case(
        make_di_graph([
            (0, 1),
            (2, 4),
            3,
            5,
            6,
        ]),
        '(0, 1), (2, 4) <3? 5? 6?>',
    )


def test_distance():
    assert DominanceHierarchy('0 => 1 => 2') - DominanceHierarchy('2 => 1 => 0') == \
           DominanceHierarchy('2 => 1 => 0') - DominanceHierarchy('0 => 1 => 2') == \
           DominanceHierarchy('2 => 1 => 0').get_distance(DominanceHierarchy('0 => 1 => 2')) == \
           DominanceHierarchy('2 => 1 => 0').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 1, 2)) == \
           DominanceHierarchy('2 => 1 => 0').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 1)) == \
           DominanceHierarchy('2 => 1 => 0').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 2)) == \
           DominanceHierarchy('2 => 1 => 0').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(1, 2)) == 1

    assert DominanceHierarchy('0 => 1 => 2') - DominanceHierarchy('0 => 1 => 2') == \
           DominanceHierarchy('0 => 1 => 2') - DominanceHierarchy('0 => 1 => 2') == \
           DominanceHierarchy('0 => 1 => 2').get_distance(DominanceHierarchy('0 => 1 => 2')) == \
           DominanceHierarchy('0 => 1 => 2').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 1, 2)) == \
           DominanceHierarchy('0 => 1 => 2').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 1)) == \
           DominanceHierarchy('0 => 1 => 2').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(0, 2)) == \
           DominanceHierarchy('0 => 1 => 2').get_distance(DominanceHierarchy('0 => 1 => 2'),
                                                          i_agents=(1, 2)) == 0

    assert DominanceHierarchy('0 => 1 => 2 => 3') - DominanceHierarchy('3 => 2 => 1 => 0') == \
           DominanceHierarchy('3 => 2 => 1 => 0') - DominanceHierarchy('0 => 1 => 2 => 3') == 1

    assert DominanceHierarchy('0 => 1 => 2 => 3') - DominanceHierarchy('0 => 1 => 3 => 2') == 1 / 6

    assert DominanceHierarchy('0 => 1 => 2 => 3').get_distance(
                                    DominanceHierarchy('0 => 1 => 3 => 2'), i_agents=(0, 1, 2)) == 0
    assert DominanceHierarchy('0 => 1 => 2 => 3').get_distance(
                                DominanceHierarchy('0 => 1 => 3 => 2'), i_agents=(1, 2, 3)) == 1 / 3
    assert DominanceHierarchy('0 => 1 => 2 => 3').get_distance(
                                DominanceHierarchy('0 => 1 => 3 => 2'), i_agents=(2, 3)) == 1


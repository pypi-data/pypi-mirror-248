from __future__ import annotations

import itertools
import re
from typing import Any

import networkx as nx
import more_itertools


def is_oriented(di_graph: nx.DiGraph) -> bool:
    for node_a, node_b in itertools.combinations(di_graph, 2):
        if (((node_a, node_b) in di_graph.edges) and ((node_b, node_a) in di_graph.edges)):
            return False
    return True

def is_tournament(di_graph: nx.DiGraph) -> bool:
    return len(di_graph) <= 1 or ((nx.density(di_graph) == 0.5) and is_oriented(di_graph))


def scc_di_graph_to_concise_text(scc_di_graph: nx.DiGraph) -> str:
    assert nx.is_strongly_connected(scc_di_graph)
    assert is_tournament(scc_di_graph)
    assert all(isinstance(node, int) for node in scc_di_graph)
    if len(scc_di_graph) == 1:
        (node,) = scc_di_graph
        return str(node)
    else:
        available_edges = sorted(scc_di_graph.edges)
        fluffs = []
        while available_edges:
            fluffs.append(fluff := [available_edges.pop(0)])
            while True:
                for edge in available_edges:
                    if edge[0] == fluff[-1][1]:
                        available_edges.remove(edge)
                        fluff.append(edge)
                        break
                else:
                    break

        fluff_texts = [
            ' -> '.join(map(str, (fluff[0][0],) + tuple(zip(*fluff, strict=True))[1]))
            for fluff in fluffs
        ]
        return '(' + ' | '.join(fluff_texts) + ')'


def oriented_graph_to_concise_text(oriented_graph: nx.DiGraph) -> str:
    assert is_oriented(oriented_graph)
    assert all(isinstance(node, int) for node in oriented_graph)
    oriented_graph_without_isolated_nodes = nx.DiGraph(oriented_graph.edges)

    if is_tournament(oriented_graph_without_isolated_nodes):
        condensed_di_graph = nx.condensation(oriented_graph_without_isolated_nodes)
        scc_concise_texts = []
        for meta_node in nx.topological_sort(condensed_di_graph):
            nodes = set(condensed_di_graph.nodes.data()[meta_node]['members'])
            scc_di_graph = get_sub_di_graph(oriented_graph_without_isolated_nodes, nodes)
            scc_concise_texts.append(scc_di_graph_to_concise_text(scc_di_graph))
        result = ' => '.join(scc_concise_texts)
    else:
        result = ', '.join(f'({edge[0]}, {edge[1]})' for edge in oriented_graph.edges())

    isolated_nodes = tuple(nx.isolates(oriented_graph))
    if isolated_nodes:
        inner = ' '.join(f'{isolated_node}?' for isolated_node in isolated_nodes)
        result += f' <{inner}>'
    return result


_scc_di_graph_subpattern = re.compile(
    '(?:([1-9][0-9]*) -> )*([1-9][0-9]*)'
)
_scc_di_graph_pattern = re.compile(
    fr' \| '
)

def concise_text_to_scc_di_graph(concise_text: str) -> nx.DiGraph:
    if concise_text.isnumeric():
        di_graph = nx.DiGraph({int(concise_text): ()})
    else:
        inner_text = re.fullmatch(r'^\(([0-9| \->]+)\)$', concise_text).group(1)
        parts = inner_text.split(' | ')
        di_graph = nx.DiGraph(
            itertools.chain.from_iterable(
                more_itertools.windowed(map(int, part.split(' -> ')), 2) for part in parts
            )
        )
    assert nx.is_strongly_connected(di_graph)
    assert is_tournament(di_graph)
    return di_graph


isolated_nodes_pattern = re.compile(r' <(?:[0-9]+\? )*[0-9]+\?>$')
isolated_nodes_subpattern = re.compile(r'^$')

def concise_text_to_oriented_graph(concise_text: str) -> nx.DiGraph:
    isolated_nodes_match = isolated_nodes_pattern.search(concise_text)
    isolated_nodes = (() if isolated_nodes_match is None
                      else tuple(map(int, re.findall('[0-9]+', isolated_nodes_match.group(0)))))
    short_concise_text = isolated_nodes_pattern.sub('', concise_text)
    if '=>' not in short_concise_text and '->' not in short_concise_text:
        di_graph = nx.DiGraph(eval(f'({short_concise_text})')) # Ugly hack
    else:
        scc_di_graphs = tuple(map(concise_text_to_scc_di_graph, short_concise_text.split(' => ')))
        di_graph = nx.DiGraph(
            itertools.chain.from_iterable(
                itertools.chain(
                    (scc_di_graph.edges for scc_di_graph in scc_di_graphs),
                    itertools.starmap(itertools.product, itertools.combinations(scc_di_graphs, 2))
                )
            )
        )
    assert not (set(isolated_nodes) & set(di_graph))
    di_graph.add_nodes_from(isolated_nodes)
    assert is_oriented(di_graph)
    return di_graph


def get_sub_di_graph(di_graph: nx.DiGraph, nodes: Iterable) -> nx.DiGraph:
    node_set = set(nodes)
    sub_di_graph = nx.DiGraph(edge for edge in di_graph.edges if set(edge) <= node_set)
    sub_di_graph.add_nodes_from(nodes)
    return sub_di_graph



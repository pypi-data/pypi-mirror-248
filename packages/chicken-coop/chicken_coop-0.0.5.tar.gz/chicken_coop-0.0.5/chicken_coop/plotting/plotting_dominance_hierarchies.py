from __future__ import annotations

import abc
import random
import math
import os
import logging
import pathlib
import sys
import itertools
import tempfile
import warnings
import functools
from typing import Optional, Iterable
import pathlib

import click
import more_itertools
import pandas as pd
import numpy as np
import scipy.signal
import networkx as nx
import plotly.graph_objects as go
import svgwrite

import chicken_coop

from ..command_group import cli
from chicken_coop.county import nx_tools
from chicken_coop.county import misc
from chicken_coop.county.typing import RealNumber
from .. import utils
from ..dominance_hierarching import DominanceHierarchy


DOUBLE_ARROW_LENGTH = 10
DOUBLE_ARROW_GAP = 1.8
DOUBLE_ARROW_HEAD_DIAGONAL_LENGTH = 4.5
DOUBLE_ARROW_SHAFT_STROKE_WIDTH = 0.7
DOUBLE_ARROW_HEAD_STROKE_WIDTH = 1
SMALL_ARROW_GAP = 8
SMALL_ARROW_STROKE_WIDTH = 0.7
SMALL_ARROW_HEAD_DIAGONAL_LENGTH = 2.5
PADDING = 2.2
NODE_RADIUS = 5

RED = '#c66'

FONT_X_OFFSET = 0
FONT_Y_OFFSET = 1
FONT_SIZE = 8
FONT_FAMILY = '"Noto Mono", Consolas, "Ubuntu Mono", monospace'



def make_condensed_plot_svg(dominance_hierarchies: Iterable[DominanceHierarchy] | DominanceHierarchy
                            ) -> str:
    dominance_hierarchies = misc.to_tuple(dominance_hierarchies, item_type=DominanceHierarchy)
    return StackedCondensedDominanceHierarchyShapino(dominance_hierarchies).svg_text


class CuteShapino(misc.Shapino, abc.ABC):
    def __init__(self, *args, x: RealNumber = 0, y: RealNumber = 0, **kwargs) -> None:
        super().__init__(self.make_cute_shapes(*args, **kwargs), x=x, y=y)

    @abc.abstractmethod
    def make_cute_shapes(self, *args, **kwargs
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        raise NotImplementedError

class RowShapino(CuteShapino):

    padding = 0

    def make_cute_shapes(self, shapinos: Iterable[misc.Shapino],
                         debug: bool = False,
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        shapinos = tuple(shapinos)
        new_shapinos = [
            shapino.duplicate_with_anchor_on_middle_left().duplicate_with_offset(offset, 0)
            for shapino, offset in zip(
                shapinos,
                misc.zero_based_accumulate((shapino.bounding_box[2] + self.padding
                                            for shapino in shapinos),
                                           drop_last=True),
                strict=True
            )
        ]
        if debug:
            for new_shapino in new_shapinos:
                new_shapino.shapes.append(
                    svgwrite.shapes.Rect(
                        new_shapino.bounding_box[:2],
                        new_shapino.bounding_box[2:],
                        stroke=random.choice(('red', 'orange', 'purple', 'yellow', 'green')),
                        stroke_dasharray=2,
                        stroke_width=0.2,
                        fill='blue',
                        fill_opacity=0.1,
                        stroke_opacity=0.2,
                    )
                )
        return new_shapinos


class ColumnShapino(CuteShapino):

    padding = 0

    def make_cute_shapes(self, shapinos: Iterable[misc.Shapino],
                         debug: bool = False,
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        shapinos = tuple(shapinos)
        new_shapinos = [
            shapino.duplicate_with_anchor_on_top_center().duplicate_with_offset(0, offset)
            for shapino, offset in zip(
                shapinos,
                misc.zero_based_accumulate((shapino.bounding_box[3] + self.padding
                                            for shapino in shapinos),
                                           drop_last=True),
                strict=True
            )
        ]
        if debug:
            for new_shapino in new_shapinos:
                new_shapino.shapes.append(
                    svgwrite.shapes.Rect(
                        new_shapino.bounding_box[:2],
                        new_shapino.bounding_box[2:],
                        stroke=random.choice(('red', 'orange', 'purple', 'yellow', 'green')),
                        stroke_dasharray=2,
                        stroke_width=0.2,
                        fill='blue',
                        fill_opacity=0.1,
                        stroke_opacity=0.2,
                    )
                )
        return new_shapinos



class StackedCondensedDominanceHierarchyShapino(ColumnShapino):

    padding = 8

    def make_cute_shapes(self, dominance_hierarchies: Iterable[DominanceHierarchy]
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        return ColumnShapino.make_cute_shapes(
            self,
            [CondensedDominanceHierarchyShapino(dominance_hierarchy)
             for dominance_hierarchy in dominance_hierarchies]
        )


class CondensedDominanceHierarchyShapino(RowShapino):
    def make_cute_shapes(self, dominance_hierarchy: DominanceHierarchy
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        shapinos = []
        for i, condensed_node in enumerate(nx.topological_sort(
                                                           dominance_hierarchy.condensed_di_graph)):
            nodes = dominance_hierarchy.condensed_di_graph.nodes.data()[condensed_node]['members']
            shapinos.append(SccShapino(nx_tools.get_sub_di_graph(dominance_hierarchy.di_graph,
                                                                 nodes)))
            if i < len(dominance_hierarchy.condensed_di_graph) - 1:
                shapinos.append(DoubleArrowShapino())
        return RowShapino.make_cute_shapes(self, shapinos)


class NodeShapino(CuteShapino):

    padding = PADDING

    def make_cute_shapes(self, text: str) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        assert len(text) == 1
        self.text = text
        return (
            svgwrite.shapes.Circle(r=NODE_RADIUS, fill='#cce', stroke='#666', stroke_width=0.5),
            svgwrite.text.Text(text=text, font_size=FONT_SIZE, font_family=FONT_FAMILY,
                               text_anchor='middle', dominant_baseline='middle',
                               fill='#444',
                               insert=(FONT_X_OFFSET, FONT_Y_OFFSET),
                               font_weight='bold'),
        )



class SccShapino(CuteShapino):

    padding = PADDING

    def make_cute_shapes(self, scc: nx.DiGraph
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        self.scc = scc
        nodes = sorted(scc)
        n_nodes = len(scc)
        self.is_single = (n_nodes == 1)
        radius = _get_scc_radius(scc)
        node_shapinos = [
            NodeShapino(
                x=radius * math.cos(math.tau * i / n_nodes),
                y=radius * math.sin(math.tau * i / n_nodes),
                text=str(node),
            )
            for i, node in enumerate(nodes)
        ]

        small_arrow_shapinos = []
        for dominant_node, subordinate_node in scc.edges:
            i_dominant_node = nodes.index(dominant_node)
            i_subordinate_node = nodes.index(subordinate_node)
            gapless_source_x = radius * math.cos(math.tau * i_dominant_node / n_nodes)
            gapless_source_y = radius * math.sin(math.tau * i_dominant_node / n_nodes)
            gapless_destination_x = radius * math.cos(math.tau * i_subordinate_node / n_nodes)
            gapless_destination_y = radius * math.sin(math.tau * i_subordinate_node / n_nodes)
            gapless_delta_x = gapless_destination_x - gapless_source_x
            gapless_delta_y = gapless_destination_y - gapless_source_y
            gapless_length = (gapless_delta_x ** 2 + gapless_delta_y ** 2) ** 0.5
            gap_x = gapless_delta_x * SMALL_ARROW_GAP / gapless_length
            gap_y = gapless_delta_y * SMALL_ARROW_GAP / gapless_length

            small_arrow_shapinos.append(
                SmallArrowShapino(
                    source_x=gapless_source_x + gap_x,
                    source_y=gapless_source_y + gap_y,
                    destination_x=gapless_destination_x - gap_x,
                    destination_y=gapless_destination_y - gap_y,
                )
            )

        shapinos = node_shapinos + small_arrow_shapinos
        if not self.is_single:
            big_circle = svgwrite.shapes.Circle(
                r=radius + NODE_RADIUS + 3,
                fill=RED,
                opacity=0.18,
            )
            shapinos.insert(0, big_circle)
        return shapinos




class SingleArrowShapino(CuteShapino):

    def make_cute_shapes(self, start: tuple[RealNumber, RealNumber],
                         end: tuple[RealNumber, RealNumber]
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        raise NotImplementedError
        stroke_kwargs = {'stroke': RED}
        shaft_lines = [
            svgwrite.shapes.Line(
                start=(0, sign * DOUBLE_ARROW_GAP / 2),
                end=(DOUBLE_ARROW_LENGTH - DOUBLE_ARROW_GAP / 2, sign * DOUBLE_ARROW_GAP / 2),
                stroke_width=DOUBLE_ARROW_SHAFT_STROKE_WIDTH,
                **stroke_kwargs,
            )
            for sign in (-1, 1)
        ]
        foo = DOUBLE_ARROW_HEAD_DIAGONAL_LENGTH * pow(2, -0.5)
        head_lines = [
            svgwrite.shapes.Line(
                start=(DOUBLE_ARROW_LENGTH, 0),
                end=(DOUBLE_ARROW_LENGTH - foo , sign * foo),
                stroke_linecap='round',
                stroke_width=DOUBLE_ARROW_HEAD_STROKE_WIDTH,
                **stroke_kwargs,
            )
            for sign in (-1, 1)
        ]
        return (*shaft_lines, *head_lines)


class DoubleArrowShapino(CuteShapino):

    padding = PADDING

    def make_cute_shapes(self) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        stroke_kwargs = {'stroke': RED}
        shaft_lines = [
            svgwrite.shapes.Line(
                start=(0, sign * DOUBLE_ARROW_GAP / 2),
                end=(DOUBLE_ARROW_LENGTH - DOUBLE_ARROW_GAP / 2, sign * DOUBLE_ARROW_GAP / 2),
                stroke_width=DOUBLE_ARROW_SHAFT_STROKE_WIDTH,
                **stroke_kwargs,
            )
            for sign in (-1, 1)
        ]
        foo = DOUBLE_ARROW_HEAD_DIAGONAL_LENGTH * pow(2, -0.5)
        head_lines = [
            svgwrite.shapes.Line(
                start=(DOUBLE_ARROW_LENGTH, 0),
                end=(DOUBLE_ARROW_LENGTH - foo , sign * foo),
                stroke_linecap='round',
                stroke_width=DOUBLE_ARROW_HEAD_STROKE_WIDTH,
                **stroke_kwargs,
            )
            for sign in (-1, 1)
        ]
        return (*shaft_lines, *head_lines)


class SmallArrowShapino(CuteShapino):

    padding = PADDING

    def make_cute_shapes(self, source_x: RealNumber, source_y: RealNumber,
                         destination_x: RealNumber, destination_y: RealNumber
                         ) -> Iterable[svgwrite.base.BaseElement | misc.Shapino]:
        stroke_kwargs = {'stroke': RED,
                         'stroke_width': SMALL_ARROW_STROKE_WIDTH}
        shaft_line = svgwrite.shapes.Line(
                start=(source_x, source_y),
                end=(destination_x, destination_y),
                **stroke_kwargs
            )

        delta_x = source_x - destination_x
        delta_y = source_y - destination_y
        length = (delta_x ** 2 + delta_y ** 2) ** 0.5
        foo = SMALL_ARROW_HEAD_DIAGONAL_LENGTH * pow(2, -0.5)
        delta_fluff_x = foo * delta_x / length
        delta_fluff_y = foo * delta_y / length
        angle = math.atan2(delta_fluff_y, delta_fluff_x) + math.tau / 4
        delta_zuff_x = foo * math.cos(angle)
        delta_zuff_y = foo * math.sin(angle)

        head_lines = [
            svgwrite.shapes.Line(
                start=(destination_x, destination_y),
                end=(destination_x + delta_fluff_x + sign * delta_zuff_x,
                     destination_y + delta_fluff_y + sign * delta_zuff_y,),
                stroke_linecap='round',
                **stroke_kwargs,
            )
            for sign in (-1, 1)
        ]

        return [shaft_line] + head_lines



def _get_scc_radius(scc: nx.DiGraph) -> RealNumber:
    return ((0 if (len(scc) == 1) else 14 + 5 * (len(scc) - 3)))


from __future__ import annotations

import random
import re
import collections
import statistics
import tempfile
import time
import math
import os
import logging
import pathlib
import sys
import itertools
import warnings
import functools
from typing import Optional
import pathlib
import webbrowser

import click
import more_itertools
import pandas as pd
import numpy as np
import scipy.signal
import networkx as nx
import plotly.graph_objects as go
import plotly.colors
import plotly.subplots

import chicken_coop

from ..command_group import cli
from chicken_coop.county import misc
from chicken_coop.county import trekking
from chicken_coop.county.typing import RealNumber
from .. import utils
from ..dominance_hierarching import (DominanceHierarchy,
                                     AttemptedTransitiveOperationOnIntransitiveDominanceHierarchy)
from . import constants
from . import plotting_dominance_hierarchies


ANIMAL_DATA_FOLDER = (pathlib.Path(__file__) / '../../../animal_data').resolve()
N_GENERATIONS_SHORT = 100
N_GENERATIONS_LONG = 150
Y_RANGE = (-0.05, 1.05)
BLUE_TO_RED = [
    [0, "rgb(0,0,255)"],
    [1, "rgb(255,0,0)"],
]

@cli.group()
@click.option('-p', '--path', 'trek_path_expression', type=str, required=False)
@click.option('-s', '--show/--dont-show', 'show_plot', is_flag=True, default=True)
@click.option('-w', '--write/--dont-write', 'write_plot', is_flag=True, default=True)
@click.option('-f', '--forgive-lack-of-samples', 'forgive_lack_of_samples', is_flag=True)
@click.pass_context
def plot_deck(context: click.Context, *, trek_path_expression: Optional[str],
              show_plot: bool, write_plot: bool,
              forgive_lack_of_samples: bool) -> None:
    context.ensure_object(dict)
    context.obj['trek_path_expression'] = trek_path_expression
    context.obj['show_plot'] = show_plot
    context.obj['write_plot'] = write_plot
    context.obj['forgive_lack_of_samples'] = forgive_lack_of_samples

global_layout_template = dict(
    plot_bgcolor='rgb(255, 255, 255, 0)',
    title_font_size=1,
    width=1_850,
    height=950,
)

global_axis_template = dict(
    showline=True,
    linewidth=3,
    linecolor='black',
)

global_y_axis_template = dict(
    range=Y_RANGE,
    tickformat='.1f',
)

def _show_and_or_write_plot(figure: go.Figure, *, name: str, context: click.Context) -> None:
    if context.obj['show_plot']:
        figure.show()
    if context.obj['write_plot']:
        folder: pathlib.Path = pathlib.Path.home() / 'Desktop'
        folder.mkdir(parents=True, exist_ok=True)
        figure.write_image(folder / f'{name}.png')



@plot_deck.command()
@click.pass_context
def two_aggressiveness(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], moniker='deck-two',
                             allow_single_trek=False)

    print(f'Making `two-aggressiveness` plots for {trek} ...', file=sys.stderr)

    dfs = [mini_trek.rollout_dataframe.filter(regex=r'agent\.[0-9]+\.aggressiveness')
           for mini_trek in trek.mini_treks[:10]]
    aggressiveness_column_names = tuple(sorted(name for name in dfs[0].columns
                                               if 'aggressiveness' in name and 'agent' in name))
    axis_template = global_axis_template | dict(
        linewidth=2,
        title_font=dict(size=50),
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    def make_label(column_name: str) -> str:
        i_agent = re.fullmatch(r'^agent\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Agent {i_agent}'


    for i, df in enumerate(dfs):
        figure = go.Figure(
            data=tuple(
                go.Scatter(
                    x=df.index, y=df[aggressiveness_column_name],
                    name=make_label(aggressiveness_column_name),
                    line=dict(
                        width=5.5,
                        color=plotly.colors.sample_colorscale(
                            BLUE_TO_RED,
                            i / (len(aggressiveness_column_names) - 1),
                            )[0]
                    ),
                )
                for i, aggressiveness_column_name in enumerate(aggressiveness_column_names)
            ),
            layout=go.Layout(
                **global_layout_template,
                xaxis=dict(
                  **axis_template,
                  title='Generation',
                  range=(0, N_GENERATIONS_SHORT),
                ),
                yaxis=dict(
                  **axis_template,
                  **global_y_axis_template,
                  title=dict(text='Aggressiveness'),
                ),
                showlegend=True,
                legend=dict(
                    xanchor='right', yanchor='middle',
                    y=0.5,
                    font=dict(size=40)
                ),
            ),
        )

        _show_and_or_write_plot(figure, name=f'two_aggressiveness_{i}', context=context)


@plot_deck.command()
@click.pass_context
def six_aggressiveness(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], moniker='deck-six',
                             allow_single_trek=False)

    print(f'Making `six-aggressiveness` plots for {trek} ...', file=sys.stderr)

    dfs = [mini_trek.rollout_dataframe.filter(regex=r'agent\.[0-9]+\.aggressiveness')
           for mini_trek in trek.mini_treks[:10]]
    aggressiveness_column_names = tuple(sorted(name for name in dfs[0].columns
                                               if 'aggressiveness' in name and 'agent' in name))
    axis_template = global_axis_template | dict(
        linewidth=2,
        title_font=dict(size=50),
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    def make_label(column_name: str) -> str:
        i_agent = re.fullmatch(r'^agent\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Agent {i_agent}'


    for i, df in enumerate(dfs):
        figure = go.Figure(
            data=tuple(
                go.Scatter(
                    x=df.index, y=df[aggressiveness_column_name],
                    name=make_label(aggressiveness_column_name),
                    line=dict(
                        width=5.5,
                        color=plotly.colors.DEFAULT_PLOTLY_COLORS[i]
                    ),
                )
                for i, aggressiveness_column_name in enumerate(aggressiveness_column_names)
            ),
            layout=go.Layout(
                **global_layout_template,
                xaxis=dict(
                  **axis_template,
                  title='Generation',
                  range=(0, N_GENERATIONS_SHORT),
                ),
                yaxis=dict(
                  **axis_template,
                  **global_y_axis_template,
                  title=dict(text='Aggressiveness'),
                ),
                showlegend=True,
                legend=dict(
                    xanchor='left', yanchor='middle',
                    y=0.8,
                    x=0.02,
                    font=dict(size=32),
                    traceorder='normal',
                ),
            ),
        )

        _show_and_or_write_plot(figure, name=f'six_aggressiveness_{i}', context=context)


@plot_deck.command()
@click.pass_context
def six_aggressiveness_pair(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], moniker='deck-six',
                             allow_single_trek=False)

    i_agent_pair = (1, 4)

    print(f'Making `six-aggressiveness-pair` plots for {trek} ...', file=sys.stderr)

    dfs = [mini_trek.rollout_dataframe.filter(
                regex=fr'dialog\.{i_agent_pair[0]}\.{i_agent_pair[1]}\.(left|right)_aggressiveness')
           for mini_trek in trek.mini_treks[:10]]
    aggressiveness_column_names = tuple(sorted(dfs[0].columns))
    axis_template = global_axis_template | dict(
        linewidth=2,
        title_font=dict(size=50),
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    for i, df in enumerate(dfs):
        figure = go.Figure(
            data=tuple(
                go.Scatter(
                    x=df.index, y=df[aggressiveness_column_name],
                    name=f'Agent {i_agent}',
                    line=dict(
                        width=5.5,
                        color=plotly.colors.DEFAULT_PLOTLY_COLORS[i_agent]
                    ),
                )
                for i_agent, aggressiveness_column_name in zip(i_agent_pair,
                                                               aggressiveness_column_names)
            ),
            layout=go.Layout(
                **global_layout_template,
                xaxis=dict(
                  **axis_template,
                  title='Generation',
                  range=(0, N_GENERATIONS_SHORT),
                ),
                yaxis=dict(
                  **axis_template,
                  **global_y_axis_template,
                  title=dict(text='Aggressiveness'),
                ),
                showlegend=True,
                legend=dict(
                    xanchor='right', yanchor='middle',
                    y=0.5,
                    font=dict(size=40)
                ),
            ),
        )

        _show_and_or_write_plot(figure, name=f'six_aggressiveness_pair_{i}', context=context)


@plot_deck.command()
@click.argument('mini_trek_path_string')
@click.pass_context
def dh(context, *, mini_trek_path_string: str) -> None:
    assert not context.obj['trek_path_expression']
    mini_trek_path = pathlib.Path(mini_trek_path_string)
    assert mini_trek_path.is_dir()
    mini_trek = trekking.MiniTrek(mini_trek_path)

    print(f'Making a `dh` plot for {mini_trek} ...', file=sys.stderr)

    plot_svg = plotting_dominance_hierarchies.make_condensed_plot_svg(mini_trek.dominance_hierarchy)

    indent = ' ' * 8
    content = constants.HTML_TEMPLATE.format(indent + plot_svg.replace('\n', '\n' + indent))
    if context.obj['write_plot']:
        (pathlib.Path.home() / 'Desktop' / 'dh.html').write_text(content)
    if context.obj['show_plot']:
        with tempfile.NamedTemporaryFile('w', suffix='.html') as fp:
            fp.write(content)
            fp.flush()
            webbrowser.open_new_tab(fp.name)
            time.sleep(3)



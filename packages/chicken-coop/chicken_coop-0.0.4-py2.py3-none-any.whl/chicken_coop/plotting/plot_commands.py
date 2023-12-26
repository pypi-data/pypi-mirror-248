from __future__ import annotations

import random
import re
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

import chicken_coop

from ..command_group import cli
from chicken_coop.county import misc
from chicken_coop.county import trekking
from chicken_coop.county.typing import RealNumber
from .. import utils
from ..dominance_hierarching import DominanceHierarchy
from . import constants


@cli.group()
@click.option('-p', '--path', 'trek_path_expression', type=str, required=False)
@click.pass_context
def plot(context: click.Context, *, trek_path_expression: Optional[str]) -> None:
    context.ensure_object(dict)
    context.obj['trek'] = trekking.Trek.get(trek_path_expression, allow_multi_trek=False)


@plot.command()
@click.option('-s', '--smoothing', type=int, required=False)
@click.pass_context
def plain(context: click.Context, *, smoothing: Optional[int]) -> None:
    import plotly.graph_objects as go
    trek = context.obj['trek']
    (mini_trek,) = trek.mini_treks

    print(f'Making a plot for {mini_trek} ...', file=sys.stderr)
    df = mini_trek.rollout_dataframe
    axis_template = {'title_font': {'size': 23,}, 'tickfont': {'size': 20,}}
    interesting_column_names = tuple(name for name in df.columns if 'agreeability' in name)
    if smoothing is None:
        wrapper = lambda column: column
    else:
        wrapper = lambda column: scipy.signal.savgol_filter(
            np.array(column),
            smoothing, # window size used for filtering
            3, # order of fitted polynomial
        )
    figure = go.Figure(
        data=tuple(
            go.Scatter(x=df.index, y=wrapper(df[interesting_column_name]),
                       name=interesting_column_name)
            for interesting_column_name in interesting_column_names
        ),
        layout=go.Layout(
            title_font_size=28,
            xaxis={**axis_template, 'title': 'Generation'},
            yaxis={**axis_template, 'title': ''},
            legend={#'xanchor': 'right', 'x': 1, 'yanchor': 'bottom',
                    #'y': 0,
                    'font': {'size': 20}}
        )
    )
    figure.show()


@plot.command()
@click.option('-o', '--output', is_flag=True)
@click.pass_context
def dh(context, *, output: bool) -> None:
    import plotly.graph_objects as go
    trek = context.obj['trek']
    (mini_trek,) = trek.mini_treks

    print(f'Making a dominance hierarchy plot for {mini_trek} ...', file=sys.stderr)
    df = mini_trek.rollout_dataframe
    # dominance_hierarchy = DominanceHierarchy(df.iloc[-1]['aggregated_dominance_hierarchy'])
    dominance_hierarchy = DominanceHierarchy(
        '0 => (1 -> 2 -> 3 -> 1) => (4 -> 5 -> 6 -> 4)'
    )
    if output:
        click.echo(dominance_hierarchy.condensed_plot_svg)
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.html') as fp:
            indent = ' ' * 8
            fp.write(
                constants.HTML_TEMPLATE.format(
                    indent + dominance_hierarchy.condensed_plot_svg.replace('\n', '\n' + indent)
                )
            )
            fp.flush()
            webbrowser.open_new_tab(fp.name)
            time.sleep(3)



# @plot.command()
# # @click.option('-p', '--path', 'path_expression', type=str, required=False)
# @click.option('-c', '--color', type=str, default='blue')
# @click.argument('data', type=str)
# @click.pass_context
# def plot_poster_rank_linearity(*, data: str, color: str) -> None:
    # # 0.7910447761194029,0.4925373134328358,0.19402985074626866,0.08955223880597014,0.014925373134328358,0.0,0.0,0.029850746268656716,0.029850746268656716,0.0,0.13432835820895522,0.40298507462686567 --color blue
    # # 1.0,0.8,0.6,0.26666666666666666,0.2,0.2,0.13333333333333333,0.26666666666666666,0.2,0.26666666666666666,0.3333333333333333,0.5333333333333333 --color red
    # import plotly.graph_objects as go
    # print(f'Making a poster rank linearity plot...', file=sys.stderr)
    # rank_legibilities = tuple(map(float, data.split(',')))
    # for rank_linearity in rank_legibilities:
        # assert 0 <= rank_linearity <= 1
    # df = pd.DataFrame(rank_legibilities, columns=('rank_linearity',))
    # axis_template = {'title_font': {'size': 350,}, 'tickfont': {'size': 175,}}
    # figure = go.Figure(
        # data=go.Scatter(
            # x=df.index, y=df['rank_linearity'], name='Rank linearity',
            # mode='lines+markers',
            # line=dict(width=25),
            # marker=dict(
                # color=color,
                # size=125,
            # )
        # ),
        # layout=go.Layout(
            # title_font_size=500,
            # xaxis={**axis_template,
                   # 'title': dict(
                       # text='Social rank',
                       # standoff=150,
                   # ),
                   # 'tickvals': tuple(range(len(rank_legibilities) + 1)),},
            # yaxis={**axis_template,
                   # 'title': dict(
                       # text='Rank linearity',
                       # standoff=150,
                   # ),
                   # 'range': (-0.05, 1.05),
                   # 'tickvals': np.arange(0, 1.1, 0.1),},
            # autosize=False,
            # width=5_000,
            # height=5_000,
            # # legend={#'xanchor': 'right', 'x': 1, 'yanchor': 'bottom',
                    # #'y': 0,
                    # # 'font': {'size': 20}}
        # )
    # )
    # figure.show()



# @plot.command()
# @click.argument('csv_path_string', type=click.Path(exists=True, file_okay=True, dir_okay=False))
# @click.pass_context
# def plot_poster_aggressiveness_animals(*, csv_path_string: str) -> None:
    # import plotly.graph_objects as go
    # print(f'Making a poster animal aggressiveness plot...', file=sys.stderr)
    # df = pd.read_csv(csv_path_string).drop(columns='time_step')
    # axis_template = {'title_font': {'size': 350,}, 'tickfont': {'size': 175,}}
    # figure = go.Figure(
        # data=[
            # go.Scatter(
                # x=df.index, y=df[f'{i + 1}_aggressiveness'], name=f'Agent {i}',
                # mode='lines',
                # line=dict(width=18),
            # ) for i in range(len(df.columns))
        # ],
        # layout=go.Layout(
            # title_font_size=500,
            # xaxis={**axis_template,
                   # 'title': dict(
                       # text='Time',
                       # standoff=150,
                   # )},
            # yaxis={**axis_template,
                   # 'title': dict(
                       # text='Aggressiveness',
                       # standoff=150,
                   # ),
                   # 'range': (-0.05, 1.05),
                   # 'tickvals': np.arange(0, 1.1, 0.1),},
            # autosize=False,
            # width=5_000,
            # height=5_000,
            # legend={'xanchor': 'right',
                    # 'x': 1,
                    # 'yanchor': 'bottom',
                    # 'y': 0.7,
                    # 'entrywidth': 100,
                    # 'entrywidthmode': 'pixels',
                    # 'itemwidth': 100,
                    # 'borderwidth': 0,
                    # 'font': {'size': 100}}
        # )
    # )
    # figure.show()



# @plot.command()
# @click.argument('jsonl_path_string', type=click.Path(exists=True, file_okay=True, dir_okay=False))
# def plot_poster_aggressiveness_ai(*, jsonl_path_string: str) -> None:
    # import plotly.graph_objects as go
    # print(f'Making a poster AI aggressiveness plot...', file=sys.stderr)
    # df = misc.jsonl_to_dataframe(jsonl_path_string, dot_notation=True)
    # df = df[
        # ['generation'] +
        # sorted(filter(re.compile(r'^agent\.[0-9]+\.aggressiveness$').fullmatch,
                      # df.columns))
    # ]
    # axis_template = {'title_font': {'size': 350,}, 'tickfont': {'size': 175,}}
    # figure = go.Figure(
        # data=[
            # go.Scatter(
                # x=df.index, y=df[f'agent.{i}.aggressiveness'], name=f'Agent {i}',
                # mode='lines',
                # line=dict(width=18),
            # ) for i in range(len(df.columns) - 1)
        # ],
        # layout=go.Layout(
            # title_font_size=500,
            # xaxis={**axis_template,
                   # 'title': dict(
                       # text='Time',
                       # standoff=150,
                   # )},
            # yaxis={**axis_template,
                   # 'title': dict(
                       # text='Aggressiveness',
                       # standoff=150,
                   # ),
                   # 'range': (-0.05, 1.05),
                   # 'tickvals': np.arange(0, 1.1, 0.1),},
            # autosize=False,
            # width=5_000,
            # height=5_000,
            # legend={'xanchor': 'right',
                    # 'x': 1,
                    # 'yanchor': 'bottom',
                    # 'y': 0.7,
                    # 'entrywidth': 100,
                    # 'entrywidthmode': 'pixels',
                    # 'itemwidth': 100,
                    # 'borderwidth': 0,
                    # 'font': {'size': 100}}
        # )
    # )
    # figure.show()




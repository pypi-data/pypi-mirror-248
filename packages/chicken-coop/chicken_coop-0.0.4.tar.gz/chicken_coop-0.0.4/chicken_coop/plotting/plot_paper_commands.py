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
def plot_paper(context: click.Context, *, trek_path_expression: Optional[str],
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



@plot_paper.command()
@click.pass_context
def comb_hero(context: click.Context) -> None:

    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False)

    print(f'Making a `comb-hero` plot for {trek} ...', file=sys.stderr)

    mini_treks = [mini_trek for mini_trek in trek.mini_treks
                  if (mini_trek.dominance_hierarchy.is_transitive and
                      mini_trek.dominance_hierarchy.is_complete)]

    dfs = [mini_trek.rankized_rollout_dataframe.filter(regex=r'rank\.[0-9]+\.aggressiveness')
           for mini_trek in mini_treks
           if mini_trek.rollout_dataframe.shape[0] >= N_GENERATIONS_SHORT + 1]
    df: pd.DataFrame = sum(dfs) / len(dfs)
    aggressiveness_column_names = tuple(name for name in df.columns
                                        if 'aggressiveness' in name and 'rank' in name)
    axis_template = global_axis_template | dict(
        title_font=dict(size=50),
        tickfont=dict(
            size=40,
            family='Noto Mono',
        ),
    )

    def make_label(column_name: str) -> str:
        i_rank = re.fullmatch(r'^rank\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Rank {i_rank}'

    figure = plotly.subplots.make_subplots(rows=2, cols=1)


    figure.add_traces(
        _make_chase_scatters(),
        rows=1,
        cols=1,
    )

    figure.update_xaxes(
        **axis_template,
        title_text='Interaction',
        row=1, col=1,
    )
    figure.update_yaxes(
        **axis_template,
        **global_y_axis_template,
        title_text='Aggressiveness',
        row=1, col=1,
    )

    figure.add_traces(
        tuple(
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
        rows=2,
        cols=1,
    )

    figure.update_xaxes(
        **axis_template,
        title_text='Generation',
        range=(0, N_GENERATIONS_SHORT),
        row=2, col=1,
    )
    figure.update_yaxes(
        **axis_template,
        **global_y_axis_template,
        title_text='Aggressiveness',
        row=2, col=1,
    )


    figure.update_layout(
        **global_layout_template | dict(
            height=2_000,
            showlegend=False,
        )
    )

    # for i in figure['layout']['annotations']:
        # i['font'] = dict(size=50)

    _show_and_or_write_plot(figure, name='comb_hero', context=context)


def _make_chase_scatters():
    N_AGENTS = 4
    ATTACKER = 'Attacker'
    VICTIM = 'Victim'
    ATTACK_TYPE = 'Attack Type'
    WINDOW_SIZE = 10

    chase_folder = ANIMAL_DATA_FOLDER / 'Chase2022'
    assert chase_folder.is_dir()

    output_dfs = []

    for csv_path in chase_folder.glob('*.csv'):
        input_df = pd.read_csv(csv_path, usecols=[ATTACKER, VICTIM, ATTACK_TYPE])
        input_df = input_df[input_df[ATTACK_TYPE] != 'J'].drop(columns=ATTACK_TYPE)

        fluffs = collections.defaultdict(list)
        gruffs = []

        for _, row in input_df.iterrows():
            fluffs[row[ATTACKER]].append(1)
            fluffs[row[VICTIM]].append(0)
            gruffs.append([misc.mean_default(items) if (items := fluffs[i][-WINDOW_SIZE:]) else None
                           for i in range(1, N_AGENTS + 1)])

        while None in gruffs[0]:
            del gruffs[:1]

        wip_df = pd.DataFrame(gruffs, columns=[f'agent_{i}_aggressiveness'
                                               for i in range(1, N_AGENTS + 1)])
        foo = dict(wip_df.mean())
        column_by_rank = tuple(sorted(foo, key=foo.__getitem__, reverse=True))
        output_df = pd.DataFrame({f'rank.{i}.aggressiveness': wip_df[column]
                                  for i, column in enumerate(column_by_rank)})
        output_dfs.append(output_df)

    final_df = sum(output_dfs)[:240] / len(output_dfs)

    aggressiveness_column_names = tuple(name for name in final_df.columns
                                        if 'aggressiveness' in name and 'rank' in name)

    def make_label(column_name: str) -> str:
        i_rank = re.fullmatch(r'^rank\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Rank {i_rank}'

    chase_scatters = tuple(
            go.Scatter(
                x=final_df.index, y=final_df[aggressiveness_column_name],
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
        )
    return chase_scatters


@plot_paper.command()
@click.pass_context
def samples_aggressiveness(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False)

    forgive_lack_of_samples = context.obj['forgive_lack_of_samples']

    print(f'Making a `samples-aggressiveness` plot for {trek} ...', file=sys.stderr)

    dfs = [mini_trek.rollout_dataframe.filter(regex=r'agent\.[0-9]+\.aggressiveness')
           for mini_trek in
           trek.get_sample_mini_treks(forgive_lack_of_samples=forgive_lack_of_samples)]
    aggressiveness_column_names = tuple(name for name in dfs[0].columns
                                        if 'aggressiveness' in name and 'agent' in name)
    axis_template = global_axis_template | dict(
        linewidth=2,
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    def make_label(column_name: str) -> str:
        i_agent = re.fullmatch(r'^agent\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Agent {i_agent}'

    subplots = []

    for df in dfs:
        subplots.append(
            tuple(
                go.Scatter(x=df.index, y=df[aggressiveness_column_name],
                           name=make_label(aggressiveness_column_name),
                           line=dict(width=4.5, color=plotly.colors.DEFAULT_PLOTLY_COLORS[i]))
                for i, aggressiveness_column_name in enumerate(aggressiveness_column_names)
            )
        )
    figure = plotly.subplots.make_subplots(
        rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
        horizontal_spacing=0.035,
        vertical_spacing=0.05,
        x_title='Generation',
        y_title='Aggressiveness',
    )

    axis_title_font_size = 55
    x_title, y_title = figure['layout']['annotations']
    x_title['font'] = y_title['font'] = dict(size=axis_title_font_size)
    x_title['yshift'] -= 10
    y_title['xshift'] -= 40

    for i, subplot in enumerate(subplots):
        figure.add_traces(subplot, rows=(1, 2)[i // 2], cols=[1, 2][i % 2])

    figure.update_layout(
        **global_layout_template,
        showlegend=False,
        margin=dict(l=140, b=100, t=10),
    )
    figure.update_xaxes(**axis_template, range=(0, N_GENERATIONS_SHORT))
    figure.update_yaxes(**axis_template, **global_y_axis_template)

    _show_and_or_write_plot(figure, name='samples_aggressiveness', context=context)


@plot_paper.command()
@click.pass_context
def samples_rapport(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False)

    forgive_lack_of_samples = context.obj['forgive_lack_of_samples']

    print(f'Making a `samples-rapport` plot for {trek} ...', file=sys.stderr)

    column_pattern = re.compile(r'^dialog\.([0-9]+)\.([0-9]+)\.rapport$')
    dfs = [mini_trek.rollout_dataframe.filter(regex=column_pattern.pattern)
           for mini_trek in
           trek.get_sample_mini_treks(forgive_lack_of_samples=forgive_lack_of_samples)]

    minimum_dfs = [pd.DataFrame({'Minimum rapport': df.min(axis=1)}) for df in dfs]

    axis_template = global_axis_template | dict(
        linewidth=2,
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    figure = plotly.subplots.make_subplots(
        rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
        horizontal_spacing=0.035,
        vertical_spacing=0.05,
        x_title='Generation',
        y_title='Minimum rapport',
    )

    axis_title_font_size = 55
    x_title, y_title = figure['layout']['annotations']
    x_title['font'] = y_title['font'] = dict(size=axis_title_font_size)
    x_title['yshift'] -= 10
    y_title['xshift'] -= 40

    for i, minimum_df in enumerate(minimum_dfs):
        figure.add_traces(
            go.Scatter(x=minimum_df.index, y=minimum_df.iloc[:, 0],
                       name=minimum_df.columns[0],
                       line=dict(width=4.5, color='black')),
            rows=(1, 2)[i // 2],
            cols=[1, 2][i % 2]
        )

    figure.update_layout(
        **global_layout_template,
        showlegend=False,
        margin=dict(l=140, b=100, t=10),
    )
    figure.update_xaxes(**axis_template)
    figure.update_yaxes(**axis_template, **global_y_axis_template)

    _show_and_or_write_plot(figure, name='samples_rapport', context=context)


@plot_paper.command()
@click.pass_context
def samples_dh(context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False)

    forgive_lack_of_samples = context.obj['forgive_lack_of_samples']

    print(f'Making a `samples-dh` plot for {trek} ...', file=sys.stderr)

    dominance_hierarchies = [
        mini_trek.dominance_hierarchy for mini_trek in
        trek.get_sample_mini_treks(forgive_lack_of_samples=forgive_lack_of_samples)
    ]

    plot_svg = plotting_dominance_hierarchies.make_condensed_plot_svg(dominance_hierarchies)

    indent = ' ' * 8
    content = constants.HTML_TEMPLATE.format(indent + plot_svg.replace('\n', '\n' + indent))
    if context.obj['write_plot']:
        (pathlib.Path.home() / 'Desktop' / 'samples_dh.html').write_text(content)
    if context.obj['show_plot']:
        with tempfile.NamedTemporaryFile('w', suffix='.html') as fp:
            fp.write(content)
            fp.flush()
            webbrowser.open_new_tab(fp.name)
            time.sleep(3)


@plot_paper.command()
@click.pass_context
def ablate_observation_rapport(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False,
                             moniker='paper-ablate-observation')


    print(f'Making an `ablate-observation-rapport` plot for {trek} ...', file=sys.stderr)
    mini_treks_by_observation_accuracy = trek.get_mini_treks_grouped_by(
        lambda mini_trek: mini_trek.meta['coop_config']['observation_accuracy']
    )
    assert set(mini_treks_by_observation_accuracy) == {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                                                       0.9, 1.0}

    df_by_observation_accuracy = {}

    for observation_accuracy, mini_treks in mini_treks_by_observation_accuracy.items():
        serieses = [mini_trek.rollout_dataframe['population.rapport'] for mini_trek in mini_treks
                    if mini_trek.rollout_dataframe.shape[0] >= N_GENERATIONS_LONG + 1]
        df_by_observation_accuracy[observation_accuracy] = pd.concat(serieses, axis=1
                                                             ).mean(axis=1).to_frame(name='rapport')

    axis_template = global_axis_template | dict(
        title_font=dict(size=50),
        tickfont=dict(
            size=40,
            family='Noto Mono',
        ),
    )

    figure = go.Figure(
        data=tuple(
            go.Scatter(x=df.index, y=df['rapport'],
                       name=str(observation_accuracy),
                       line=dict(
                           width=5.5,
                           color=plotly.colors.sample_colorscale(BLUE_TO_RED,
                                                                 [observation_accuracy])[0]
                       ))
            for observation_accuracy, df in df_by_observation_accuracy.items()
        ),
        layout=go.Layout(
            **global_layout_template,
            xaxis=dict(
              **axis_template,
              title='Generation',
              range=(0, N_GENERATIONS_LONG),
            ),
            yaxis=dict(
              **axis_template,
              **global_y_axis_template,
              title=dict(text='Rapport', standoff=0),
            ),
            legend=dict(
                xanchor='left', yanchor='top',
                x=-0.25, y=1,
                traceorder='reversed',
                font=dict(size=40)
                ),
            annotations=(
                go.layout.Annotation(
                    text='Opponent perception accuracy',
                    xref='paper', yref='paper',
                    # x=-0.79, y=0.5,
                    x=-0.27, y=0.5,
                    xanchor='center',
                    yanchor='middle',
                    textangle=-90,
                    font=dict(
                        size=50,
                    ),
                ),
            ),
            margin=dict(l=400),
        ),
    )
    _show_and_or_write_plot(figure, name='ablate_observation_rapport', context=context)


@plot_paper.command()
@click.option('-o', '--output', is_flag=True)
@click.pass_context
def ablate_observation_samples_aggressiveness(context, *, output: bool) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False,
                             moniker='paper-ablate-observation')

    dfs = [mini_trek.rollout_dataframe.filter(regex=r'agent\.[0-9]+\.aggressiveness')
           for mini_trek in
           trek.get_mini_treks_grouped_by(
               lambda mini_trek: mini_trek.meta['coop_config']['observation_accuracy'])[0.1][:4]]
    assert len(dfs) == 4

    aggressiveness_column_names = tuple(name for name in dfs[0].columns
                                        if 'aggressiveness' in name and 'agent' in name)
    axis_template = global_axis_template | dict(
        linewidth=2,
        tickfont=dict(
            size=35,
            family='Noto Mono',
        ),
    )

    def make_label(column_name: str) -> str:
        i_agent = re.fullmatch(r'^agent\.([0-9]+)\.aggressiveness$', column_name).group(1)
        return f'Agent {i_agent}'

    subplots = []

    for df in dfs:
        subplots.append(
            tuple(
                go.Scatter(x=df.index, y=df[aggressiveness_column_name],
                           name=make_label(aggressiveness_column_name),
                           line=dict(width=4.5, color=plotly.colors.DEFAULT_PLOTLY_COLORS[i]))
                for i, aggressiveness_column_name in enumerate(aggressiveness_column_names)
            )
        )
    figure = plotly.subplots.make_subplots(
        rows=2, cols=2, shared_xaxes=True, shared_yaxes=True,
        horizontal_spacing=0.035,
        vertical_spacing=0.05,
        x_title='Generation',
        y_title='Aggressiveness',
    )

    axis_title_font_size = 55
    x_title, y_title = figure['layout']['annotations']
    x_title['font'] = y_title['font'] = dict(size=axis_title_font_size)
    x_title['yshift'] -= 10
    y_title['xshift'] -= 40

    for i, subplot in enumerate(subplots):
        figure.add_traces(subplot, rows=(1, 2)[i // 2], cols=[1, 2][i % 2])

    figure.update_layout(
        **global_layout_template,
        showlegend=False,
        margin=dict(l=140, b=100, t=10),
    )
    figure.update_xaxes(**axis_template, range=(0, N_GENERATIONS_SHORT))
    figure.update_yaxes(**axis_template, **global_y_axis_template)

    _show_and_or_write_plot(figure, name='ablate_observation_samples_aggressiveness',
                            context=context)


@plot_paper.command()
@click.pass_context
def transmit(context: click.Context) -> None:
    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False,
                             moniker='paper-transplant')

    print(f'Making a `transmit` plot for {trek} ...', file=sys.stderr)
    mini_treks_by_n_visitor_agents = trek.get_mini_treks_grouped_by(
        lambda mini_trek: len(mini_trek.meta['coop_config']['i_visitor_agents'])
    )

    df_by_n_visitor_agents = {}

    for n_visitor_agents, mini_treks in sorted(mini_treks_by_n_visitor_agents.items()):
        df_by_n_visitor_agents[n_visitor_agents] = pd.DataFrame(
            [1 - mini_trek.rollout_dataframe['population.'
                             'restricted_distance_from_visitor_dominance_hierarchy'].tail(1).iloc[0]
             for mini_trek in mini_treks],
            columns=('transmission_fidelidy',),
        )

    axis_template = global_axis_template | dict(
        title_font=dict(size=50),
        tickfont=dict(
            size=40,
            family='Noto Mono',
        ),
    )

    figure = go.Figure(
        data=tuple(
            go.Box(
                x=[n_visitor_agents] * len(df['transmission_fidelidy']),
                y=df['transmission_fidelidy'],
                name=str(n_visitor_agents),
                marker=dict(
                    color='black',
                ),
                # notched=True,
                showwhiskers=False,
                boxpoints=False,
                quartilemethod='exclusive',
                # boxmean=True,
                line=dict(width=4,),
            ) for n_visitor_agents, df in df_by_n_visitor_agents.items()
        ) + tuple(
            go.Scatter(
                x=[n_visitor_agents],
                y=[df['transmission_fidelidy'].median()],
                name=str(n_visitor_agents),
                marker=dict(
                    color='white',
                    size=60,
                    line=dict(
                        width=4,
                        color='black',
                    )
                )
            ) for n_visitor_agents, df in df_by_n_visitor_agents.items()
        )
        ,
        layout=go.Layout(
            **global_layout_template,
            xaxis=dict(
              **axis_template,
              title='Number of experienced agents',
            ),
            yaxis=axis_template | global_y_axis_template | dict(
              title_font=dict(size=47),
              title=dict(text='Dominance hierarchy transmission fidelidy'),
            ),
            showlegend=False,
        ),
    )
    _show_and_or_write_plot(figure, name='transmit', context=context)


@plot_paper.command()
@click.pass_context
def non_linearity(context: click.Context) -> None:

    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False,
                             moniker='paper-cycles')

    print(f'Making a `non-linearity` plot for {trek} ...', file=sys.stderr)

    def mouse_string_to_i_agent(agent_string: str) -> int:
        i_agent_plus_one = int(re.fullmatch('^M([0-9]+)$', agent_string).group(1))
        assert agent_string == f'M{i_agent_plus_one}'
        return i_agent_plus_one - 1

    def csv_path_to_dominance_hierarchy(path: pathlib.Path) -> DominanceHierarchy:
        df = pd.read_csv(path, index_col=0)

        edges = []

        for i in range(df.shape[0]):
            for j in range(i+1, df.shape[1]): # We start from i+1 to avoid repeating pairs
                agent_a = df.index[i]
                agent_b = df.columns[j]

                a_wins = df.at[agent_a, agent_b]
                b_wins = df.at[agent_b, agent_a]

                if pd.isna(a_wins) or pd.isna(b_wins):
                    assert pd.isna(a_wins) and pd.isna(b_wins)
                    assert agent_a == agent_b
                    continue
                assert agent_a != agent_b

                if a_wins >= b_wins:
                    edges.append((mouse_string_to_i_agent(agent_a),
                                  mouse_string_to_i_agent(agent_b)))
                else:
                    assert b_wins > a_wins
                    edges.append((mouse_string_to_i_agent(agent_b),
                                  mouse_string_to_i_agent(agent_a)))

        return DominanceHierarchy(edges)

    williamson_folder = ANIMAL_DATA_FOLDER / 'Williamson2017'

    csv_paths = tuple(williamson_folder.glob('*.csv'))

    mice_dominance_hierarchies = tuple(map(csv_path_to_dominance_hierarchy, csv_paths))
    mice_mean_rank_legibilities = \
                             DominanceHierarchy.get_mean_rank_linearity(mice_dominance_hierarchies)


    dominance_hierarchies = tuple(mini_trek.dominance_hierarchy for mini_trek in trek.mini_treks
                                  if mini_trek.dominance_hierarchy.is_complete)

    mean_rank_legibilities = DominanceHierarchy.get_mean_rank_linearity(dominance_hierarchies)

    df = pd.DataFrame({'mice_rank_linearity': mice_mean_rank_legibilities,
                       'chicken_coop_rank_linearity': mean_rank_legibilities})

    axis_template = global_axis_template | dict(
        title_font=dict(size=50),
        tickfont=dict(
            size=40,
            family='Noto Mono',
        ),
    )

    figure = go.Figure(
        data=(
            go.Scatter(
                x=df.index,
                y=df['mice_rank_linearity'],
                name='Male CD-1 mice',
                mode='lines+markers',
                line=dict(
                    color='orange',
                    width=6,
                ),
                marker=dict(
                    size=13,
                )
            ),
            go.Scatter(
                x=df.index,
                y=df['chicken_coop_rank_linearity'],
                name='Chicken Coop agents',
                mode='lines+markers',
                line=dict(
                    color='purple',
                    width=6,
                ),
                marker=dict(
                    size=13,
                )
            ),
        )
        ,
        layout=go.Layout(
            **global_layout_template,
            xaxis=dict(
              **axis_template,
              title='Rank',
              dtick=1,
            ),
            yaxis=dict(
              **axis_template,
              **global_y_axis_template,
              title=dict(text='Rank linearity'),
            ),
            showlegend=True,
            legend=dict(
                xanchor='right', yanchor='top',
                font=dict(size=40)
            ),
        ),
    )
    _show_and_or_write_plot(figure, name='non_linearity', context=context)



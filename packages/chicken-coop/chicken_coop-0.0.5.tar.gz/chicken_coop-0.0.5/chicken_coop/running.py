from __future__ import annotations

import os
from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, Sequence
import pathlib
import inspect
import copy
import enum
import yaml
import datetime as datetime_module
import statistics
import pickle
import base64
import time
import abc
import lzma
import logging
import functools
import collections
import sys
import operator
import dataclasses
import functools
import itertools
import numbers
import pprint
import random
import re
import string
import contextlib

import more_itertools
import ray.rllib.env.multi_agent_env
import ray.rllib.algorithms.callbacks
from ray.rllib.utils.typing import PolicyID, MultiAgentDict, ModelWeights
from ray.rllib import algorithms
import ray.tune
import ray.rllib.algorithms.ppo
import gymnasium
import gymnasium.spaces
import numpy as np
import pysnooper
import click

from chicken_coop import county
from chicken_coop.county.thready_krueger import ThreadyKrueger
from chicken_coop.county import misc
from chicken_coop.county import trekking
from chicken_coop.county import csv_tools
from chicken_coop.county import policing
import chicken_coop
from chicken_coop.county.typing import Agent, RealNumber
from .zeitgeisting import Zeitgeist
from .stating import State
from .enving import Env
from . import defaults
from chicken_coop.coop_config import CoopConfig
from . import utils
from .callbackino import Callbackino

from .command_group import cli



def rollout_from_tune(config: dict[str, Any]) -> None:

    pure_config = {}
    coop_config_dict = {}
    config_arguments = set(inspect.signature(CoopConfig).parameters)
    for key, value in config.items():
        if key in config_arguments:
            coop_config_dict[key] = value
        else:
            pure_config[key] = value

    coop_config = CoopConfig(**coop_config_dict)
    return rollout(**pure_config, coop_config=coop_config,
                  trial_folder=pathlib.Path(ray.tune.get_trial_dir()),
                  report_to_tune=True, write_stdout_to_stdout=False)

def rollout(coop_config: CoopConfig, *,
            trial_folder: Optional[pathlib.Path] = None,
            report_to_tune: bool = False,
            write_stdout_to_stdout: bool = True,
            raw_visitor_policies: tuple[tuple[str, os.PathLike], ...] = (),
            argv: Optional[Iterable[str]] = None,
            ) -> None:

    trial_folder = trial_folder or pathlib.Path(ray.tune.get_trial_dir())

    samples_folder = trial_folder / 'samples'
    samples_folder.mkdir(parents=True, exist_ok=True)

    policy_snapshots_folder = trial_folder / 'policy_snapshots'
    policy_snapshots_folder.mkdir(parents=True, exist_ok=True)

    output_path: pathlib.Path = trial_folder / 'output.txt'
    reporters = [county.misc.JsonlRolloutReporter(trial_folder / 'rollout.jsonl')]

    if report_to_tune:
        reporters.append(county.misc.TuneRolloutReporter())

    if raw_visitor_policies:
        (visitor_mini_trek,) = {trekking.MiniTrek.get(policy_path)
                                for _, policy_path in raw_visitor_policies}
        visitor_policy_snapshot_by_policy_name = {
            policy_name: policing.PolicySnapshot.uncompickle_from_bytes(policy_path.read_bytes())
            for policy_name, policy_path in raw_visitor_policies
        }
        visitor_dominance_hierarchy = visitor_mini_trek.dominance_hierarchy
        assert visitor_dominance_hierarchy.is_complete

    else: # not raw_visitor_policies
        visitor_mini_trek = None
        visitor_dominance_hierarchy = \
                                   chicken_coop.DominanceHierarchy.get_trivial(coop_config.n_agents)
        visitor_policy_snapshot_by_policy_name = {}

    coop_config = dataclasses.replace(
        coop_config, visitor_dominance_hierarchy=visitor_dominance_hierarchy,
        i_visitor_agents=tuple(map(misc.get_int_from_mixed_string,
                                   visitor_policy_snapshot_by_policy_name)),
    )

    env = Env({'coop_config': coop_config})

    algorithm_config = (
        algorithms.ppo.PPOConfig()
        .training(
            train_batch_size=coop_config.train_batch_size,
            lr=coop_config.learning_rate,
        )
        .resources(
            num_gpus=0,
            num_gpus_per_worker=0,
        )
        .environment(
            env=Env,
            env_config=env.config,
            disable_env_checking=True,
        )
        .rollouts(
            create_env_on_local_worker=True,
            num_rollout_workers=coop_config.n_rollout_workers,
        )
        .reporting(
            keep_per_episode_custom_metrics=True,
        )
        .callbacks(
            Callbackino,
        )
        .multi_agent(
            policies={policy_name: ray.rllib.policy.policy.PolicySpec()
                      for policy_name in env.policies},
            policy_mapping_fn=coop_config.policy_mapping_fn,
            policies_to_train=tuple(
                policy_name for policy_name in env.policies if
                (not coop_config.freeze_visitors) or
                policy_name not in visitor_policy_snapshot_by_policy_name
            ),
        )
    )

    algorithm = algorithm_config.build()

    for visitor_policy_name, visitor_policy_snapshot in \
                                             visitor_policy_snapshot_by_policy_name.items():
        visitor_policy_snapshot.transplant_to_algorithm(algorithm, visitor_policy_name)


    if coop_config.flip_initial_weights:
        flipped_culture_snapshot = - policing.CultureSnapshot.import_from_algorithm(algorithm)
        flipped_culture_snapshot.transplant_to_algorithm(algorithm)

    # base_agentwise_measures = ('aggressiveness',)
    # simple_measure_fields = ()
    # simple_fields = ('generation', 'episode_reward', 'datetime')
    # agentwise_measure_fields = tuple(f'{agent}_{base_measure}' for agent in
                                     # self.coop_config.policy_by_agent for base_measure in
                                     # base_agentwise_measures)

    with (trial_folder / 'meta.yaml').open('w') as yaml_file:
        yaml.dump(
            {
                'coop_config': coop_config.get_nice_dict(for_yaml=True),
                'chicken_coop_repo_commit': county.misc.get_chicken_coop_repo_commit(),
                'chicken_coop_repo_is_clean': county.misc.get_chicken_coop_repo_is_clean(),
                'observation_fields': list(env.observation_space.keys()),
                'algorithm_class': type(algorithm).__name__,
                'raw_visitor_policies': {visitor_policy_name: str(visitor_policy_path) for
                                         visitor_policy_name, visitor_policy_path in
                                         raw_visitor_policies},
                'argv': sys.argv if argv is None else argv,
            },
            yaml_file,
            Dumper=misc.ListifyingDumper,
        )


    with contextlib.ExitStack() as exit_stack:
        if write_stdout_to_stdout:
            exit_stack.enter_context(county.misc.tee_stdout(output_path))
            stream = sys.stdout
        else:
            stream = exit_stack.enter_context(output_path.open('w'))

        zeitgeists = []

        for i_generation in range(coop_config.n_generations + 1):
            if i_generation == 0:
                # For fast failure in case there's a bug in `Callbackino`:
                Callbackino().on_train_result(algorithm=algorithm, result={})
            (samples_folder / f'{i_generation:04d}').write_text(
                Env.sample_episode_to_text(algorithm, coop_config=coop_config)
            )
            if (i_generation % coop_config.policy_snapshot_period == 0 or
                                                        i_generation == coop_config.n_generations):
                policy_snapshots_subfolder = (policy_snapshots_folder / f'{i_generation:04d}')
                policy_snapshots_subfolder.mkdir()
                culture_snapshot = policing.CultureSnapshot.import_from_algorithm(algorithm)
                for policy_name, policy_snapshot in culture_snapshot.items():
                    (policy_snapshots_subfolder / policy_name).write_bytes(
                                                               policy_snapshot.compickle_to_bytes())

            # generation_is_mature = i_generation >= 0.8 * n_generations
            if i_generation == 0:
                results = algorithm.evaluate()['evaluation']
            else:
                results = algorithm.train()
            from_array = lambda a_: Zeitgeist.from_array(a_, coop_config)
            zeitgeist = Zeitgeist.sum(
                map(from_array, results['custom_metrics']['zeitgeist_array'])
            )
            zeitgeists.append(zeitgeist)
            stream.write(f'Generation: {algorithm.iteration:04d}  '
                         f'Reward: {zeitgeist.population_portrait.reward:04.2f}\n')
            report = {
                'generation': algorithm.iteration,
                'datetime': datetime_module.datetime.now().isoformat(),
                'aggregated_dominance_hierarchy': (Zeitgeist.sum(zeitgeists[-5:]).
                                                           population_portrait.dominance_hierarchy),
                **zeitgeist.output,
            }
            for reporter in reporters:
                reporter.report(report)

    # Clean heavy files we don't need:
    for path in itertools.chain(trial_folder.glob('events.out.tfevents*'),
                                ((trial_folder / 'result.json'),)):
        path.unlink(missing_ok=True)


@cli.command()
@click.option('--moniker', type=str, default=None)
@click.option('-t', '--use-tune', is_flag=True, show_default=True)
@click.option('--n-tune-samples', type=int, default=defaults.DEFAULT_N_TUNE_SAMPLES,
              show_default=True)
@click.option('--visitor-policy', 'raw_visitor_policies',
              type=(str, click.Path(exists=True, dir_okay=False, resolve_path=True,
                                    path_type=pathlib.Path)),
              multiple=True, show_default=True)
@CoopConfig.add_options_to_click_command()
def run(*, moniker: Optional[str], use_tune: bool, n_tune_samples: int,
        raw_visitor_policies: tuple[tuple[str, str], ...], **raw_coop_config_kwargs) -> None:
    '''Run the Chicken Coop environment and train the agents.'''
    with trekking.Trek.create(extra_meta={'command': 'run', 'moniker': moniker}) as trek:
        county.init_ray()

        coop_config_kwargs = {}
        for key, values in raw_coop_config_kwargs.items():
            if not values:
                continue
            elif len(values) == 1:
                (value,) = values
                coop_config_kwargs[key] = value
            else:
                assert len(values) >= 2
                if not use_tune:
                    raise click.UsageError
                coop_config_kwargs[key] = ray.tune.grid_search(values)


        if use_tune:
            experiment = ray.tune.Experiment(
                name='chicken-coop',
                run=rollout_from_tune,
                config={
                    **coop_config_kwargs,
                    'raw_visitor_policies': raw_visitor_policies,
                    'argv': sys.argv,
                },
                num_samples=n_tune_samples,
                storage_path=str(tune_folder := trek.folder / 'tune_rollouts'),
                log_to_file=('stdout', 'stderr'),
                resources_per_trial=ray.tune.PlacementGroupFactory(
                    [{'CPU': 1.0}] + [{'CPU': 1.0}] * 2
                ),
            )
            experiment.dir_name = tune_folder

            analysis = ray.tune.run(experiment)
            df = misc.get_mean_dataframe_from_experiment_analysis(analysis)
            df.to_csv(trek.folder / 'tune_analysis.csv')

        else:
            rollout(coop_config=CoopConfig(**coop_config_kwargs),
                    raw_visitor_policies=raw_visitor_policies,
                    trial_folder=(trek.folder / 'rollout'))


@cli.command()
@click.option('--moniker', type=str, default=None)
@click.option('--visitor-trek', 'visitor_trek_path_string',
              type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True,
                              path_type=pathlib.Path),
              show_default=True)
@click.option('--n-visitor-populations-per-n-visitor-agents', type=int,
              default=defaults.DEFAULT_N_VISITOR_POPULATIONS_PER_N_VISITOR_AGENTS,
              show_default=True)
@click.option('--n-transplants-per-visitor-population', type=int,
              default=defaults.DEFAULT_N_TRANSPLANTS_PER_VISITOR_POPULATION,
              show_default=True)
@CoopConfig.add_options_to_click_command(defaults={'learning_rate': (float(2e-05),),
                                                   'n_generations': (35,),
                                                   'train_batch_size': (256,),})
def transplant(*, moniker: Optional[str], visitor_trek_path_string: str,
               n_visitor_populations_per_n_visitor_agents: int,
               n_transplants_per_visitor_population: int, **raw_coop_config_kwargs) -> None:
    '''Transplant experienced agents into naive populations.'''
    with trekking.Trek.create(extra_meta={'command': 'transplant', 'moniker': moniker}) as trek:
        county.init_ray()

        visitor_trek = trekking.Trek.get(visitor_trek_path_string, allow_single_trek=False)

        coop_config_kwargs = {}
        for key, values in raw_coop_config_kwargs.items():
            if not values:
                continue
            elif len(values) == 1:
                (value,) = values
                coop_config_kwargs[key] = value
            else:
                assert len(values) >= 2
                raise NotImplementedError("Grid search isn't implemented for `transplant`.")

        visitor_mini_treks = tuple(
            more_itertools.islice_extended(
                (visitor_mini_trek for visitor_mini_trek in visitor_trek.mini_treks
                 if visitor_mini_trek.dominance_hierarchy.is_complete),
                n_visitor_populations_per_n_visitor_agents
            )
        )
        assert len(visitor_mini_treks) == n_visitor_populations_per_n_visitor_agents
        fluff = []
        n_agents = CoopConfig(**coop_config_kwargs).n_agents
        for n_visitor_agents in range(n_agents - 1):
            for visitor_mini_trek in visitor_mini_treks:
                visitor_mini_trek: trekking.MiniTrek
                assert len(visitor_mini_trek.policy_path_by_name) == n_agents
                fluff.extend(
                    misc.get_wacky_choices(visitor_mini_trek.policy_path_by_name.items(),
                                           n=n_visitor_agents, k=n_transplants_per_visitor_population)
                )


        assert len(fluff) == ((n_agents - 1) * n_transplants_per_visitor_population *
                              n_visitor_populations_per_n_visitor_agents)
        assert set(collections.Counter(map(len, fluff)).values()) == \
                 {n_visitor_populations_per_n_visitor_agents * n_transplants_per_visitor_population}
        assert len(fluff[0]) == 0
        # Easing troubleshooting by making the first runs not be degenerate cases:
        for _ in range(100):
            if set(map(len, fluff[:4])) & {0, n_agents}:
                random.shuffle(fluff)
            else:
                break
        else:
            raise Exception
        raw_visitor_policies_grid_search = ray.tune.grid_search(fluff)


        experiment = ray.tune.Experiment(
            name='chicken-coop',
            run=rollout_from_tune,
            config={
                **coop_config_kwargs,
                'raw_visitor_policies': raw_visitor_policies_grid_search,
                'argv': sys.argv,
            },
            num_samples=1,
            storage_path=str(tune_folder := trek.folder / 'tune_rollouts'),
            log_to_file=('stdout', 'stderr'),
            resources_per_trial=ray.tune.PlacementGroupFactory(
                [{'CPU': 1.0}] + [{'CPU': 1.0}] * 2
            ),
        )
        experiment.dir_name = tune_folder

        analysis = ray.tune.run(experiment)

        df = misc.get_mean_dataframe_from_experiment_analysis(
            analysis,
        )

        df.to_csv(trek.folder / 'tune_analysis.csv')



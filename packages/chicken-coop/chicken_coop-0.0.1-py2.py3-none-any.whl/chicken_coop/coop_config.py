from __future__ import annotations

from typing import (Tuple, Optional, Dict, Mapping, Iterable, Any, Sequence, Callable, Hashable,
                    Callable)
import typing
import pathlib
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
from chicken_coop.county import csv_tools
from chicken_coop.county import policing
import chicken_coop
from chicken_coop.county.typing import Agent, RealNumber
from . import defaults
from .dominance_hierarching import DominanceHierarchy


@dataclasses.dataclass(kw_only=True, repr=False)
class CoopConfig:

    victory_reward: RealNumber = defaults.DEFAULT_VICTORY_REWARD
    boredom_reward: RealNumber = defaults.DEFAULT_BOREDOM_REWARD
    defeat_reward: RealNumber = defaults.DEFAULT_DEFEAT_REWARD
    anguish_reward: RealNumber = defaults.DEFAULT_ANGUISH_REWARD

    episode_length: RealNumber = defaults.DEFAULT_EPISODE_LENGTH
    identity_is_linear: bool = defaults.DEFAULT_IDENTITY_IS_LINEAR
    n_agents: int = defaults.DEFAULT_N_AGENTS
    n_generations: int = defaults.DEFAULT_N_GENERATIONS
    train_batch_size: int = defaults.DEFAULT_TRAIN_BATCH_SIZE
    learning_rate: RealNumber = defaults.DEFAULT_LEARNING_RATE
    n_rollout_workers: int = defaults.DEFAULT_N_ROLLOUT_WORKERS
    policy_snapshot_period: int = defaults.DEFAULT_POLICY_SNAPSHOT_PERIOD
    flip_initial_weights: bool = defaults.DEFAULT_FLIP_INITIAL_WEIGHTS
    dominance_hierarchy_polarity_threshold: float = \
                                          defaults.DEFAULT_DOMINANCE_RELATIONSHIP_POLARITY_THRESHOLD
    observation_accuracy: float = defaults.DEFAULT_OBSERVATION_ACCURACY
    i_visitor_agents: tuple[int, ...] = ()
    visitor_dominance_hierarchy: Optional[DominanceHierarchy] = None
    freeze_visitors: bool = defaults.DEFAULT_FREEZE_VISITORS


    def __post_init__(self) -> None:
        self.i_agents = tuple(range(self.n_agents))
        self.i_agent_pairs_full = tuple(itertools.product(self.i_agents, repeat=2))
        self.i_agent_pairs_increasing = tuple(itertools.combinations(self.i_agents, 2))
        self.i_agent_pairs_decreasing = tuple(
            sorted(map(tuple, (map(reversed, itertools.combinations(self.i_agents, 2)))))
        )
        self.i_agent_pairs_diagonal = tuple(zip(self.i_agents, self.i_agents, strict=True))
        self.i_agent_pairs_without_diagonal = tuple(itertools.permutations(self.i_agents, 2))
        self.i_resident_agents = tuple(i_agent for i_agent in self.i_agents
                                       if i_agent not in self.i_visitor_agents)

        self.pad_i_agent = lambda i_agent: str(i_agent).rjust(len(str(self.n_agents)), '0')
        self.policy_by_agent = {f'agent_{self.pad_i_agent(i)}': f'policy_{self.pad_i_agent(i)}'
                                for i in self.i_agents}


        ### Validating: ############################################################################
        #                                                                                          #
        assert len({self.victory_reward, self.boredom_reward, self.defeat_reward,
                    self.anguish_reward}) == 4
        assert self.n_agents % 2 == 0
        assert set(self.i_visitor_agents) <= set(self.i_agents)
        assert more_itertools.is_sorted(self.i_visitor_agents)

        assert all(
            map(more_itertools.is_sorted,
                (self.i_agent_pairs_full, self.i_agent_pairs_increasing,
                 self.i_agent_pairs_decreasing, self.i_agent_pairs_diagonal,
                 self.i_agent_pairs_without_diagonal)
            )
        )
        assert set(self.i_agent_pairs_full) == (
            set(self.i_agent_pairs_increasing) | set(self.i_agent_pairs_decreasing) |
            set(self.i_agent_pairs_diagonal)
        ) == (
            set(self.i_agent_pairs_diagonal) | set(self.i_agent_pairs_without_diagonal)
        )
        assert not (set(self.i_agent_pairs_diagonal) & set(self.i_agent_pairs_without_diagonal))
        assert set(self.i_agent_pairs_without_diagonal) == (set(self.i_agent_pairs_increasing) |
                                                            set(self.i_agent_pairs_decreasing))
        assert not (set(self.i_agent_pairs_increasing) & set(self.i_agent_pairs_decreasing))
        assert not (set(self.i_agent_pairs_increasing) & set(self.i_agent_pairs_diagonal))
        assert not (set(self.i_agent_pairs_diagonal) & set(self.i_agent_pairs_decreasing))
        #                                                                                          #
        ### Finished validating. ###################################################################

    def policy_mapping_fn(self,
                          agent_id: Agent,
                          episode: Optional[ray.rllib.evaluation.episode.Episode] = None,
                          worker: Optional[ray.rllib.evaluation.rollout_worker.
                                           RolloutWorker] = None,
                          **kwargs) -> PolicyID:
        return self.policy_by_agent[agent_id]

    def get_nice_dict(self, *, for_yaml: bool = False) -> dict[str, Any]:
        keys = tuple(key for key in vars(self) if not key.startswith('_') and
                     not key.startswith('i_agent_pairs') and key != 'pad_i_agent') + \
                                                                               ('i_visitor_agents',)
        result = {key: getattr(self, key) for key in keys}
        if for_yaml:
            if self.visitor_dominance_hierarchy is not None:
                result['visitor_dominance_hierarchy'] = str(self.visitor_dominance_hierarchy)
        return result


    @classmethod
    def _get_field_type_for_click(cls, field_name: str) -> type:
        field_type_map = {
            RealNumber: float,
        }
        raw_field_type = typing.get_type_hints(CoopConfig)[field_name]
        try:
            return field_type_map[raw_field_type]
        except KeyError:
            return raw_field_type


    @classmethod
    def add_options_to_click_command(cls,
                                     defaults: Optional[Mapping] = None
                                     ) -> Callable[click.decorators.FC, click.decorators.FC]:
        def inner(command: click.decorators.FC) -> click.decorators.FC:
            defaults_copy = dict(defaults or {})
            if defaults_copy:
                for value in defaults_copy.values():
                    assert isinstance(value, tuple)
            for field in cls.__dataclass_fields__.values():
                field: dataclasses.Field
                field_type = cls._get_field_type_for_click(field.name)
                dashed_field_name = field.name.replace('_', '-')
                option_kwargs = {
                    'type': field_type,
                    'default': defaults_copy.pop(field.name, (field.default,)),
                    'multiple': True,
                    'show_default': True,
                }
                if field_type is bool:
                    option_kwargs['is_flag'] = True
                    name = f'--{dashed_field_name}/--not-{dashed_field_name}'
                else:
                    name = f'--{dashed_field_name}'
                command = click.option(name, **option_kwargs)(command)
            if defaults_copy:
                raise Exception(f'Some unrecognized defaults were passed in: {defaults_copy}')
            return command
        return inner


    def __hash__(self) -> int:
        return hash(
            (type(self),
             *(getattr(self, field) for field in self.__dataclass_fields__))
        )
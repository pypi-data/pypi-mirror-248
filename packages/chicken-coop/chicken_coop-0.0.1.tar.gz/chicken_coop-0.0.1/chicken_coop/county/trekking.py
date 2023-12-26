from __future__ import annotations

import copy
import functools
import re
import yaml
import tempfile
import contextlib
import pathlib
import operator
import math
import os
import datetime as datetime_module
import lzma
import random
import json
import shutil

import pandas as pd
import sys
import subprocess
import itertools
import operator
import collections.abc
import contextlib
import pathlib
import pickle
import more_itertools
from typing import (Any, Mapping, Optional, BinaryIO, Iterable, TypeVar, TextIO, Iterator, Generator,
                    Hashable, Callable)
import io

import numpy as np
import ray.rllib
import svgwrite

from .constants import CHICKEN_COOP_HOME
from chicken_coop.county import csv_tools
from ..dominance_hierarching import (DominanceHierarchy,
                                     AttemptedTransitiveOperationOnIntransitiveDominanceHierarchy,
                                     AttemptedCompleteOperationOnIncompleteDominanceHierarchy)
from .typing import Agent, Action, RealNumber
from chicken_coop import county
from . import filtros
from . import misc


class BaseTrek:
    folder: pathlib.Path

    @property
    def meta_yaml_path(self) -> pathlib.Path:
        return self.folder / 'meta.yaml'

    @property
    def meta(self) -> dict:
        with self.meta_yaml_path.open('r') as file:
            return yaml.safe_load(file)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({repr(self.folder)})'

    def __str__(self) -> str:
        return str(self.folder)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseTrek):
            return False
        return (type(self) is type(other)) and (self.folder == other.folder)

    def __hash__(self) -> int:
        return hash((type(self), self.folder))


class Trek(BaseTrek):

    @staticmethod
    def create(*, extra_meta: Optional[dict[str, Any]] = None) -> Trek:
        folder = CHICKEN_COOP_HOME / (datetime_module.datetime.now().isoformat()
                                      .replace(':', '-').replace('.', '-').replace('T', '-'))
        folder.mkdir(parents=True, exist_ok=False)
        with (folder / 'meta.yaml').open('w') as yaml_file:
            yaml.dump(
                {
                    'argv': sys.argv,
                } | extra_meta,
                yaml_file,
            )
        return Trek(folder)

    def __init__(self, folder: pathlib.Path | str | os.PathLike) -> None:
        self.folder = pathlib.Path(folder).resolve()
        if not self.folder.exists():
            raise FileNotFoundError(self.folder)
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)


    @property
    def moniker(self) -> Optional[str]:
        return self.meta.get('moniker', None)


    def __enter__(self) -> pathlib.Path:
        self.original_stdout = sys.stdout
        sys.stdout = misc.TeeStream(self.original_stdout, self.folder / 'stdout')

        self.original_stderr = sys.stderr
        sys.stderr = misc.TeeStream(self.original_stderr, self.folder / 'stderr')

        print(f'Writing to folder {self.folder}')

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception: Optional[BaseException],
                 traceback: Optional[Any]) -> None:
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr


    @property
    def mini_treks(self) -> tuple[MiniTrek, ...]:
        return tuple(MiniTrek(path.parent) for path in sorted(self.folder.rglob('rollout.jsonl')))

    def get_mini_treks_grouped_by(self, key_function: Callable[MiniTrek, Any]
                                  ) -> dict[Any, tuple[MiniTrek, ...]]:
        result = collections.defaultdict(list)
        for mini_trek in self.mini_treks:
            value = key_function(mini_trek)
            result[value].append(mini_trek)
        return {value: tuple(mini_treks) for value, mini_treks in result.items()}


    @property
    def is_multi_trek(self) -> bool:
        return len(self.mini_treks) >= 2

    @property
    def is_single_trek(self) -> bool:
        return len(self.mini_treks) == 1

    @property
    def is_empty_trek(self) -> bool:
        return len(self.mini_treks) == 0


    @staticmethod
    def get(trek_path_expression: str | pathlib.Path | None,
            *, allow_multi_trek: bool = True, allow_single_trek: bool = True,
            allow_empty_trek: bool = False, moniker: Optional[str] = None) -> Trek:
        '''
        Get a trek, usually for running analysis or producing plots.

        A trek is a folder in `~/.chicken-coop/` which represents a single run of the `chicken_coop`
        package.

        When the user runs a command, e.g. a plot command, we allow the user to be able to specify
        which trek they are plotting, but for convenience we also allow not specifying a trek, in
        which case we choose the newest trek.
        '''
        trek_allowed = lambda trek: (
            ((allow_multi_trek and trek.is_multi_trek) or
             (allow_single_trek and trek.is_single_trek) or
             (allow_empty_trek and trek.is_empty_trek)) and
            (moniker is None or trek.moniker == moniker)
        )

        if trek_path_expression is None:
            for folder in sorted(CHICKEN_COOP_HOME.iterdir(), reverse=True):
                trek = Trek(folder)
                if trek_allowed(trek):
                    return trek
            else:
                raise FileNotFoundError
        else:
            trek = Trek(trek_path_expression)
            if trek_allowed(trek):
                return trek
            else:
                raise Exception


    def get_sample_mini_treks(self, *, forgive_lack_of_samples: bool = False
                              ) -> tuple[MiniTrek, ...]:
        n_agents = 6
        two_linear_mini_treks = []
        middle_non_linear_mini_trek = None
        non_middle_non_linear_mini_trek = None

        for mini_trek in self.mini_treks:
            dominance_hierarchy: DominanceHierarchy = mini_trek.dominance_hierarchy
            assert dominance_hierarchy.n_agents == n_agents

            if not dominance_hierarchy.is_complete:
                continue
            elif dominance_hierarchy.is_transitive:
                if len(two_linear_mini_treks) <= 1:
                    two_linear_mini_treks.append(mini_trek)
            elif (middle_non_linear_mini_trek is None) and (
                                       {0, n_agents - 1} <= set(dominance_hierarchy.linear_ranks)):
                middle_non_linear_mini_trek = mini_trek
            elif (non_middle_non_linear_mini_trek is None) and \
                                     ({0, n_agents - 1} & set(dominance_hierarchy.non_linear_ranks)):
                non_middle_non_linear_mini_trek = mini_trek

            sample_mini_treks = tuple(two_linear_mini_treks) + (middle_non_linear_mini_trek,
                                                                non_middle_non_linear_mini_trek)
            if len(sample_mini_treks) == 4 and (None not in sample_mini_treks):
                return sample_mini_treks

        if forgive_lack_of_samples and two_linear_mini_treks:
            return (tuple(filter(None, sample_mini_treks)) * 4)[:4]
        else:
            raise Exception




class MiniTrek(BaseTrek):
    def __init__(self, folder: pathlib.Path) -> None:
        self.folder = folder
        self.rollout_jsonl_path = self.folder / 'rollout.jsonl'
        self.progress_csv_path = self.folder / 'progress.csv'


    @functools.cached_property
    def dominance_hierarchy(self) -> DominanceHierarchy:
        dominance_hierarchy_texts = self.rollout_dataframe['population.dominance_hierarchy'][::-1]
        for dominance_hierarchy_text in dominance_hierarchy_texts:
            dominance_hierarchy = DominanceHierarchy(dominance_hierarchy_text)
            if dominance_hierarchy.is_complete:
                return dominance_hierarchy
        return DominanceHierarchy(dominance_hierarchy_texts.iloc[0])

    @property
    def rollout_dataframe(self) -> pd.DataFrame:
        return misc.jsonl_to_dataframe(self.rollout_jsonl_path, dot_notation=True)


    @property
    def rankized_rollout_dataframe(self) -> pd.DataFrame:
        if not self.dominance_hierarchy.is_transitive:
            raise AttemptedTransitiveOperationOnIntransitiveDominanceHierarchy
        if not self.dominance_hierarchy.is_complete:
            raise AttemptedCompleteOperationOnIncompleteDominanceHierarchy
        i_agent_by_rank = self.dominance_hierarchy.i_agent_by_rank
        rank_by_i_agent = tuple(i_agent_by_rank.index(i_agent)
                                for i_agent in self.dominance_hierarchy.i_agents)
        assert set(rank_by_i_agent) == set(i_agent_by_rank)

        def rename_agent_column(agent_column: str) -> str:
            i_agent_str, rest = re.fullmatch('^agent\.([0-9]+)\.(.+)$', agent_column).groups()
            rank = rank_by_i_agent[int(i_agent_str)]
            return f'rank.{rank}.{rest}'

        df = self.rollout_dataframe

        df.rename(columns={column: rename_agent_column(column)
                           for column in df.columns if column.startswith('agent.')},
                  inplace=True)

        return df

    @property
    def policy_path_by_name(self) -> dict[str, pathlib.Path]:
        return {
            policy_path.name: policy_path for policy_path in
            sorted(sorted((self.folder / 'policy_snapshots').iterdir())[-1].iterdir())
        }


    @staticmethod
    def get(mini_trek_descendant_path: str | os.PathLike) -> Trek:
        mini_trek_descendant_path = pathlib.Path(mini_trek_descendant_path)
        candidate_paths = itertools.chain((mini_trek_descendant_path,),
                                          mini_trek_descendant_path.parents)
        for candidate_path in candidate_paths:
            mini_trek_candidate = MiniTrek(candidate_path)
            if mini_trek_candidate.rollout_jsonl_path.exists():
                return mini_trek_candidate
        raise Exception


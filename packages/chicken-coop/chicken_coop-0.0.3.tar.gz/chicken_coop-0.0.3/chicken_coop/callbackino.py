from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable, Any, Sequence
import itertools
import pathlib
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

import more_itertools
import ray.rllib.env.multi_agent_env
import ray.rllib.algorithms.callbacks
from ray.rllib.utils.typing import PolicyID, MultiAgentDict, ModelWeights
from ray.rllib import algorithms
import ray.rllib.algorithms.a2c
import ray.rllib.algorithms.a3c
import ray.rllib.algorithms.ppo
import ray.rllib.algorithms.sac
import ray.rllib.algorithms.appo
import ray.rllib.algorithms.impala
import ray.rllib.algorithms.maddpg
from ray import rllib
import gymnasium
import gymnasium.spaces
import numpy as np
import pysnooper

from chicken_coop import county
from chicken_coop.county import misc
from chicken_coop.county import misc
from chicken_coop.county import csv_tools
from chicken_coop.county import policing
import chicken_coop
from chicken_coop.county.typing import Agent, RealNumber, PolicyID
from .stating import State, Move, Dialog
from .enving import Env


class Callbackino(ray.rllib.algorithms.callbacks.DefaultCallbacks):
    def on_episode_end(
        self,
        *,
        worker: ray.rllib.evaluation.RolloutWorker,
        base_env: ray.rllib.BaseEnv,
        policies: dict[PolicyID, ray.rllib.Policy],
        episode: ray.rllib.evaluation.Episode | ray.rllib.evaluation.episode_v2.EpisodeV2 |
            Exception,
        **kwargs,
        ) -> None:

        if isinstance(episode, Exception):
            return


    def on_train_result(
        self,
        *,
        algorithm: ray.rllib.algorithms.Algorithm,
        result: dict,
        **kwargs,
        ) -> None:
        """Called at the end of Algorithm.train().

        Args:
            algorithm: Current Algorithm instance.
            result: Dict of results returned from Algorithm.train() call.
                You can mutate this object to add additional metrics.
            kwargs: Forward compatibility placeholder.
        """
        pass

    def on_episode_end(
        self,
        *,
        worker: rllib.evaluation.RolloutWorker,
        base_env: rllib.env.BaseEnv,
        policies: dict[PolicyID, rllib.Policy],
        episode: Union[rllib.evaluation.Episode, rllib.evaluation.episode_v2.EpisodeV2, Exception],
        env_index: Optional[int] = None,
        **kwargs,
    ) -> None:
        """Runs when an episode is done.

        Args:
            worker: Reference to the current rollout worker.
            base_env: BaseEnv running the episode. The underlying
                sub environment objects can be retrieved by calling
                `base_env.get_sub_environments()`.
            policies: Mapping of policy id to policy
                objects. In single agent mode there will only be a single
                "default_policy".
            episode: Episode object which contains episode
                state. You can use the `episode.user_data` dict to store
                temporary data, and `episode.custom_metrics` to store custom
                metrics for the episode.
                In case of environment failures, episode may also be an Exception
                that gets thrown from the environment before the episode finishes.
                Users of this callback may then handle these error cases properly
                with their custom logics.
            env_index: The index of the sub-environment that ended the episode
                (within the vector of sub-environments of the BaseEnv).
            kwargs: Forward compatibility placeholder.
        """
        (env,) = base_env.get_sub_environments()
        last_state: State = env.state
        episode.custom_metrics |= {
            'zeitgeist_array': last_state.zeitgeist.to_array()
            # f'dialog.{agent_a}.{agent_b}': last_state.dialog_by_i_agent_pair[i_agent_a, i_agent_b]
            # for (i_agent_a, agent_a), (i_agent_b, agent_b) in
            # itertools.combinations(enumerate(self.coop_config.policy_by_agent), 2)
        }
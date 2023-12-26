from __future__ import annotations

from typing import Tuple, Optional, Dict, Mapping, Iterable
import abc
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

import ray.rllib.env.multi_agent_env
from ray.rllib.algorithms.ppo import PPO # pytype: disable=import-error
import gymnasium
import gymnasium.spaces
from frozendict import frozendict
import numpy as np
from scipy import stats
import more_itertools

from chicken_coop import county
from chicken_coop.county import misc
from chicken_coop.county.typing import Agent, RealNumber
from chicken_coop.county.constants import ALL_AGENTS


class CoopException(Exception):
    pass
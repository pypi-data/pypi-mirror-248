from __future__ import annotations

import random
import pprint
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
import yaml
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



@cli.group()
@click.option('-p', '--path', 'trek_path_expression', type=str, required=False)
@click.option('-f', '--forgive-lack-of-samples', 'forgive_lack_of_samples', is_flag=True)
@click.pass_context
def analyze_paper(context: click.Context, *, trek_path_expression: Optional[str],
                  forgive_lack_of_samples: bool) -> None:
    context.ensure_object(dict)
    context.obj['trek_path_expression'] = trek_path_expression
    context.obj['forgive_lack_of_samples'] = forgive_lack_of_samples




@analyze_paper.command()
@click.pass_context
def analyzo(context: click.Context) -> None:

    trek = trekking.Trek.get(context.obj['trek_path_expression'], allow_single_trek=False)

    print(f'Making an `analyzo` analysis for {trek} ...', file=sys.stderr)

    mini_treks = [mini_trek for mini_trek in trek.mini_treks
                  if mini_trek.dominance_hierarchy.is_complete]
    counter = collections.Counter(mini_trek.dominance_hierarchy for mini_trek in mini_treks)

    result = {
        'n_populations': len(mini_treks),
        'n_populations_that_converged_to_dominance_hierarchy': sum(
            mini_trek.dominance_hierarchy.is_complete for mini_trek in mini_treks
        ),
        'n_dominance_hierarchies': len(counter),
        'n_transitive_dominance_hierarchies': (
            n_transitive_dominance_hierarchies := sum(dominance_hierarchy.is_transitive
                                                      for dominance_hierarchy in counter)
        ),
        'n_intransitive_dominance_hierarchies': len(counter) - n_transitive_dominance_hierarchies,
        'transitive_ratio': n_transitive_dominance_hierarchies / len(counter),
        'most_common': list(list(zip(*counter.most_common(3)))[1]),
        'least_common': list(list(zip(*counter.most_common()[:-4:-1]))[1]),
    }
    print(yaml.dump(result))

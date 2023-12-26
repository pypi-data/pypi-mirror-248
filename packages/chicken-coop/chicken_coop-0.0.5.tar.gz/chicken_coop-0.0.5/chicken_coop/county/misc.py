from __future__ import annotations

import copy
import re
import statistics
import functools
import yaml
import tempfile
import contextlib
import pathlib
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
                    Sequence)
import io

import numpy as np
import ray.rllib
import svgwrite

from .constants import CHICKEN_COOP_HOME
from chicken_coop.county import csv_tools
from .typing import Agent, Action, RealNumber
from chicken_coop import county
from . import filtros





def sane_kwargs(function):
    @functools.wraps(function)
    def inner(config):
        return function(**config)
    return inner


def jsonl_to_dataframe(jsonl_path: str | pathlib.Path, *, dot_notation: bool = False) -> pd.DataFrame:
    jsonl_path = pathlib.Path(jsonl_path)
    with jsonl_path.open() as file:
        entries = list(map(json.loads, file))
    if dot_notation:
        for entry in entries:
            unprocessed_keys = set(entry)
            while unprocessed_keys:
                key = unprocessed_keys.pop()
                if isinstance(entry[key], dict):
                    for sub_key, sub_value in entry[key].items():
                        unprocessed_keys.add(dotted_key := f'{key}.{sub_key}')
                        entry[dotted_key] = sub_value
                    del entry[key]

    return pd.DataFrame(entries)


def compute_actions_for_all_agents(algorithm: ray.rllib.algorithms.Algorithm,
                                   env: county.BaseEnv) -> dict[Agent, Action]:
    return {agent: algorithm.compute_single_action(
        env.observation_by_agent[agent],
        policy_id=algorithm.config['policy_mapping_fn'](agent)
    )
            for agent in env.get_agent_ids()}



def compickle(thing: Any, file_or_path: pathlib.Path | BinaryIO, /) -> None:
    with contextlib.ExitStack() as exit_stack:
        if isinstance(file_or_path, pathlib.Path):
            file_ = exit_stack.enter_context(file_or_path.open('wb'))
        else:
            file_ = file_or_path
        file_.write(lzma.compress(pickle.dumps(thing)))


def compickle_to_bytes(thing: Any)-> bytes:
    bytes_io = io.BytesIO()
    compickle(thing, bytes_io)
    return bytes_io.getvalue()

def uncompickle(file_or_path: pathlib.Path | BinaryIO, /) -> Any:
    with contextlib.ExitStack() as exit_stack:
        if isinstance(file_or_path, pathlib.Path):
            file_ = exit_stack.enter_context(file_or_path.open('rb'))
        else:
            file_ = file_or_path
        return pickle.loads(lzma.decompress(file_.read()))

def uncompickle_from_bytes(compickled_bytes: bytes) -> Any:
    return uncompickle(io.BytesIO(compickled_bytes))


class TroubleshootingDict(collections.abc.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._map = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self._map[key]

    def __delitem__(self, key):
        del self._map[key]

    def __setitem__(self, key, value):
        if isinstance(value, list):
            if all(isinstance(item, list) for item in value):
                value = TroubleshootingList(map(TroubleshootingList, value))
            else:
                value = TroubleshootingList(value)
        self._map[key] = value

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

    def __repr__(self):
        return f'{type(self).__name__}({self._map})'


class TroubleshootingList(collections.abc.MutableSequence):
    def __init__(self, *args, **kwargs):
        self._list = list(*args, **kwargs)

    def __getitem__(self, key):
        return self._list[key]

    def __delitem__(self, key):
        del self._list[key]

    def __setitem__(self, key, value):
        self._list[key] = value

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def insert(self, index, thing):
        self._list.insert(index, thing)

    def __repr__(self):
        return f'{type(self).__name__}({self._list})'



def all_equal(values: Iterable[Any]) -> bool:
    return all(itertools.starmap(operator.eq, more_itertools.windowed(values, 2)))


def cute_div(x: RealNumber, y: RealNumber, *, default: RealNumber = 0) -> RealNumber:
    try:
        return x / y
    except ZeroDivisionError:
        return default

# def cool_windowed(iterable: Iterable[Any], n: int = 2) -> Iterable[tuple[Any, Any]]:
    # sentinel = object()
    # for left, right in more_itertools.windowed(iterable, n, fillvalue=sentinel):
        # if sentinel in (left, right):
            # return
        # yield (left, right)

def get_chicken_coop_repo_commit() -> Optional[str]:
    try:
        result = subprocess.run(
            ('/usr/bin/git', 'rev-parse', 'HEAD'),
            check=True,
            cwd=pathlib.Path(__file__).parent,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding='utf-8',
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_chicken_coop_repo_is_clean() -> Optional[bool]:
    result = subprocess.run(
        (cmd := ('/usr/bin/git', 'diff-index', '--quiet', 'HEAD')),
        cwd=pathlib.Path(__file__).parent,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding='utf-8',
    )
    if result.returncode == 0:
        return True
    elif result.returncode == 1:
        return False
    else:
        return None

def clamp(number: RealNumber, low: RealNumber, high: RealNumber) -> RealNumber:
    if number < low:
        return low
    elif number > high:
        return high
    else:
        return number


class TeeStream:
    def __init__(self, original_stream: TextIO, path: pathlib.Path)-> None:
        self.original_stream = original_stream
        self.path = path

    def write(self, message: str) -> None:
        self.original_stream.write(message)
        with self.path.open('a') as file:
            file.write(message)

    def flush(self) -> None:
        self.original_stream.flush()

    def fileno(self) -> int:
        return self.original_stream.fileno()

    def close(self) -> None:
        pass


@contextlib.contextmanager
def tee_stdout(path: pathlib.Path) -> None:
    original_stdout = sys.stdout
    sys.stdout = TeeStream(original_stdout, path)
    try:
        yield
    finally:
        sys.stdout = original_stdout


@contextlib.contextmanager
def tee_stderr(path: pathlib.Path, *, ensure_filtros: bool = True) -> None:
    original_stderr = sys.stderr
    sys.stderr = TeeStream(original_stderr, path)
    try:
        if ensure_filtros:
            filtros.activate()
        yield
    finally:
        sys.stderr = original_stderr


class BaseRolloutReporter(collections.abc.Sequence):
    def __init__(self) -> None:
        self.rows = []

    def __iter__(self) -> Iterator[dict[str, Any]]:
        yield from self.rows

    def __getitem__(self, i: int) -> dict[str, Any]:
        return self.rows[i]

    def __len__(self) -> int:
        return len(self.rows)

    def __reversed__(self) -> Iterator[dict[str, Any]]:
        yield from reversed(self.rows)

    def as_dataframe(self) -> pd.DataFrame:
        pd.DataFrame.from_dict(self.rows)

    def report(self, row_or_rows: Mapping[str, Any] | Iterable[Mapping[str, Any]], /) -> None:
        for row in self._parse_row_or_rows(row_or_rows):
            row = dict(row)
            self.rows.append(row)

    @staticmethod
    def _parse_row_or_rows(row_or_rows: Mapping[str, Any] | Iterable[Mapping[str, Any]]
                           ) -> Iterable[Mapping[str, Any]]:
        if isinstance(row_or_rows, collections.abc.Mapping):
            return (row_or_rows,)
        else:
            return row_or_rows

class NumpyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.floating):
            if np.isnan(obj):
                return None  # Serialized as JSON null.
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)

class TuneRolloutReporter(BaseRolloutReporter):
    def report(self, row_or_rows: Mapping[str, Any] | Iterable[Mapping[str, Any]], /) -> None:
        import ray.tune
        for row in self._parse_row_or_rows(row_or_rows):
            BaseRolloutReporter.report(self, row)
            ray.tune.report(**row)

class BaseFileRolloutReporter(BaseRolloutReporter):
    def __init__(self, path: pathlib.Path) -> None:
        BaseRolloutReporter.__init__(self)
        self.path = path


class CsvRolloutReporter(BaseFileRolloutReporter):
    def report(self, row_or_rows: Mapping[str, Any] | Iterable[Mapping[str, Any]], /) -> None:
        for row in self._parse_row_or_rows(row_or_rows):
            BaseFileRolloutReporter.report(self, row)
            with csv_tools.CSVWriter(self.path, row.keys(),
                                     overwrite=(len(self.rows) == 1)) as csv_writer:
                csv_writer.write_row(row)

class JsonlRolloutReporter(BaseFileRolloutReporter):
    def report(self, row_or_rows: Mapping[str, Any] | Iterable[Mapping[str, Any]], /) -> None:
        for row in self._parse_row_or_rows(row_or_rows):
            BaseFileRolloutReporter.report(self, row)
            make_tree = lambda: collections.defaultdict(make_tree)
            tree = make_tree()
            for key, value in row.items():
                *parents, short_name = key.split('.')
                subtree = tree
                for parent in parents:
                    subtree = subtree[parent]
                subtree[short_name] = value

            with self.path.open('a') as file:
                json.dump(tree, file, cls=NumpyJsonEncoder)
                file.write('\n')



def shuffled(iterable: Iterable[Any], *, seed: Optional[int] = None) -> tuple[Any, ...]:
    list_ = list(iterable)
    random.Random(seed).shuffle(list_)
    return tuple(list_)

def get_mean_dataframe_from_experiment_analysis(
    experiment_analysis: ray.tune.ExperimentAnalysis,
    fields_that_need_last: tuple[str] = ()) -> pd.DataFrame:

    rows = {
        path: df.mean(numeric_only=True).to_dict()
        for path, df in experiment_analysis.trial_dataframes.items()
    }

    for field_that_needs_last in fields_that_need_last:
        for path, df in experiment_analysis.trial_dataframes.items():
            rows[path][field_that_needs_last] = df[field_that_needs_last].values[-1]

    all_configs = experiment_analysis.get_all_configs(prefix=True)
    for path, config in all_configs.items():
        if path in rows:
            rows[path].update(config)
            rows[path].update(logdir=path)
    return pd.DataFrame(list(rows.values()))

def int_sqrt(x: RealNumber) -> int:
    sqrt_float = math.sqrt(x)
    sqrt_int = int(sqrt_float)
    if not sqrt_int == sqrt_float:
        raise ValueError(f"Got number {x} when expecting a number that's a square of an "
                         f"integer. Alas, the sqrt of {x} is a non-int: {sqrt_float}")
    return sqrt_int


def make_one_hot(i: int, n: int) -> np.ndarray:
    array = np.zeros((n,), dtype=np.int8)
    array[i] = 1
    return array

@contextlib.contextmanager
def create_temp_folder(*, prefix=tempfile.template, suffix='',
                       parent_folder=None, chmod=None):
    '''
    Context manager that creates a temporary folder and deletes it after usage.

    After the suite finishes, the temporary folder and all its files and
    subfolders will be deleted.

    Example:

        with create_temp_folder() as temp_folder:

            # We have a temporary folder!
            assert temp_folder.is_dir()

            # We can create files in it:
            (temp_folder / 'my_file').open('w')

        # The suite is finished, now it's all cleaned:
        assert not temp_folder.exists()

    Use the `prefix` and `suffix` string arguments to dictate a prefix and/or a
    suffix to the temporary folder's name in the filesystem.

    If you'd like to set the permissions of the temporary folder, pass them to
    the optional `chmod` argument, like this:

        create_temp_folder(chmod=0o550)

    '''
    temp_folder = pathlib.Path(tempfile.mkdtemp(prefix=prefix, suffix=suffix,
                                                dir=parent_folder))
    try:
        if chmod is not None:
            temp_folder.chmod(chmod)
        yield temp_folder
    finally:
        shutil.rmtree(str(temp_folder))

def zero_based_accumulate(iterable: Iterable[RealNumber],
                          drop_last: bool = False) -> Iterable[RealNumber]:
    old_item = 0
    for new_item in itertools.accumulate(iterable):
        yield old_item
        old_item = new_item
    if not drop_last:
        yield new_item


def duplicate_shape_with_attribs(shape: svgwrite.base.BaseElement, **attribs
                                 ) -> svgwrite.base.BaseElement:
    new_shape = copy.deepcopy(shape)
    new_shape.attribs |= attribs
    return new_shape


def duplicate_with_offset(shape: svgwrite.base.BaseElement | Shapino, dx: float, dy: float
               ) -> svgwrite.base.BaseElement | Shapino:
    if isinstance(shape, Shapino):
        return shape.add_offset(dx, dy)

    attribs = shape.attribs.copy()
    match shape:
        case svgwrite.shapes.Rect():
            return duplicate_shape_with_attribs(
                shape,
                x=float(attribs.get('x', 0)) + dx,
                y=float(attribs.get('y', 0)) + dy,
            )
        case svgwrite.shapes.Circle():
            return duplicate_shape_with_attribs(
                shape,
                cx=float(attribs.get('cx', 0)) + dx,
                cy=float(attribs.get('cy', 0)) + dy,
            )
        case svgwrite.shapes.Line():
            return duplicate_shape_with_attribs(
                shape,
                x1=float(attribs.get('x1', 0)) + dx,
                y1=float(attribs.get('y1', 0)) + dy,
                x2=float(attribs.get('x2', 0)) + dx,
                y2=float(attribs.get('y2', 0)) + dy,
            )
        case svgwrite.shapes.Ellipse():
            return duplicate_shape_with_attribs(
                shape,
                cx=float(attribs.get('cx', 0)) + dx,
                cy=float(attribs.get('cy', 0)) + dy,
            )
        case svgwrite.shapes.Polyline():
            return duplicate_shape_with_attribs(
                shape,
                points=[(float(p[0]) + dx, float(p[1]) + dy,) for p in attribs.get('points', [])]
            )
        case svgwrite.shapes.Polygon():
            return duplicate_shape_with_attribs(
                shape,
                points=[(float(p[0])+dx, float(p[1])+dy) for p in attribs.get('points', [])]
            )
        case svgwrite.text.Text():
            return duplicate_shape_with_attribs(
                shape,
                x=float(attribs.get('x', 0)) + dx,
                y=float(attribs.get('y', 0)) + dy,
            )
        case svgwrite.image.Image():
            return duplicate_shape_with_attribs(
                shape,
                x=float(attribs.get('x', 0)) + dx,
                y=float(attribs.get('y', 0)) + dy,
            )
        case svgwrite.container.Use():
            return duplicate_shape_with_attribs(
                shape,
                x=float(attribs.get('x', 0)) + dx,
                y=float(attribs.get('y', 0)) + dy,
            )
        case _:
            return duplicate_shape_with_attribs(shape)

class Shapino:

    padding = 0

    def __init__(self, shapes_or_shapinos: Iterable[svgwrite.base.BaseElement | Shapino] = (),
                 x: RealNumber = 0, y: RealNumber = 0) -> None:
        self.shapes = []
        self.add(shapes_or_shapinos, x, y)

    def add(self, shapes_or_shapinos: Iterable[svgwrite.base.BaseElement | Shapino] = (),
            x: RealNumber = 0, y: RealNumber = 0) -> None:
        items = collections.deque(shapes_or_shapinos)
        while items:
            item = items.popleft()
            if isinstance(item, svgwrite.base.BaseElement):
                self.shapes.append(duplicate_with_offset(item, x, y))
            else:
                items.extend(item)

    @property
    def bounding_box(self) -> Tuple[float, float, float, float]:
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for shape in self.shapes:
            match shape:
                case svgwrite.shapes.Rect():
                    x, y, w, h = map(float, (shape.attribs.get(attr, 0)
                                             for attr in ('x', 'y', 'width', 'height')))
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x + w), max(max_y, y + h)
                case svgwrite.shapes.Circle():
                    cx, cy, r = map(float, (shape.attribs.get(attr, 0)
                                            for attr in ('cx', 'cy', 'r')))
                    r += shape.attribs.get('stroke_width', 1) / 2
                    min_x, min_y = min(min_x, cx - r), min(min_y, cy - r)
                    max_x, max_y = max(max_x, cx + r), max(max_y, cy + r)
                case svgwrite.shapes.Line():
                    x1, y1, x2, y2 = map(float, (shape.attribs.get(attr, 0)
                                                 for attr in ('x1', 'y1', 'x2', 'y2')))
                    min_x, min_y = min(min_x, min(x1, x2)), min(min_y, min(y1, y2))
                    max_x, max_y = max(max_x, max(x1, x2)), max(max_y, max(y1, y2))
                case svgwrite.shapes.Ellipse():
                    cx, cy, rx, ry = map(float, (shape.attribs.get(attr, 0)
                                                 for attr in ('cx', 'cy', 'rx', 'ry')))
                    min_x, min_y = min(min_x, cx - rx), min(min_y, cy - ry)
                    max_x, max_y = max(max_x, cx + rx), max(max_y, cy + ry)
                case svgwrite.shapes.Polyline():
                    points = shape.attribs.get('points', [])
                    xs, ys = zip(*((float(p[0]), float(p[1])) for p in points))
                    min_x, min_y = min(min_x, min(xs)), min(min_y, min(ys))
                    max_x, max_y = max(max_x, max(xs)), max(max_y, max(ys))
                case svgwrite.shapes.Polygon():
                    points = shape.attribs.get('points', [])
                    xs, ys = zip(*((float(p[0]), float(p[1])) for p in points))
                    min_x, min_y = min(min_x, min(xs)), min(min_y, min(ys))
                    max_x, max_y = max(max_x, max(xs)), max(max_y, max(ys))
                case svgwrite.path.Path():
                    pass
                case svgwrite.text.Text():
                    x, y = float(shape.attribs.get('x', 0)), float(shape.attribs.get('y', 0))
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x), max(max_y, y)
                case svgwrite.image.Image():
                    x, y, w, h = map(float, (shape.attribs.get(attr, 0)
                                             for attr in ('x', 'y', 'width', 'height')))
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x + w), max(max_y, y + h)
                case svgwrite.container.Use():
                    x, y = float(shape.attribs.get('x', 0)), float(shape.attribs.get('y', 0))
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x), max(max_y, y)
                case _:
                    pass

        return (min_x - self.padding,
                min_y - self.padding,
                max_x - min_x + 2 * self.padding,
                max_y - min_y + 2 * self.padding)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {len(self.shapes)} shapes, {self.bounding_box}>'

    def __iter__(self):
        return iter(self.shapes)

    @property
    def svg_text(self, size=('100%', '100%'), **extra) -> str:
        with create_temp_folder(prefix='chicken_coop_') as temp_folder:
            drawing_path = temp_folder / 'svg.svg'
            drawing = svgwrite.Drawing(drawing_path, size=size, **extra)
            drawing.viewbox(*self.bounding_box)
            for shape in self:
                drawing.add(shape)
            drawing.save()
            return drawing_path.read_text()

    def duplicate_with_offset(self, x: RealNumber, y: RealNumber) -> Shapino:
        new_shapino: Shapino = copy.deepcopy(self)
        new_shapino.shapes[:] = (duplicate_with_offset(shape, x, y) for shape in self)
        return new_shapino

    def duplicate_with_anchor_on_middle_left(self) -> Shapino:
        x, y, w, h = self.bounding_box
        new_shapino = self.duplicate_with_offset(-x, -y - (h / 2))
        new_x, new_y, new_w, new_h = new_shapino.bounding_box
        assert abs(new_x) < 0.01
        assert abs((new_y / (new_h / 2)) + 1) < 0.01
        return new_shapino

    def duplicate_with_anchor_on_top_center(self) -> Shapino:
        x, y, w, h = self.bounding_box
        new_shapino = self.duplicate_with_offset(-x - (w / 2), -y)
        new_x, new_y, new_w, new_h = new_shapino.bounding_box
        assert abs((new_x / (new_w / 2)) + 1) < 0.01
        assert abs(new_y) < 0.01
        return new_shapino



def get_last_line_from_file(path: pathlib.Path) -> bytes:
    with path.open('rb') as f:
        f.seek(-2, 2)  # Jump to the second last byte.

        # If the file is too short (possibly just one line or empty)
        if f.tell() == -1:
            f.seek(0)  # Go to the start
        else:
            # Search for the beginning of the last line
            while f.read(1) != b'\n':
                f.seek(-2, 1)
        return f.readline()


def get_last_entry_from_jsonl(jsonl_path: pathlib.Path) -> Any:
    return json.loads(get_last_line_from_file(jsonl_path))

def to_tuple(single_or_sequence, item_type=None, item_test=None):
    '''
    Convert an item or a sequence of items into a tuple of items.

    This is typically used in functions that request a sequence of items but
    are considerate enough to accept a single item and wrap it in a tuple
    `(item,)` themselves.

    This function figures out whether the user entered a sequence of items, in
    which case it will only be converted to a tuple and returned; or the user
    entered a single item, in which case a tuple `(item,)` will be returned.

    To aid this function in parsing, you may optionally specify `item_type`
    which is the type of the items, or alternatively `item_test` which is a
    callable that takes an object and returns whether it's a valid item. These
    are necessary only when your items might be sequences themselves.

    You may optionally put multiple types in `item_type`, and each object would
    be required to match to at least one of them.
    '''
    if (item_type is not None) and (item_test is not None):
        raise Exception('You may specify either `item_type` or '
                        '`item_test` but not both.')
    if item_test is not None:
        actual_item_test = item_test
    elif item_type is not None:
        actual_item_test = \
            lambda candidate: isinstance(candidate, item_type)
    else:
        actual_item_test = None

    if actual_item_test is None:
        if isinstance(single_or_sequence, collections.abc.Sequence):
            return tuple(single_or_sequence)
        elif single_or_sequence is None:
            return tuple()
        else:
            return (single_or_sequence,)
    else: # actual_item_test is not None
        if actual_item_test(single_or_sequence):
            return (single_or_sequence,)
        elif single_or_sequence is None:
            return ()
        else:
            return tuple(single_or_sequence)


def int_to_base(n: int, base: int) -> tuple:
    if n == 0:
        return (0,)
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return tuple(digits)



class ListifyingDumper(yaml.Dumper):
    def _represent_tuple(self, data):
        return self.represent_list(data)

ListifyingDumper.add_representer(tuple, ListifyingDumper._represent_tuple)


def _get_wacky_choices(m: int, *, n: int, k: int) -> tuple[tuple, ...]:
    if n == 0:
        return ((),) * k
    result = []
    counter = collections.Counter({i: 0 for i in range(m)})
    for _ in range(k):
        least_chosen = counter.most_common()[-1][0]
        fluffs = tuple(
            sorted([least_chosen] + random.sample(tuple(range(least_chosen)) +
                                                  tuple(range(least_chosen + 1, m)), n - 1))
        )
        for fluff in fluffs:
            counter[fluff] += 1
        result.append(fluffs)

    return tuple(result)


def get_wacky_choices(iterable: Iterable, /, *, n: int, k: int) -> tuple[tuple, ...]:
    sequence = iterable if isinstance(iterable, Sequence) else tuple(iterable)
    result = _get_wacky_choices(len(sequence), n=n, k=k)
    return tuple(tuple(map(sequence.__getitem__, fluff)) for fluff in result)


def get_int_from_mixed_string(s: str) -> int:
    return int(re.fullmatch('^[^0-9]*([0-9]+)[^0-9]*$', s).group(1))


def mean_default(numbers: Iterable[float | int], *, default: Optional[float | int] = None
                 ) -> float | int:
    numbers = tuple(numbers)
    if not numbers and default is not None:
        return default
    return statistics.mean(numbers)


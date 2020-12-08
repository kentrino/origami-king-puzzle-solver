from multiprocessing import Queue
from typing import NamedTuple, Optional, List

import numpy as np

from message_queue import MessageQueue

_zero = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


try:
    profile
except NameError:
    def profile(func):
        return func


class Command(NamedTuple):
    type: str
    i: int
    n: int


class RunContext(NamedTuple):
    field_0: np.ndarray
    range: range
    task_id: int
    queue: Optional[MessageQueue]


@profile
def _process_command(field: np.ndarray, c: Command):
    if c.type == "r":
        field[c.i] = np.roll(field[c.i], c.n)
        return field
    else:
        fi = np.concatenate([field[:, 0:6], np.flipud(field[:, 6:12])])
        fi[:, c.i] = np.roll(fi[:, c.i], c.n)
        return np.concatenate([fi[0:4, :], np.flipud(fi[4:8, :])], 1)


ring_rotation_patterns = 44
column_slide_patten = 42
all_patterns = ring_rotation_patterns + column_slide_patten


@profile
def _generate_command(m: int) -> Command:
    """
    rの手数
    n: 11
    i: 4
    44
    cの手数
    n: 7
    i: 6
    42
    """
    if m < ring_rotation_patterns:
        n = m // 4
        i = m % 4
        return Command(type="r", i=i, n=n + 1)
    else:
        b = m - 44
        n = b // 6
        i = b % 6
        return Command(type="c", i=i, n=n + 1)


@profile
def _check_hummer(_field: np.ndarray, _i: int):
    return \
        _field[2, _i - 1] == 1 and \
        _field[3, _i - 1] == 1 and \
        _field[2, _i] == 1 and \
        _field[3, _i] == 1


@profile
def _add_hummer(_field: np.ndarray, _i: int):
    _field[2:4, _i] = [1, 1]
    _field[2:4, _i - 1] = [1, 1]


@profile
def _check(field: np.ndarray):
    # [4, 3, 2, 1, ... , 0]
    a = np.sum(field, axis=0)
    if np.any(a == 3) or np.any(a == 1):
        return False
    # [1, 0, 0, 0, ... , 0]
    b = a // 4
    # bootsにヒットしたものを除いた残り
    left = field - np.stack([b, b, b, b], axis=0)
    # 上段に1があればfail
    if np.any(left[0:2, :] == 1):
        return False
    z = np.array(_zero)
    for i in range(0, 12):
        if _check_hummer(field, i):
            _add_hummer(z, i)
    return np.all(left - z == 0)


def run(context: RunContext) -> Optional[List[Command]]:
    for i in context.range:
        if i >= all_patterns:
            return None
        # noinspection PyTypeChecker
        f: List[np.ndarray] = [None] * 3
        # noinspection PyTypeChecker
        c: List[Command] = [None] * 3
        f[0] = np.copy(context.field_0)
        c[0] = _generate_command(i)
        f[0] = _process_command(f[0], c[0])
        for j in range(0, all_patterns):
            f[1] = np.copy(f[0])
            c[1] = _generate_command(j)
            f[1] = _process_command(f[1], c[1])
            for k in range(0, all_patterns):
                f[2] = np.copy(f[1])
                c[2] = _generate_command(k)
                if context.queue is not None:
                    context.queue.debug(c, context.task_id)
                f[2] = _process_command(f[2], c[2])
                if _check(f[2]):
                    return c
    return None

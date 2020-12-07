from collections import namedtuple
from typing import TypedDict, NamedTuple

import numpy as np
import sys

try:
    profile
except NameError:
    def profile(func):
        return func


f = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
]

zero = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class Command(NamedTuple):
    type: str
    i: int
    n: int


@profile
def process_command(field, c: Command):
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
def generate_one(m: int) -> Command:
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
        return Command(type="r", i=i, n=n+1)
    else:
        b = m - 44
        n = b // 6
        i = b % 6
        return Command(type="c", i=i, n=n+1)


@profile
def check_boots(_field: np.ndarray, _i: int):
    # 282ms
    return \
        _field[0, _i] == 1 and \
        _field[1, _i] == 1 and \
        _field[2, _i] == 1 and \
        _field[3, _i] == 1
    # 715ms
    # return np.all(_field[:, _i] == 1)


@profile
def check_hummer(_field: np.ndarray, _i: int):
    # 2331ms
    # return np.all(np.stack([_field[2:4, _i - 1], _field[2:4, _i]], 1))
    # 337ms
    return \
        _field[2, _i - 1] == 1 and \
        _field[3, _i - 1] == 1 and \
        _field[2, _i] == 1 and \
        _field[3, _i] == 1


@profile
def add_hummer(_field: np.ndarray, _i: int):
    _field[2:4, _i] = [1, 1]
    _field[2:4, _i - 1] = [1, 1]


@profile
def add_boots(_field: np.ndarray, _i: int):
    _field[:, _i] = [1, 1, 1, 1]


@profile
def check(field: np.ndarray):
    z = np.array(zero)
    # np.where(np.sum(field, axis=0) == 4)
    for i in range(0, 12):
        if check_boots(field, i):
            add_boots(z, i)
    for i in range(0, 12):
        if check_hummer(field, i):
            add_hummer(z, i)
    return np.all(field - z == 0)


@profile
def erase(n: int = 1):
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    for i in range(0, n):
        sys.stdout.write(cursor_up_one)
        sys.stdout.write(erase_line)


@profile
def solve(input_):
    field_0 = np.array(input_)
    for i in range(0, all_patterns):
        field_1 = np.copy(field_0)
        command_1 = generate_one(i)
        field_1 = process_command(field_1, command_1)
        for j in range(0, all_patterns):
            field_2 = np.copy(field_1)
            command_2 = generate_one(j)
            field_2 = process_command(field_2, command_2)
            for k in range(0, 2):
                field_3 = np.copy(field_2)
                command_3 = generate_one(k)
                print(command_1, command_2, command_3)
                field_3 = process_command(field_3, command_3)
                if check(field_3):
                    print(command_1, command_2, command_3)
                    return
                erase()


solve(f)
# process(f, [['c', 1, 4], ['r', 2, 1], ['c', 1, 4]])

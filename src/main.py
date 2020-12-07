import numpy as np
import sys

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


def process_command(field, command, i, n):
    if command == "r":
        field[i] = np.roll(field[i], n)
        return field
    else:
        fi = np.concatenate([field[:, 0:6], np.flipud(field[:, 6:12])])
        fi[:, i] = np.roll(fi[:, i], n)
        return np.concatenate([fi[0:4, :], np.flipud(fi[4:8, :])], 1)


def generate_one(m: int):
    """
    rの手数
    n: 12
    i: 4
    cの手数
    n: 8
    i: 6
    """
    a = m // 48
    b = m % 48
    if a == 0:
        n = b // 4
        i = b % 4
        return ["r", i, n]
    else:
        n = b // 6
        i = b % 6
        return ["c", i, n]


def check(field):
    def check_boots(_field, _i):
        return np.all(_field[:, _i] == 1)

    def check_hummer(_field, _i):
        return np.all(np.stack([_field[2:4, _i - 1], _field[2:4, _i]], 1))

    def add_hummer(_field, _i):
        _field[2:4, _i] = [1, 1]
        _field[2:4, _i - 1] = [1, 1]

    def add_boots(_field, _i):
        _field[:, _i] = [1, 1, 1, 1]

    z = np.array(zero)
    for i in range(0, 12):
        if check_boots(field, i):
            add_boots(z, i)
    for i in range(0, 12):
        if check_hummer(field, i):
            add_hummer(z, i)
    return np.all(field - z == 0)


def erase(n):
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    for i in range(0, n):
        sys.stdout.write(cursor_up_one)
        sys.stdout.write(erase_line)


def process(input_, commands):
    field = np.array(input_)
    # print(field)
    for command in commands:
        # print(command)
        c, i, n = command
        field = process_command(field, c, i=i, n=n)
        # print(field)
    return field


def solve(input_):
    for i in range(0, 96 ** 3):
        print(i)
        commands = []
        for index in [i // (96 ** 2), (i % (96 ** 2)) // 96, i % 96]:
            commands.append(generate_one(index))
        print(commands)
        if check(process(input_, commands)):
            return
        erase(2)


solve(f)
# process(f, [['c', 1, 4], ['r', 2, 1], ['c', 1, 4]])

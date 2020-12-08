from solve import solve
from solve_multiprocess import solve_multiprocess

_initial_field = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
]

if __name__ == '__main__':
    print(solve_multiprocess(_initial_field, n_process=16, debug_print=False))
    # print(solve(_initial_field))

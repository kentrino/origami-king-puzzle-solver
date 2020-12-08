import numpy as np

from run import run, RunContext


def solve(field_0: np.ndarray):
    ranges = [range(i * 6 + 1, (i + 1) * 6) for i in range(0, 15)]
    for i, _range in enumerate(ranges):
        run(context=RunContext(
                task_id=0,
                queue=None,
                field_0=field_0,
                range=_range,
            ))


from typing import List

import numpy as np

from run import run, RunContext, Command


def solve(initial_field: List[List[int]]) -> List[Command]:
    field_0 = np.array(initial_field)
    ranges = [range(i * 6 + 1, (i + 1) * 6) for i in range(0, 15)]
    for i, _range in enumerate(ranges):
        result = run(context=RunContext(
                task_id=0,
                queue=None,
                field_0=field_0,
                range=_range,
            ))
        if result is not None:
            return result
    raise ValueError("field cannot be solved")

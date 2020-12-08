import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Queue, Manager
from typing import List

import numpy as np

from printer import start_printer
from run import RunContext, run, all_patterns


async def async_run(
        loop: AbstractEventLoop,
        executor: ProcessPoolExecutor,
        context: RunContext):
    return await loop.run_in_executor(
        executor,
        run,
        context)


async def async_solve(loop: AbstractEventLoop, field_0: np.ndarray, queue: Queue, n_process: int):
    t = all_patterns // n_process
    ranges = [range(i * t + 1, (i + 1) * t) for i in range(0, n_process)]
    tasks = []
    with ProcessPoolExecutor(max_workers=n_process) as executor:
        for i, _range in enumerate(ranges):
            tasks.append(asyncio.create_task(async_run(
                loop,
                executor,
                RunContext(
                    task_id=i,
                    queue=queue,
                    field_0=field_0,
                    range=_range,
                ))))
        return await asyncio.gather(*tasks)


_initial_field = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
]


def solve_multiprocess(initial_field: List[List[int]], n_process):
    manager = Manager()
    queue = manager.Queue()
    close_printer = start_printer(queue=queue, lines=n_process)
    _loop = asyncio.get_event_loop()
    results = _loop.run_until_complete(async_solve(_loop, np.array(initial_field), queue=queue, n_process=n_process))
    close_printer()
    print(list(filter(lambda r: r is not None, results))[0])


if __name__ == '__main__':
    solve_multiprocess(_initial_field, n_process=6)

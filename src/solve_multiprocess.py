import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures.process import ProcessPoolExecutor
from typing import List

import numpy as np

from message_queue import MessageQueue
from printer import Printer
from run import RunContext, run, all_patterns, Command


async def _async_run(
        loop: AbstractEventLoop,
        executor: ProcessPoolExecutor,
        context: RunContext):
    return await loop.run_in_executor(
        executor,
        run,
        context)


async def _async_solve(loop: AbstractEventLoop, field_0: np.ndarray, queue: MessageQueue, n_process: int):
    t = all_patterns // n_process
    ranges = [range(i * t + 1, (i + 1) * t) for i in range(0, n_process)]
    tasks = []
    with ProcessPoolExecutor(max_workers=n_process) as executor:
        for i, _range in enumerate(ranges):
            tasks.append(asyncio.create_task(_async_run(
                loop,
                executor,
                RunContext(
                    task_id=i,
                    queue=queue,
                    field_0=field_0,
                    range=_range,
                ))))
        return await asyncio.gather(*tasks)


def solve_multiprocess(initial_field: List[List[int]], n_process, debug_print: bool) -> List[Command]:
    with Printer(lines=n_process, debug_print=debug_print) as p:
        _loop = asyncio.get_event_loop()
        results = _loop.run_until_complete(
            _async_solve(_loop, np.array(initial_field), queue=p.queue, n_process=n_process))
    return list(list(filter(lambda r: r is not None, results))[0])

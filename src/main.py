import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures.process import ProcessPoolExecutor

import numpy as np

from printer import Printer
from run import RunContext, run


async def async_run(
        loop: AbstractEventLoop,
        executor: ProcessPoolExecutor,
        context: RunContext):
    return await loop.run_in_executor(
        executor,
        run,
        context)


async def async_solve(loop: AbstractEventLoop, field_0: np.ndarray, printer: Printer):
    ranges = [range(i * 6 + 1, (i + 1) * 6) for i in range(0, 15)]
    tasks = []
    with ProcessPoolExecutor(max_workers=16) as executor:
        for i, _range in enumerate(ranges):
            tasks.append(asyncio.create_task(async_run(
                loop,
                executor,
                RunContext(
                    task_no=i,
                    printer=printer,
                    field_0=field_0,
                    range=_range,
                ))))
        await asyncio.gather(*tasks)


_initial_field = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
]


if __name__ == '__main__':
    p = Printer(16)
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(async_solve(_loop, np.array(_initial_field), printer=p))
    p.finalize()

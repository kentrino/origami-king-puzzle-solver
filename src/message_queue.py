from multiprocessing import Manager
from typing import Tuple, List

STOP = "___STOP___"
MESSAGE = "___MESSAGE___"


class MessageQueue(object):
    def __init__(self, debug_print: bool):
        self.queue = Manager().Queue()
        self.debug_print = debug_print

    def get(self) -> Tuple[str, any, int]:
        return self.queue.get()

    def debug(self, commands: any, task_id: int):
        if self.debug_print:
            self.queue.put((MESSAGE, commands, task_id))

    def stop(self):
        self.queue.put((STOP, [], -1))

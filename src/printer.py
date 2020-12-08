import sys
from multiprocessing.context import Process
from multiprocessing import Queue

from message_queue import MessageQueue, STOP


def _print_runner(queue: Queue, lines: int):
    printer = Printer(lines=lines, queue=queue)
    printer.run()


class PrinterStarter(object):
    def __init__(self, queue: MessageQueue, lines: int, debug_print: bool):
        self.queue = queue
        self.lines = lines
        self.debug_print = debug_print

    def __enter__(self):
        if self.debug_print:
            self.process = Process(target=_print_runner, args=(self.queue, self.lines))
            self.process.start()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.debug_print:
            self.queue.stop()
            self.process.join()
            self.process.close()


def _down(n: int):
    if n == 0:
        return
    cursor_up = "\x1b[{}B".format(n)
    sys.stdout.write(cursor_up)


def _up(n: int):
    if n == 0:
        return
    cursor_up = "\x1b[{}A".format(n)
    sys.stdout.write(cursor_up)


def _clear():
    sys.stdout.write("\x1b[0J")


move_left_most = "\x1b[1000D"
erase_line = '\x1b[K'


class Printer(object):
    def __init__(self, lines: int, queue: Queue):
        self.lines = lines
        for i in range(0, lines):
            print("")
        _up(lines)
        self.queue = queue

    def run(self):
        while True:
            _type, message, i = self.queue.get()
            if _type == STOP:
                break
            self.show(message, i)
        _clear()

    def show(self, message: any, i: int):
        if i >= self.lines:
            return
        _down(i)
        sys.stdout.write(erase_line)
        sys.stdout.write(str(message))
        sys.stdout.write(move_left_most)
        _up(i)

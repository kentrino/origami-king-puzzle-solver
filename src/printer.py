import sys
from multiprocessing.context import Process
from multiprocessing import Queue

STOP = "___STOP___"


def _print_runner(queue: Queue, lines: int):
    printer = Printer(lines=lines, queue=queue)
    printer.run()


def start_printer(queue, lines):
    p = Process(target=_print_runner, args=(queue, lines))
    p.start()

    def stop():
        queue.put((STOP, 0))
        p.join()
        p.close()
    return stop


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
            message, i = self.queue.get()
            if message == STOP:
                break
            self.show(message, i)
        _clear()

    def show(self, message, i: int):
        if i >= self.lines:
            return
        _down(i)
        sys.stdout.write(erase_line)
        sys.stdout.write(str(message))
        sys.stdout.write(move_left_most)
        _up(i)

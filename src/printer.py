import sys
import threading


class Printer(object):
    def __init__(self, lines: int):
        pass
        self.lines = lines
        # for i in range(0, lines):
        #     print("---")
        # self.up(lines)
        # self.lock = threading.Lock()

    def up(self, n: int):
        cursor_up = "\x1b[{}A".format(n)
        sys.stdout.write(cursor_up)
        # erase_line = '\x1b[2K'
        # for i in range(0, n):
        #     sys.stdout.write(cursor_up_one)

    def down(self, n: int):
        cursor_up = "\x1b[{}B".format(n)
        sys.stdout.write(cursor_up)

    def show(self, message, i: int):
        if i >= self.lines:
            return
        # self.lock.acquire()
        self.down(i)
        # erase_line = '\x1b[2K'
        move_left_most = "\x1b[1000D"
        erase_line = '\x1b[K'
        sys.stdout.write(move_left_most)
        sys.stdout.write(erase_line)
        sys.stdout.write(message)
        self.up(i)
        # self.lock.release()

    def finalize(self):
        self.down(self.lines)

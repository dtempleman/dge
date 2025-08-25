import numpy as np
from dge import logger
from datetime import datetime
import curses


class Renderer:
    def __init__(self, width: int = 10, height: int = 10) -> None:
        self.window = curses.initscr()
        curses.noecho()

        self.width: int = width
        self.height: int = height
        self.log_len = 5
        self.render_buffer = [
            [[] for _ in range(self.width)] for _ in range(self.height)
        ]

        self.start_time = datetime.now()

    def render(self, sprite: str, coords: np.ndarray):
        self.render_buffer[coords[1]][coords[0]].append(sprite)

    def clean_render_buffer(self):
        self.render_buffer = [
            [[] for _ in range(self.width)] for _ in range(self.height)
        ]

    def draw_logs(self):

        for i, message in enumerate(logger.log_stack):
            self.window.addstr(self.width + i + 1, 0, message)

    def draw_board(self):
        for x in range(len(self.render_buffer)):
            for y in range(len(self.render_buffer[x])):
                if len(self.render_buffer[x][y]) > 0:
                    self.window.addstr(y, x, "".join(self.render_buffer[x][y]))
                else:
                    self.window.addstr(y, x, ".")
        self.clean_render_buffer()

    def draw_time(self):
        self.window.addstr(
            self.width + len(logger.log_stack) + 1,
            0,
            str(datetime.now() - self.start_time),
        )

    def draw(self):
        self.window.clear()
        self.draw_board()
        self.draw_logs()
        self.draw_time()
        self.window.refresh()

    def teardown(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

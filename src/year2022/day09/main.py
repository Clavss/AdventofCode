from __future__ import annotations

import os
from dataclasses import dataclass

from utils.exercise import Exercise


@dataclass
class Coord:
    x: int
    y: int


class Problem(Exercise):
    grid = None
    rope = None

    def set_debug(self, debug=True) -> None:
        self.debug = debug

    def part1(self, data: list[str]) -> int | str:
        # Create a set to save coord visited by the tail
        self.grid: set[str] = set()
        # Init head and tail at 0
        self.init_rope(2)

        for line in data:
            move, quantity = line.split()
            for _ in range(int(quantity)):
                self.move_head(move)
                self.move_tails()
                self.save_tail_coord()

        return len(self.grid)

    def init_rope(self, length: int) -> None:
        self.rope = [Coord(0, 0) for _ in range(length)]

    def move_head(self, move: str) -> None:
        match move:
            case 'L':
                self.move_head_left()
            case 'R':
                self.move_head_right()
            case 'U':
                self.move_head_up()
            case 'D':
                self.move_head_down()

    def move_tails(self) -> None:
        for index in range(1, len(self.rope)):
            self.move_tail(index)

    def move_tail(self, tail_index: int) -> None:
        head = self.rope[tail_index - 1]
        tail = self.rope[tail_index]
        dx = head.x - tail.x
        dy = head.y - tail.y
        if (dx == 0) and (abs(dy) > 1):
            self.move_tail_down(tail_index) if dy > 0 else self.move_tail_up(tail_index)
        elif (dy == 0) and (abs(dx) > 1):
            self.move_tail_right(tail_index) if dx > 0 else self.move_tail_left(tail_index)
        elif (abs(dx) > 1) or (abs(dy) > 1):
            self.move_tail_down(tail_index) if dy > 0 else self.move_tail_up(tail_index)
            self.move_tail_right(tail_index) if dx > 0 else self.move_tail_left(tail_index)

    def get_head(self) -> Coord:
        return self.rope[0]

    def get_tail(self) -> Coord:
        return self.rope[-1]

    @Exercise.stack
    def move_head_left(self) -> None:
        head = self.get_head()
        head.x -= 1

    @Exercise.stack
    def move_head_right(self) -> None:
        head = self.get_head()
        head.x += 1

    @Exercise.stack
    def move_head_up(self) -> None:
        head = self.get_head()
        head.y -= 1

    @Exercise.stack
    def move_head_down(self) -> None:
        head = self.get_head()
        head.y += 1

    def save_tail_coord(self) -> None:
        tail = self.get_tail()
        self.grid.add(f'{tail.x};{tail.y}')

    @Exercise.stack
    def move_tail_left(self, tail_index: int) -> None:
        self.rope[tail_index].x -= 1

    @Exercise.stack
    def move_tail_right(self, tail_index: int) -> None:
        self.rope[tail_index].x += 1

    @Exercise.stack
    def move_tail_up(self, tail_index: int) -> None:
        self.rope[tail_index].y -= 1

    @Exercise.stack
    def move_tail_down(self, tail_index: int) -> None:
        self.rope[tail_index].y += 1

    def part2(self, data: list[str]) -> int | str:
        # Create a set to save coord visited by the tail
        self.grid: set[str] = set()
        # Init head and tails at 0
        self.rope = [Coord(0, 0) for _ in range(10)]

        for line in data:
            move, quantity = line.split()
            for _ in range(int(quantity)):
                self.move_head(move)
                self.move_tails()
                self.save_tail_coord()

        return len(self.grid)


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

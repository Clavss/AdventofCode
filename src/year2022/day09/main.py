from __future__ import annotations

import os
from dataclasses import dataclass

from utils.common import stack
from utils.exercise import Exercise


@dataclass
class Coord:
    x: int
    y: int


class Problem(Exercise):
    grid = None
    head = None
    tail = None
    debug = False

    def part1(self, data: list[str]) -> int | str:
        # Create a dict to save coord visited by the tail
        self.grid: set[str] = set()
        # Init head and tail at 0
        self.head = Coord(0, 0)
        self.tail = Coord(0, 0)

        for line in data:
            move, quantity = line.split()
            for _ in range(int(quantity)):
                self.move_head(move)
                self.move_tail()
                self.save_tail_coord()

        return len(self.grid)

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

    def move_tail(self) -> None:
        dx = self.head.x - self.tail.x
        dy = self.head.y - self.tail.y
        if (dx == 0) and (abs(dy) > 1):
            self.move_tail_down() if dy > 0 else self.move_tail_up()
        elif (dy == 0) and (abs(dx) > 1):
            self.move_tail_right() if dx > 0 else self.move_tail_left()
        elif (abs(dx) > 1) or (abs(dy) > 1):
            self.move_tail_down() if dy > 0 else self.move_tail_up()
            self.move_tail_right() if dx > 0 else self.move_tail_left()

    @stack(debug=debug)
    def move_head_left(self) -> None:
        self.head.x -= 1

    @stack(debug=debug)
    def move_head_right(self) -> None:
        self.head.x += 1

    @stack(debug=debug)
    def move_head_up(self) -> None:
        self.head.y -= 1

    @stack(debug=debug)
    def move_head_down(self) -> None:
        self.head.y += 1

    def save_tail_coord(self) -> None:
        self.grid.add(f'{self.tail.x};{self.tail.y}')

    @stack(debug=debug)
    def move_tail_left(self) -> None:
        self.tail.x -= 1

    @stack(debug=debug)
    def move_tail_right(self) -> None:
        self.tail.x += 1

    @stack(debug=debug)
    def move_tail_up(self) -> None:
        self.tail.y -= 1

    @stack(debug=debug)
    def move_tail_down(self) -> None:
        self.tail.y += 1

    def part2(self, data: list[str]) -> int | str:
        return 0


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

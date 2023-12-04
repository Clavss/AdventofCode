import functools
import os
import re

from utils.exercise import Exercise


def is_adjacent_to_symbol(pos: complex, num: int, data: list[str]) -> bool:
    length = len(data[0])
    height = len(data)
    start_y = int(pos.imag) - 1
    end_y = int(pos.imag) + 1
    start_x = int(pos.real) - 1
    end_x = start_x + len(str(num)) + 1

    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            # outside the grid
            if x < 0 or x >= length or y < 0 or y >= height:
                continue
            # on the actual number
            if y == start_y + 1 and (start_x + 1 <= x <= end_x - 1):
                continue
            # supposing a number cannot be adjacent to another, this should be a symbol
            if data[y][x] != '.':
                return True

    return False


def find_adjacent_gears(pos: complex, num: int, data: list[str], gears: dict[complex, list[int]]) -> None:
    """Modify gears by adding the position of every gear and numbers adjacent to it."""
    length = len(data[0])
    height = len(data)
    start_y = int(pos.imag) - 1
    end_y = int(pos.imag) + 1
    start_x = int(pos.real) - 1
    end_x = start_x + len(str(num)) + 1

    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            # outside the grid
            if x < 0 or x >= length or y < 0 or y >= height:
                continue
            # on the actual number
            if y == start_y + 1 and (start_x + 1 <= x <= end_x - 1):
                continue
            # on a gear
            if data[y][x] == '*':
                gear_pos = complex(x, y)
                gears[gear_pos] = gears.get(gear_pos, []) + [num]


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total = 0
        # [(pos, num)]
        indexes: list[tuple[complex, int]] = []

        for y, line in enumerate(data):
            indexes += [(complex(m.start(), y), int(m.group(0))) for m in re.finditer(r'\d+', line)]

        for pos, num in indexes:
            if is_adjacent_to_symbol(pos, num, data):
                total += num

        return total

    def part2(self, data: list[str]) -> int | str:
        # [(pos, num)]
        indexes: list[tuple[complex, int]] = []
        # {pos: [adjacent nums]}
        gears: dict[complex, list[int]] = {}

        for y, line in enumerate(data):
            indexes += [(complex(m.start(), y), int(m.group(0))) for m in re.finditer(r'\d+', line)]

        for pos, num in indexes:
            find_adjacent_gears(pos, num, data, gears)

        gear_ratio = functools.reduce(lambda cnt, elm: cnt + ((elm[0] * elm[1]) if len(elm) == 2 else 0),
                                      gears.values(), 0)
        return gear_ratio


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

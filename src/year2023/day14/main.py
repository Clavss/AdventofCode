import os
from copy import copy
from functools import cache

from utils.exercise import Exercise


@cache
def tilt_line(line: str, reverse: bool) -> str:
    splited_line: list[str] = ''.join(line).split('#')
    sorted_line: list[str] = [''.join(sorted(part, reverse=reverse)) for part in splited_line]
    tilted_line: str = '#'.join(sorted_line)
    return tilted_line


def tilt_data(transposed_data: list[str], reverse: bool) -> list[str]:
    new_data = zip(*transposed_data)
    transposed_data: list[str] = []

    for line in new_data:
        tilted_line = tilt_line(line, reverse=reverse)
        transposed_data.append(tilted_line)

    return transposed_data


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total_north_load: int = 0
        transposed_data: list[str] = copy(data)

        # tilt north
        transposed_data = tilt_data(transposed_data, reverse=True)

        for index, line in enumerate(list(zip(*transposed_data))[::-1]):
            count = line.count('O')
            total_north_load += count * (index + 1)

        return total_north_load

    def part2(self, data: list[str]) -> int | str:
        total_north_load: int = 0
        transposed_data: list[str] = copy(data)
        save: list[str] = []
        cycle: int = 0

        # looking for a cycle
        while '-'.join(transposed_data) not in save:
            save.append('-'.join(transposed_data))
            cycle += 1
            # north
            transposed_data = tilt_data(transposed_data, reverse=True)
            # west
            transposed_data = tilt_data(transposed_data, reverse=True)
            # south
            transposed_data = tilt_data(transposed_data, reverse=False)
            # east
            transposed_data = tilt_data(transposed_data, reverse=False)

        first_cycle: int = save.index('-'.join(transposed_data))
        cycle_length: int = cycle - first_cycle
        equivalent_cycle: int = (1_000_000_000 - first_cycle) % cycle_length + first_cycle

        state_at_1md = save[equivalent_cycle].split('-')
        for index, line in enumerate(state_at_1md[::-1]):
            count = line.count('O')
            total_north_load += count * (index + 1)

        return total_north_load


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

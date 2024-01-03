import os

from utils.common import value_at, replace_str_at, get_adjacent_positions
from utils.exercise import Exercise


def create_terrain(trench: set[complex]) -> list[str]:
    trench_list = list(trench)
    min_x: int = int(min(trench_list, key=lambda pos: pos.real).real)
    max_x: int = int(max(trench_list, key=lambda pos: pos.real).real)
    min_y: int = int(min(trench_list, key=lambda pos: pos.imag).imag)
    max_y: int = int(max(trench_list, key=lambda pos: pos.imag).imag)
    terrain: list[str] = []

    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if complex(x, y) in trench:
                line += '#'
            else:
                line += '.'
        terrain.append(line)

    return terrain


def show_terrain(terrain: list[str]) -> None:
    for line in terrain:
        print(line)


def create_interior(terrain: list[str], start: complex) -> set[complex]:
    """Visit every position inside the trench iteratively from start and return them as a set."""
    seen: set[complex] = set()
    to_visit: set[complex] = {start}
    next_pos: complex

    while len(to_visit) > 0:
        next_pos = to_visit.pop()
        if next_pos in seen:
            continue

        seen.add(next_pos)

        adjacent_positions = get_adjacent_positions(next_pos)
        for adjacent_position in adjacent_positions:
            if value_at(terrain, adjacent_position) == '.':
                to_visit.add(adjacent_position)

    return seen


def update_terrain_with_interior(terrain: list[str], interior: set[complex]) -> None:
    for pos in interior:
        x: int = int(pos.real)
        y: int = int(pos.imag)
        terrain[y] = replace_str_at(terrain[y], x, '#')


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        count: int
        position: complex = 0j
        trench: set[complex] = {position}
        position_delta: dict[str, complex] = {'U': 0 - 1j, 'D': 0 + 1j, 'L': -1 + 0j, 'R': 1 + 0j}

        for line in data:
            split: list[str] = line.split(' ')
            direction: str = split[0]
            distance: int = int(split[1])

            for i in range(distance):
                position += position_delta[direction]
                trench.add(position)

        terrain: list[str] = create_terrain(trench)
        # show_terrain(terrain)

        # find the first (most top-left) position inside the trench
        start: complex = terrain[0].index('#') + (1 + 1j)
        interior: set[complex] = create_interior(terrain, start)

        update_terrain_with_interior(terrain, interior)
        # show_terrain(terrain)

        count = len(trench) + len(interior)
        return count

    def part2(self, data: list[str]) -> int | str:
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

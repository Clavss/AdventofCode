import math
import os
from dataclasses import dataclass

from utils.exercise import Exercise


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def coords_between(coord1: Coord, coord2: Coord) -> list[Coord]:
    # suppose both coords are aligned
    res = [coord1, coord2]
    if coord1.x == coord2.x:
        y_min = min(coord1.y, coord2.y)
        y_max = max(coord1.y, coord2.y)
        for y in range(y_min + 1, y_max):
            res.append(Coord(coord1.x, y))
    else:  # coord1.y == coord2.y
        x_min = min(coord1.x, coord2.x)
        x_max = max(coord1.x, coord2.x)
        for x in range(x_min + 1, x_max):
            res.append(Coord(x, coord1.y))

    return res


class Problem(Exercise):
    # use a dict to avoid creating a list too big with a lot of unused indexes
    cave: dict[Coord, str]
    min_x: int | float
    max_x: int
    max_y: int
    sand_start: Coord

    def resolve(self, data: list[str], void: bool) -> int:
        self.init_cave(data)
        max_sand_units = self.simulate_sand(void=void)

        self.print_cave(void=void)
        return max_sand_units

    def part1(self, data: list[str]) -> int | str:
        max_sand_units = self.resolve(data, True)
        return max_sand_units

    def part2(self, data: list[str]) -> int | str:
        max_sand_units = self.resolve(data, False)
        return max_sand_units

    def init_cave(self, data: list[str]) -> None:
        self.cave = {}
        self.min_x = math.inf
        self.max_x = 0
        self.max_y = 0
        self.sand_start = Coord(500, 0)
        last_coord = None

        for line in data:
            split = line.split(' -> ')
            for index, coord_str in enumerate(split):
                _split = coord_str.split(',')
                x, y = int(_split[0]), int(_split[1])

                self.min_x = min(x, self.min_x)
                self.max_x = max(x, self.max_x)
                self.max_y = max(y, self.max_y)

                coord = Coord(x, y)
                if index != 0:
                    # place rocks between the 2 coordinates
                    self.place_rock_between(last_coord, coord)

                last_coord = coord

    def simulate_sand(self, void: bool) -> int:
        sand_counter = 0
        is_in_void = False
        full = not void
        is_full = False

        while (void and not is_in_void) or (full and not is_full):
            sand_unit_x, sand_unit_y = self.sand_start.x, self.sand_start.y
            while True:
                # in void, stop
                if void and (not self.min_x <= sand_unit_x <= self.max_x or self.max_y < sand_unit_y):
                    is_in_void = True
                    break

                # in void, expand x limits
                if full:
                    self.min_x = min(sand_unit_x, self.min_x)
                    self.max_x = max(sand_unit_x, self.max_x)

                # on floor
                if full and sand_unit_y == self.max_y + 1:
                    sand_counter += 1
                    break

                # move down
                if self.cave.get(Coord(sand_unit_x, sand_unit_y + 1), None) is None:
                    sand_unit_y += 1
                # move down left
                elif self.cave.get(Coord(sand_unit_x - 1, sand_unit_y + 1), None) is None:
                    sand_unit_x -= 1
                    sand_unit_y += 1
                # move down right
                elif self.cave.get(Coord(sand_unit_x + 1, sand_unit_y + 1), None) is None:
                    sand_unit_x += 1
                    sand_unit_y += 1
                # cannot move further down
                else:
                    sand_counter += 1
                    break

            sand_coord = Coord(sand_unit_x, sand_unit_y)
            if sand_coord == self.sand_start:
                is_full = True
            else:
                self.cave[sand_coord] = 'o'

        return sand_counter

    def print_cave(self, void: bool) -> None:
        for y in range(self.max_y + 1 + 1 * (not void)):
            for x in range(self.min_x, self.max_x + 1):
                coord = Coord(x, y)
                if coord == self.sand_start:
                    print('+', end='')
                else:
                    print(self.cave.get(coord, '.'), end='')
            print()

        if not void:
            print('#' * (self.max_x - self.min_x + 1))

    def place_rock_between(self, coord1: Coord, coord2: Coord) -> None:
        for coord_between in coords_between(coord1, coord2):
            self.cave[coord_between] = '#'
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

import math
import os
from dataclasses import dataclass

from utils.common import get_adjacent_positions, value_at, is_in_grid
from utils.exercise import Exercise


def find_start(data: list[str]) -> complex:
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 'S':
                return complex(x, y)


def get_next_positions(data: list[str], position: complex, part: int) -> list[complex]:
    res: list[complex] = []
    adjacent_positions: list[complex] = get_adjacent_positions(position)

    if part == 1:
        for position in adjacent_positions:
            if is_in_grid(data, position) and value_at(data, position) in 'S.':
                res.append(position)
    else:  # part == 2
        for position in adjacent_positions:
            x: int = int(position.real) % len(data[0])
            y: int = int(position.imag) % len(data)
            centered_position: complex = complex(x, y)
            if value_at(data, centered_position) in 'S.':
                res.append(position)

    return res


@dataclass
class PositionDistance:
    position: complex
    distance: int = 0


def find_plots(data: list[str], start_position: complex, max_steps: int, part: int) -> set[complex]:
    plots: set[complex] = set()
    seen: dict[complex, int] = {start_position: 0}
    queue: list[PositionDistance] = [PositionDistance(start_position, 0)]

    while len(queue) > 0:
        position_distance: PositionDistance = queue.pop()

        if position_distance.distance > max_steps:
            continue

        next_positions: list[complex] = get_next_positions(data, position_distance.position, part)
        for position in next_positions:
            previous_distance: int | None = seen.get(position, None)
            if previous_distance is None or previous_distance > position_distance.distance + 1:
                queue.append(PositionDistance(position, position_distance.distance + 1))
                seen[position] = position_distance.distance + 1

        if (max_steps - position_distance.distance) % 2 == 0 and position_distance.position not in plots:
            plots.add(position_distance.position)

    return plots


def print_plots(data: list[str], plots: set[complex]) -> None:
    for y in range(len(data)):
        for x in range(len(data[0])):
            if complex(x, y) in plots:
                print('O', end='')
            else:
                print(data[y][x], end='')
        print()


def calculate_nb_plots(cycles: int) -> int:
    square_side: float = math.pow(cycles * 2 + 1, 2) / 2
    x: int = math.ceil(square_side)
    y: int = x - 1
    n: int = cycles - 3
    z: int = (int(n * (n + 1) // 2) - 3) * -1
    res: int = 3882 * x + int(3738.25 * y) + 39 * z
    return res


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        start_position: complex = find_start(data)
        plots: set[complex] = find_plots(data, start_position, 64, 1)

        res: int = len(plots)
        print_plots(data, plots)

        return res

    def part2(self, data: list[str]) -> int | str:
        res: int = calculate_nb_plots(202300)
        return res


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_part(1, True)
    problem.exec_part(2, False)


if __name__ == "__main__":
    main()

# 26501365 = 2023*100*131+65

# 0*131+65 =  65 ->   3882 =   1*3882               =   1*3882 +   0*3738.25 + 0*39 =   1*3882 +  0*14953 + 0*39
# 1*131+65 = 196 ->  34441 =   5*3882 +   4*b + x*c =   5*3882 +   4*3738.25 + 2*39 =   5*3882 +  1*14953 + 2*39
# 2*131+65 = 327 ->  95442 =  13*3882 +  12*b + x*c =  13*3882 +  12*3738.25 + 3*39 =  13*3882 +  3*14953 + 3*39
# 3*131+65 = 458 -> 186885 =  25*3882 +  24*b + x*c =  25*3882 +  24*3738.25 + 3*39 =  25*3882 +  6*14953 + 3*39
# 4*131+65 = 589 -> 308770 =  41*3882 +  40*b + x*c =  41*3882 +  40*3738.25 + 2*39 =  41*3882 + 10*14953 + 2*39
# 5*131+65 = 720 -> 461097 =  61*3882 +  60*b + x*c =  61*3882 +  60*3738.25 + 0*39 =  61*3882 + 15*14953 + 0*39
# 6*131+65 = 851 -> 643866 =  85*3882 +  84*b + x*c =  85*3882 +  84*3738.25 - 3*39 =  85*3882 + 21*14953 - 3*39
# 7*131+65 = 982 -> 857077 = 113*3882 + 112*b + x*c = 113*3882 + 112*3738.25 - 7*39 = 113*3882 + 28*14953 - 7*39
# ...
# 2023*100*131+65 = 26501365 -> ?     = 81850984601*3882 + 81850984600*3738.25 + x*39
#                                     = 81850984601*3882 + 20462746150*14953   + x*39 --> x should be even

# { 34441 - 5*3882 = 15031 = 4*b + x*c }
# { 95442 - 13*3882 = 44976 = 12*b + x*c }
# { 186885 - 25*3882 = 89835 = 24*b + x*c }

# 3882  = 2 × 3 × 647
# 14953 = 19 × 787
# 39    = 3 × 13

# a = 3882
# b = 3738.25 (= 14953 / 4)
# c = 39

# ................^................
# .....###.#...../###.#......###.#.
# .###.##..#..###.##\.#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#...../..#.#..\.....#.#....
# .##...####./##...####\.##...####.
# .##..#...#/.##..#...#.\##..#...#.
# .......##/........##...\.....##..
# .##.#.####..##.#.####..##.#.####.
# .##..##/##..##..##.##..##\.##.##.
# ....../...................\......
# ...../..........^..........\.....
# ..../###.#...../###.#......###.#.
# .###.##..#..###.##\.#..###.##\.#.
# ..#.#...#....#.#...#....#.#...#..
# ./..#.#...../..#.#..\.....#.#..\.
# <##...####.<##..S####>.##...####>
# .##..#...#..##..#...#..##..#...#.
# ..\....##....\....##.........##..
# .##.#.####..##\#.####..##.#.####.
# .##.\##.##..##.\##.##..##..##.##.
# .....\..........v........../.....
# ......\.................../......
# .....###.#......###.#..../.###.#.
# .###.##.\#..###.##..#..###.##..#.
# ..#.#...#\...#.#...#.../#.#...#..
# ....#.#...\....#.#..../...#.#....
# .##...####.\##...####/.##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##....\....##.........##..
# .##.#.####..##\#.####..##.#.####.
# .##..##.##..##.\##.##..##..##.##.
# ................v................

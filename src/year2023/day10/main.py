import os

from utils.exercise import Exercise


def find_start(data: list[str]) -> complex:
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == 'S':
                return complex(x, y)
    return 0j


def find_next_tile(data: list[str], current_tile: complex, from_tile: complex) -> complex:
    possible_next = []
    x = int(current_tile.real)
    y = int(current_tile.imag)
    # up
    if y > 0 and data[y - 1][x] in '|7FS' and data[y][x] in '|JLS':
        possible_next.append(complex(x, y - 1))
    # down
    if y < len(data) - 1 and data[y + 1][x] in '|JLS' and data[y][x] in '|7FS':
        possible_next.append(complex(x, y + 1))
    # left
    if x > 0 and data[y][x - 1] in '-LFS' and data[y][x] in '-J7S':
        possible_next.append(complex(x - 1, y))
    # right
    if x < len(data[0]) - 1 and data[y][x + 1] in '-J7S' and data[y][x] in '-LFS':
        possible_next.append(complex(x + 1, y))

    # there are always 2 connected tiles
    # removing the one we originate from
    try:
        possible_next.remove(from_tile)
    except ValueError:
        pass

    return possible_next[0]


def find_loop(data: list[str], start_pos: complex) -> list[complex]:
    loop = [start_pos]
    current_tile = start_pos
    next_tile = find_next_tile(data, current_tile, current_tile)
    while next_tile != start_pos:
        loop.append(next_tile)
        last_tile = current_tile
        current_tile = next_tile
        next_tile = find_next_tile(data, current_tile, last_tile)

    return loop


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        res = 0
        start_pos = find_start(data)
        loop = find_loop(data, start_pos)

        return len(loop) // 2

    def part2(self, data: list[str]) -> int | str:
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

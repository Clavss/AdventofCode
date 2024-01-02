import os
from typing import Iterable

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


def find_start_equivalent(data: list[str], start_pos: complex) -> str:
    x: int = int(start_pos.real)
    y: int = int(start_pos.imag)
    top: str = data[y - 1][x]
    down: str = data[y + 1][x]
    left: str = data[y][x - 1]
    right: str = data[y][x + 1]
    possibilities: str = 'F-L7J|'
    if top not in 'F7|':
        for char in 'LJ|':
            possibilities = possibilities.replace(char, '')
    if down not in 'LJ|':
        for char in 'F7|':
            possibilities = possibilities.replace(char, '')
    if left not in 'F-L':
        for char in '-7J':
            possibilities = possibilities.replace(char, '')
    if right not in '-7J':
        for char in 'F-L':
            possibilities = possibilities.replace(char, '')
    return possibilities


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


def get_ground(data: list[str], loop: Iterable[complex], in_pos: Iterable[complex] = None,
               out_pos: Iterable[complex] = None) -> list[str]:
    ground: list[str] = []
    for y in range(len(data)):
        line: str = ''
        for x in range(len(data[0])):
            pos = complex(x, y)
            if pos in loop:
                line += data[y][x]
            elif pos in in_pos:
                line += 'I'
            elif pos in out_pos:
                line += 'O'
            else:
                line += '.'
        ground.append(line)
    return ground


def get_in_and_out_pos(data: list[str], loop: set[complex], start_pos: complex) -> tuple[set[complex], set[complex]]:
    """Return a set of tile's position that are in the loop and a set of tile's position that are out the loop."""
    length: int = len(data[0])
    height: int = len(data)
    start_equivalent: str = find_start_equivalent(data, start_pos)
    start_block_index: int = -1
    end_block_index: int = -1
    in_pos: set[complex] = set()
    out_pos: set[complex] = set()

    for y in range(height):
        out: bool = True
        in_block: bool = False

        for x in range(length):
            char = data[y][x]
            pos = complex(x, y)

            if pos in loop:
                if char == 'S':
                    char = start_equivalent

                if char == '|':
                    out = not out
                    continue
                if char == '-':
                    continue

                if not in_block:
                    start_block_index = 'FL'.find(char)
                    in_block = start_block_index != -1
                else:  # in_block
                    end_block_index = '7J'.find(char)
                    if start_block_index != end_block_index:
                        out = not out
                    in_block = end_block_index == -1

            elif not out:  # pos not in loop
                in_pos.add(pos)
            elif out:  # pos not in loop
                out_pos.add(pos)

    return in_pos, out_pos


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        start_pos: complex = find_start(data)
        loop: list[complex] = find_loop(data, start_pos)

        return len(loop) // 2

    def part2(self, data: list[str]) -> int | str:
        # My thoughts:
        # visit every line from left to right
        # start as O (out), change from O to I (in) or from I to O when encountering a | or a reverse block
        # a block is a continuous path starting with F and ending with 7, or starting with L and ending with J
        # a block starting with F and ending with J, or starting with L and ending with 7 is a reverse block
        # a block can contain as many - as needed between his start and his end
        # only consider tile that are part of the loop

        start_pos: complex = find_start(data)
        # use a set to find elements in constant time
        loop: set[complex] = set(find_loop(data, start_pos))

        in_pos, out_pos = get_in_and_out_pos(data, loop, start_pos)

        count = len(in_pos)
        return count


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

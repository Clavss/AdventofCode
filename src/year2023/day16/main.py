import os
import sys
from enum import Enum

from utils.exercise import Exercise


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


def is_in_grid(pos: complex, data: list[str]) -> bool:
    x = int(pos.real)
    y = int(pos.imag)
    length = len(data[0])
    height = len(data)
    return 0 <= x < length and 0 <= y < height


def next_directions(curr_pos: complex, curr_direction: Direction, data: list[str]) -> list[Direction]:
    x = int(curr_pos.real)
    y = int(curr_pos.imag)
    symbol = data[y][x]

    match symbol:
        case '|':
            if curr_direction in [Direction.RIGHT, Direction.LEFT]:
                return [Direction.UP, Direction.DOWN]
            else:
                return [curr_direction]

        case '-':
            if curr_direction in [Direction.DOWN, Direction.UP]:
                return [Direction.LEFT, Direction.RIGHT]
            else:
                return [curr_direction]

        case '/':
            match curr_direction:
                case Direction.UP:
                    return [Direction.RIGHT]
                case Direction.LEFT:
                    return [Direction.DOWN]
                case Direction.DOWN:
                    return [Direction.LEFT]
                case Direction.RIGHT:
                    return [Direction.UP]

        case '\\':
            match curr_direction:
                case Direction.UP:
                    return [Direction.LEFT]
                case Direction.LEFT:
                    return [Direction.UP]
                case Direction.DOWN:
                    return [Direction.RIGHT]
                case Direction.RIGHT:
                    return [Direction.DOWN]

        case '.':
            return [curr_direction]


def next_positions(curr_pos: complex, new_directions: list[Direction]) -> list[complex]:
    res: list[complex] = []
    x = int(curr_pos.real)
    y = int(curr_pos.imag)

    for direction in new_directions:
        match direction:
            case Direction.RIGHT:
                res.append(complex(x + 1, y))
            case Direction.LEFT:
                res.append(complex(x - 1, y))
            case Direction.UP:
                res.append(complex(x, y - 1))
            case Direction.DOWN:
                res.append(complex(x, y + 1))

    return res


def visit(data: list[str], seen: dict[complex, set[Direction]], pos_dir: tuple[complex, Direction]) -> None:
    current_position, current_direction = pos_dir

    if current_position in seen.keys() and current_direction in seen[current_position]:
        return
    else:
        _dir = seen.get(current_position, set())
        _dir.add(current_direction)
        seen[current_position] = _dir

    new_directions = next_directions(current_position, current_direction, data)
    new_positions = next_positions(current_position, new_directions)

    for pos, direction in zip(new_positions, new_directions):
        if is_in_grid(pos, data):
            visit(data, seen, (pos, direction))


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total: int
        position_seen: dict[complex, set[Direction]] = {}
        start: tuple[complex, Direction] = (0j, Direction.RIGHT)

        visit(data, position_seen, start)

        total = len(position_seen)
        return total

    def part2(self, data: list[str]) -> int | str:
        position_seen: dict[complex, set[Direction]]
        starts: list[tuple[complex, Direction]] = []
        max_tiles: int = 0
        length = len(data[0])
        height = len(data)

        for x in range(length):
            starts.append((complex(x, 0), Direction.DOWN))
            starts.append((complex(x, height - 1), Direction.UP))
        for y in range(height):
            starts.append((complex(0, y), Direction.RIGHT))
            starts.append((complex(length - 1, y), Direction.LEFT))

        for start in starts:
            position_seen = {}
            visit(data, position_seen, start)
            max_tiles = max(max_tiles, len(position_seen))

        return max_tiles


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    sys.setrecursionlimit(4220)
    problem.exec_all(True)


if __name__ == "__main__":
    main()

import math
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
    x: int = int(pos.real)
    y: int = int(pos.imag)
    length: int = len(data[0])
    height: int = len(data)
    return 0 <= x < length and 0 <= y < height


def next_directions(data: list[str], position: complex, direction: Direction, consecutive: int) -> list[Direction]:
    directions: list[Direction] = []

    match direction:
        case Direction.RIGHT:
            directions.append(Direction.UP)
            directions.append(Direction.DOWN)
            directions.append(Direction.RIGHT)
        case Direction.LEFT:
            directions.append(Direction.UP)
            directions.append(Direction.DOWN)
            directions.append(Direction.LEFT)
        case Direction.DOWN:
            directions.append(Direction.LEFT)
            directions.append(Direction.RIGHT)
            directions.append(Direction.DOWN)
        case Direction.UP:
            directions.append(Direction.LEFT)
            directions.append(Direction.RIGHT)
            directions.append(Direction.UP)

    # cannot continue forward
    if consecutive >= 3:
        directions.pop()

    return directions


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


def opposite_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.RIGHT:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP


global_min = math.inf
global_min_printed = global_min


def visit(data: list[str],
          seen: dict[tuple[complex, Direction, int], int],
          position: complex,
          direction: Direction,
          consecutive: int,
          heat_loss: int) -> int | float:
    pos_dir_con: tuple[complex, Direction, int] = (position, direction, consecutive)
    length: int = len(data[0])
    height: int = len(data)

    # TODO: remove this
    if heat_loss >= 179_000:
        return math.inf

    if position == complex(length - 1, height - 1):
        global global_min
        global global_min_printed
        if heat_loss < global_min:
            if global_min_printed - heat_loss > 100:
                print(heat_loss)
                global_min_printed = heat_loss

            global_min = heat_loss
        return heat_loss

    # stop if similar (pos, dir, consecutive) and same or worst heat_loss
    for n in range(1, consecutive + 1):
        pos_dir_con = (position, direction, n)
        if pos_dir_con in seen.keys() and seen[pos_dir_con] <= heat_loss:
            return math.inf
    for n in range(1, 4):
        pos_opposite_dir_con = (position, opposite_direction(direction), n)
        if pos_opposite_dir_con in seen.keys() and seen[pos_opposite_dir_con] <= heat_loss:
            return math.inf

    seen[pos_dir_con] = heat_loss

    # 4 adjacent positions, minus previous one, minus forward if consecutive is 3
    new_directions: list[Direction] = next_directions(data, position, direction, consecutive)
    new_positions: list[complex] = next_positions(position, new_directions)
    min_heat_loss: int | float = math.inf

    for new_position, new_direction in zip(new_positions, new_directions):
        if not is_in_grid(new_position, data):
            continue

        x: int = int(new_position.real)
        y: int = int(new_position.imag)
        new_consecutive: int = consecutive + 1 if new_direction == direction else 1
        new_heat_loss: int = heat_loss + int(data[y][x])

        a = visit(data, seen, new_position, new_direction, new_consecutive, new_heat_loss)
        min_heat_loss: int = min(min_heat_loss, a)

    return min_heat_loss


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        heat_loss: int
        # {(pos, (dirs...), consecutive): heat_loss}
        position_seen: dict[tuple[complex, Direction, int], int] = {}

        heat_loss = visit(data, position_seen, 0j, Direction.RIGHT, 0, 0)

        return heat_loss

    def part2(self, data: list[str]) -> int | str:
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    sys.setrecursionlimit(100000)
    problem.exec_all(False)


if __name__ == "__main__":
    main()

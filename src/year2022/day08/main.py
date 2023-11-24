from __future__ import annotations

import os

from utils.exercise import Exercise


def is_border(x: int, y: int, length: int, height: int) -> bool:
    return (x in [0, length - 1]) or (y in [0, height - 1])


def is_visible_from_left(x: int, y: int, data: list[str]) -> bool:
    tree = data[y][x]
    # Lookup from 0 to x - 1 (every tree from left)
    for index in range(x):
        if data[y][index] >= tree:
            return False
    return True


def is_visible_from_right(x: int, y: int, limit: int, data: list[str]) -> bool:
    tree = data[y][x]
    # Lookup from x + 1 to limit (every tree from right)
    for index in range(x + 1, limit):
        if data[y][index] >= tree:
            return False
    return True


def is_visible_from_top(x: int, y: int, data: list[str]) -> bool:
    tree = data[y][x]
    # Lookup from 0 to y - 1 (every tree from top)
    for index in range(y):
        if data[index][x] >= tree:
            return False
    return True


def is_visible_from_bottom(x: int, y: int, limit: int, data: list[str]) -> bool:
    tree = data[y][x]
    # Lookup from y + 1 to limit (every tree from bottom)
    for index in range(y + 1, limit):
        if data[index][x] >= tree:
            return False
    return True


def is_visible(x: int, y: int, length: int, height: int, data: list[str]) -> bool:
    from_left = is_visible_from_left(x, y, data)
    from_right = is_visible_from_right(x, y, length, data)
    from_top = is_visible_from_top(x, y, data)
    from_bottom = is_visible_from_bottom(x, y, height, data)
    return any([from_left, from_right, from_top, from_bottom])


def scenic_score_from_left(x: int, y: int, data: list[str]) -> int:
    res = 0
    tree = data[y][x]
    # from x - 1 to 0
    for index in range(x - 1, -1, -1):
        res += 1
        if data[y][index] >= tree:
            return res
    return res


def scenic_score_from_right(x: int, y: int, limit: int, data: list[str]) -> int:
    res = 0
    tree = data[y][x]
    # from x + 1 to limit
    for index in range(x + 1, limit):
        res += 1
        if data[y][index] >= tree:
            return res
    return res


def scenic_score_from_top(x: int, y: int, data: list[str]) -> int:
    res = 0
    tree = data[y][x]
    # from y - 1 to 0
    for index in range(y - 1, -1, -1):
        res += 1
        if data[index][x] >= tree:
            return res
    return res


def scenic_score_from_bottom(x: int, y: int, limit: int, data: list[str]) -> int:
    res = 0
    tree = data[y][x]
    # from y + 1 to limit
    for index in range(y + 1, limit):
        res += 1
        if data[index][x] >= tree:
            return res
    return res


def scenic_score(x: int, y: int, length: int, height: int, data: list[str]) -> int:
    from_left = scenic_score_from_left(x, y, data)
    from_right = scenic_score_from_right(x, y, length, data)
    from_top = scenic_score_from_top(x, y, data)
    from_bottom = scenic_score_from_bottom(x, y, height, data)
    return from_left * from_right * from_top * from_bottom


class Problem(Exercise):
    def part1(self, data: list[str]) -> int | str:
        length = len(data[0])
        height = len(data)
        count = 0
        # Iterate over each tree
        for y in range(height):
            for x in range(length):
                if is_border(x, y, length, height) or is_visible(x, y, length, height, data):
                    count += 1

        return count

    def part2(self, data: list[str]) -> int | str:
        length = len(data[0])
        height = len(data)
        max_scenic_score = 0
        # Iterate over each tree
        for y in range(height):
            for x in range(length):
                current_scenic_score = scenic_score(x, y, length, height, data)
                if current_scenic_score > max_scenic_score:
                    max_scenic_score = current_scenic_score

        return max_scenic_score


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

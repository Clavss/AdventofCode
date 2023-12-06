import math
import os
import re

from utils.exercise import Exercise


def solve2eq(a: int, b: int, c: int) -> tuple[float, float]:
    delta = b ** 2 - 4 * a * c
    # suppose it should always exist 2 solutions
    if delta <= 0:
        raise RuntimeWarning

    x1 = (-b + math.sqrt(delta)) / 2 * a
    x2 = (-b - math.sqrt(delta)) / 2 * a
    if x2 < x1:
        x1, x2 = x2, x1

    return x1, x2


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        ways = 1
        times, distances = [[int(num) for num in re.findall(r'\d+', line)] for line in data]

        for i in range(len(times)):
            time, distance = times[i], distances[i]
            res = solve2eq(-1, time, -distance)

            # min has to be rounded up and max down (both exclusive if there are representing ints)
            _min = math.floor(res[0] + 1)
            _max = math.ceil(res[1] - 1)
            ways *= _max - _min + 1

        return ways

    def part2(self, data: list[str]) -> int | str:
        ways = 1
        time, distance = [int(''.join(re.findall(r'\d+', line))) for line in data]

        res = solve2eq(-1, time, -distance)

        # min has to be rounded up and max down (both exclusive if there are representing ints)
        _min = math.floor(res[0] + 1)
        _max = math.ceil(res[1] - 1)
        ways *= _max - _min + 1

        return ways


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

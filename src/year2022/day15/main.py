import math
import os
import re

from utils.exercise import Exercise


def dist(a: complex, b: complex) -> int:
    """Manhattan distance between 2 coords as complex numbers."""
    dx = int(a.real - b.real)
    dy = int(a.imag - b.imag)
    return abs(dx) + abs(dy)


def nearest_sensor(n: complex, sensors_dist: dict[complex, int]) -> complex:
    min_distance = math.inf
    nearest_s = None
    for sensor in sensors_dist.keys():
        distance = dist(n, sensor)
        if distance < min_distance:
            min_distance = distance
            nearest_s = sensor

    return nearest_s


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total = 0
        coords = []
        min_x = math.inf
        max_x = 0
        sensors_radius: dict[complex, int] = {}
        row = int(data[0])

        for line in data[1:]:
            # parsing with regex
            sx, sy, bx, by = [int(s) for s in re.findall(r'\d+', line)]
            # simulating coordinates using complex numbers
            s, b = complex(sx, sy), complex(bx, by)
            coords.append((s, b))
            d = dist(s, b)
            sensors_radius[s] = d

            min_x = min(min_x, sx - d)
            max_x = max(max_x, sx + d)

        for n in range(min_x, max_x + 1):
            n_coord = complex(n, row)

            for sensor, radius in sensors_radius.items():
                # is in sensor radius and is not on a beacon
                if dist(n_coord, sensor) <= radius and (n_coord not in [beacon for sensor, beacon in coords]):
                    total += 1
                    break

        return total

    def part2(self, data: list[str]) -> int | str:
        # 16_000_000_000_000
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

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


def is_beacon(coord: complex, coords: list[tuple[complex, complex]]) -> bool:
    return coord in [beacon for sensor, beacon in coords]


def is_in_radius(coord: complex, sensors_radius: dict[complex, int]) -> bool:
    for sensor, radius in sensors_radius.items():
        # is in any sensor radius
        if dist(coord, sensor) <= radius:
            return True
    return False


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
            sx, sy, bx, by = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
            # simulating coordinates using complex numbers
            s, b = complex(sx, sy), complex(bx, by)
            coords.append((s, b))
            d = dist(s, b)
            sensors_radius[s] = d

            min_x = min(min_x, sx - d)
            max_x = max(max_x, sx + d)

        for n in range(min_x, max_x + 1):
            n_coord = complex(n, row)

            if is_in_radius(n_coord, sensors_radius) and not is_beacon(n_coord, coords):
                total += 1

        return total

    def part2(self, data: list[str]) -> int | str:
        coords = []
        sensors_radius: dict[complex, int] = {}
        row = int(data[0])
        max_xy = row * 2

        for line in data[1:]:
            # parsing with regex
            sx, sy, bx, by = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
            # simulating coordinates using complex numbers
            s, b = complex(sx, sy), complex(bx, by)
            coords.append((s, b))
            d = dist(s, b)
            sensors_radius[s] = d

        # loop over coords at radius + 1 distance from every sensor
        for sensor, radius in sensors_radius.items():
            distance = radius + 1
            for dx in range(-distance, distance + 1):
                dy = distance - abs(dx)

                for i in [-1, 1]:
                    dy *= i
                    coord = sensor + complex(dx, dy)

                    if not coord.imag >= 0 <= coord.real <= max_xy >= coord.imag:
                        continue

                    if not is_in_radius(coord, sensors_radius) and not is_beacon(coord, coords):
                        return int(coord.real * 4_000_000 + coord.imag)

        return 0


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

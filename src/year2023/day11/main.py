import os

from utils.exercise import Exercise


def nb_empty_line_between(x1: int, x2: int, empty_line: list[int]) -> int:
    total = 0

    for line in empty_line:
        if x1 < line < x2:
            total += 1

    return total


def expanded_dist(g1: complex, g2: complex, empty_columns: list[int], empty_rows: list[int], part2: bool) -> int:
    x_min = min(int(g1.real), int(g2.real))
    x_max = max(int(g1.real), int(g2.real))
    y_min = min(int(g1.imag), int(g2.imag))
    y_max = max(int(g1.imag), int(g2.imag))

    dist = x_max - x_min + y_max - y_min
    nb_empty_columns = nb_empty_line_between(x_min, x_max, empty_columns)
    nb_empty_rows = nb_empty_line_between(y_min, y_max, empty_rows)

    if part2:
        nb_empty_columns *= 999_999
        nb_empty_rows *= 999_999

    return dist + nb_empty_columns + nb_empty_rows


def resolve(data: list[str], part2: bool = False) -> int:
    total: int = 0
    empty_rows: list[int] = []
    empty_columns: list[int] = []
    galaxies: list[complex] = []
    pairs: set[tuple[complex, complex]] = set()

    for y, line in enumerate(data):
        if '#' not in line:
            empty_rows.append(y)
        for x, char in enumerate(line):
            if data[y][x] == '#':
                galaxies.append(complex(x, y))

    for x, column in enumerate(zip(*data)):
        if '#' not in column:
            empty_columns.append(x)

    # every pair of galaxies
    for galaxy1 in galaxies:
        for galaxy2 in galaxies:
            if galaxy1 != galaxy2 and (galaxy1, galaxy2) not in pairs and (galaxy2, galaxy1) not in pairs:
                total += expanded_dist(galaxy1, galaxy2, empty_columns, empty_rows, part2)
                pairs.add((galaxy1, galaxy2))

    return total


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        return resolve(data)

    def part2(self, data: list[str]) -> int | str:
        return resolve(data, part2=True)


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

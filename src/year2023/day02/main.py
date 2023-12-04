import os

from utils.exercise import Exercise


def possible(rgb: dict[str, int], config: tuple[int, int, int] = (12, 13, 14)) -> bool:
    red = rgb.get('red')
    green = rgb.get('green')
    blue = rgb.get('blue')
    rgb_tuple = (red, green, blue)
    return all([rgb_tuple[i] <= config[i] for i in range(3)])


def get_power(max_colors: dict[str, int]) -> int:
    red_mult = max_colors.get('red', 1)
    green_mult = max_colors.get('green', 1)
    blue_mult = max_colors.get('blue', 1)
    return red_mult * green_mult * blue_mult


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total = 0
        max_colors: dict[str, int]

        for line in data:
            split = line.split(':')
            game_id = int(split[0].removeprefix('Game '))
            sets = split[1]
            sets = sets.replace(',', '').replace(';', '').split()

            max_colors = {}
            for index in range(0, len(sets), 2):
                num = int(sets[index])
                color = sets[index + 1]
                max_colors[color] = max(max_colors.get(color, 0), num)

            if possible(max_colors):
                total += game_id

        return total

    def part2(self, data: list[str]) -> int | str:
        total = 0
        max_colors: dict[str, int]

        for line in data:
            split = line.split(':')
            sets = split[1]
            sets = sets.replace(',', '').replace(';', '').split()

            max_colors = {}
            for index in range(0, len(sets), 2):
                num = int(sets[index])
                color = sets[index + 1]
                max_colors[color] = max(max_colors.get(color, 0), num)

            power = get_power(max_colors)
            total += power

        return total


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

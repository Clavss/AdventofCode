import os
import re

from utils.exercise import Exercise


def is_correct(possibility: str, groups_length: list[int]) -> bool:
    groups = [group.count('#') for group in re.findall(r'#+', possibility)]
    return groups == groups_length


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        # brute force, won't work for part2
        total = 0

        for line in data:
            split = line.split()
            springs = split[0]
            groups_length = [int(num) for num in split[1].split(',')]

            # test each possibility
            nb_unknown = springs.count('?')
            # every binary number of length nb_unknown
            for binary in range(pow(2, nb_unknown)):
                possibility = springs
                count = 0
                for index, char in enumerate(springs):
                    if char == '?':
                        nth_digit = (binary >> count) % 2
                        count += 1
                        possibility = possibility[:index] + '.#'[nth_digit] + possibility[index + 1:]

                if is_correct(possibility, groups_length):
                    total += 1

        return total

    def part2(self, data: list[str]) -> int | str:
        # Initial thoughts:
        # for each group of '?':
        #   nb_dots = len('?') - count('#')
        #   nb_places = nb_groups('#') + 1
        #   nb_arrangements = len(list(combinations(range(nb_dots + nb_places - 1), nb_places - 1)))
        #   total += nb_arrangements
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

import itertools
import os

from utils.exercise import Exercise


def is_reflection_row(y: int, pattern: list[str], part2: bool) -> bool:
    height: int = len(pattern)
    nb_lines_before: int = y + 1
    nb_lines_after: int = height - nb_lines_before
    min_nb_lines: int = min(nb_lines_before, nb_lines_after)
    swap_done = False

    for row in range(min_nb_lines):
        if pattern[y - row] != pattern[y + 1 + row]:
            if part2 and not swap_done:
                # count number of differences in the rows
                count = 0
                for index in range(len(pattern[0])):
                    if pattern[y - row][index] != pattern[y + 1 + row][index]:
                        count += 1
                # only one character differs
                if count == 1:
                    swap_done = True
                    continue
            return False

    return True


def nb_lines_before_reflexion(pattern: list[str], part2: bool, previous_line: int = -1) -> int:
    last_index: int = len(pattern) - 1

    for index in range(last_index):
        # part 2, skip old reflection line
        if index == previous_line - 1:
            continue
        # find reflection
        if is_reflection_row(index, pattern, part2):
            return index + 1

    return -1


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        nb_rows_above: int = 0
        nb_columns_left: int = 0
        patterns: list[list[str]] = [list(group) for k, group in itertools.groupby(data, lambda x: x == '') if not k]

        for pattern in patterns:
            if (nb_lines := nb_lines_before_reflexion(pattern, False)) > 0:
                nb_rows_above += nb_lines
            else:
                # transpose pattern
                pattern = list(zip(*pattern))
                nb_columns_left += nb_lines_before_reflexion(pattern, False)

        return 100 * nb_rows_above + nb_columns_left

    def part2(self, data: list[str]) -> int | str:
        nb_rows_above: int = 0
        nb_columns_left: int = 0
        patterns: list[list[str]] = [list(group) for k, group in itertools.groupby(data, lambda x: x == '') if not k]

        for pattern in patterns:
            old_lines = [-1, -1]

            # get old reflection line
            old_lines[0] = nb_lines_before_reflexion(pattern, False)
            if old_lines[0] == -1:
                old_lines[1] = nb_lines_before_reflexion(list(zip(*pattern)), False)

            # find new reflection line
            if (new_nb_lines := nb_lines_before_reflexion(pattern, True, old_lines[0])) > 0:
                nb_rows_above += new_nb_lines
            else:
                new_nb_lines = nb_lines_before_reflexion(list(zip(*pattern)), True, old_lines[1])
                nb_columns_left += new_nb_lines

        return 100 * nb_rows_above + nb_columns_left


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

import os
import re

from utils.exercise import Exercise


def str_to_int(string: str) -> int:
    _dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    res = _dict.get(string, None)
    return res if res is not None else int(string)


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        calibration_sum = 0

        for line in data:
            digits = ''.join(re.findall(r'\d+', line))
            calibration_sum += int(digits[0] + digits[-1])

        return calibration_sum

    def part2(self, data: list[str]) -> int | str:
        calibration_sum = 0

        for line in data:
            matches = re.finditer('(?=(1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine))', line)
            digits = [match.group(1) for match in matches]
            calibration_sum += int(str(str_to_int(digits[0])) + str(str_to_int(digits[-1])))

        return calibration_sum


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

import os
import re

from utils.exercise import Exercise


def extrapolate(line: str, reverse: bool = False) -> int:
    nums = [int(num) for num in re.findall(r'-?\d+', line)]
    if reverse:
        nums = nums[::-1]

    total = nums[-1]
    nums = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    while any(nums):
        total += nums[-1]
        nums = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]

    return total


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        # Initial thoughts, not used
        # 68 = 45 + 15 + 6 + 2                                  total = pascal triangle (pt) sum =
        # 45 = 45                                                                           pt(1) +
        # 15 = (45 - 30)                                                                    pt(2) +
        # 6 = 15 - 9 = (45 - 30) - (30 - 21) = 45 - 2*30 + 21                               pt(3) +
        # 2 = 6 - 4 = 15 - 9 - (9 - 5) = (45 - 30) - (30 - 21) - ((30 - 21) - (21 - 16))    pt(4)
        #   = 45 - 30 - 30 + 21 - 30 + 21 + 21 - 16
        #   = 45 - 3*30 + 3*21 - 16
        total = 0

        for line in data:
            total += extrapolate(line)

        return total

    def part2(self, data: list[str]) -> int | str:
        return sum([extrapolate(line, reverse=True) for line in data])


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

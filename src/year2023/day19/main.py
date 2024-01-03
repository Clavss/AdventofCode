import os
import re

from utils.exercise import Exercise


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        count: int = 0
        workflows: dict[str, str] = {}
        sep: int = data.index('')

        for line in data[:sep]:
            split: list[str] = line.split('{')
            name: str = split[0]
            rules: str = split[1][:-1]
            workflows[name] = rules

        for line in data[sep + 1:]:
            numbers: list[int] = [int(num) for num in re.findall(r'\d+', line)]
            workflow: str = 'in'

            while workflow not in 'RA':
                rules: str = workflows[workflow]
                rules: list[str] = rules.split(',')

                for rule in rules:
                    condition: str | None
                    res_workflow: str
                    colon_index: int = rule.find(':')
                    # unconditional
                    if colon_index == -1:
                        workflow = rule
                        break

                    res_workflow = rule[colon_index + 1:]
                    condition = rule[:colon_index]
                    # replace letter by its value in the condition
                    letter: str = condition[0]
                    value: int = numbers['xmas'.index(letter)]
                    condition = str(value) + condition[1:]

                    res_condition: bool = eval(condition)

                    if res_condition:
                        workflow = res_workflow
                        break

            if workflow == 'A':
                count += sum(numbers)

        return count

    def part2(self, data: list[str]) -> int | str:
        pass


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

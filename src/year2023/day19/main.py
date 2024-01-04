import os
import re

from utils.common import replace_tuple_at
from utils.exercise import Exercise


def inverse_rule(rule: str) -> str:
    colon_index: int = rule.find(':')
    condition: str = rule[:colon_index]
    letter: str = condition[0]
    comp_sign: str = condition[1]
    value: int = int(condition[2:])

    new_sign: str = '<>'[comp_sign == '<']
    new_value: int = [1, -1][comp_sign == '<'] + value
    return letter + new_sign + str(new_value) + rule[colon_index:]


def inverse_previous_rules(rules: list[str], rule_index: int) -> list[str]:
    return [inverse_rule(rule) for rule in rules[:rule_index]] + [rules[rule_index]]


def update_intervals(intervals: tuple[int, ...], rules: list[str]) -> tuple[int, ...]:
    for rule in rules:
        colon_index: int = rule.find(':')
        if colon_index == -1:
            break

        condition = rule[:colon_index]
        letter: str = condition[0]
        comp_sign: str = condition[1]
        value: int = int(condition[2:])

        letter_index: int = 'xmas'.index(letter)
        condition_index_min: int = letter_index * 2
        condition_index_max: int = condition_index_min + 1

        if comp_sign == '<':
            _min = min(value - 1, intervals[condition_index_max])
            intervals = replace_tuple_at(intervals, condition_index_max, _min)
        else:  # comp_sign == '>'
            _max = max(value + 1, intervals[condition_index_min])
            intervals = replace_tuple_at(intervals, condition_index_min, _max)

    return intervals


def find_accepted_intervals(intervals: tuple[int, ...], state: str, workflows: dict[str, str]) -> list[list[int]]:
    if state == 'A':
        return [list(intervals)]
    if state == 'R':
        return []

    rules: list[str] = workflows[state].split(',')
    res: list[list[int]] = []

    for rule_index, rule in enumerate(rules):
        condition: str
        colon_index: int = rule.find(':')
        res_workflow: str = rule[colon_index + 1:]

        new_rules: list[str] = inverse_previous_rules(rules, rule_index)
        new_intervals: tuple[int, ...] = update_intervals(intervals, new_rules)
        res += find_accepted_intervals(new_intervals, res_workflow, workflows)

    return res


def combinations(interval: list[int]) -> int:
    res = 1
    for i in range(4):
        start = interval[i * 2]
        end = interval[i * 2 + 1]
        length = end - start + 1
        res *= length
    return res


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
                    # unconditional rule
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
        workflows: dict[str, str] = {}
        sep: int = data.index('')

        for line in data[:sep]:
            split: list[str] = line.split('{')
            name: str = split[0]
            rules: str = split[1][:-1]
            workflows[name] = rules

        start: str = 'in'
        accepted_intervals: list[list[int]] = find_accepted_intervals((1, 4000, 1, 4000, 1, 4000, 1, 4000), start,
                                                                      workflows)

        count: int = sum([combinations(accepted_interval) for accepted_interval in accepted_intervals])
        return count


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

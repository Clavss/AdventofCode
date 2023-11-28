import functools
import math
import os
from dataclasses import dataclass, field
from typing import Callable

from utils.exercise import Exercise


@dataclass
class Item:
    worry_level: int


@dataclass
class Monkey:
    id: int
    items: list[Item] = field(default_factory=list, init=False)
    operation: Callable[[int], int] = field(init=False)
    test_divisible_by: int = field(init=False)
    monkeys_to_throw_to: tuple[int, int] = field(default=None, init=False)
    inspection_counter: int = field(default=0, init=False)

    def set_operation(self, operator: str, operand: str) -> None:
        match operator:
            case '+':
                self.operation = (lambda old: old + int(operand)) if operand != 'old' else (lambda old: old + old)
            case '*':
                self.operation = (lambda old: old * int(operand)) if operand != 'old' else (lambda old: old * old)
            case '-':
                self.operation = (lambda old: old - int(operand)) if operand != 'old' else (lambda old: old - old)
            case '/':
                self.operation = (lambda old: old / int(operand)) if operand != 'old' else (lambda old: old / old)

    def take_turn(self, monkey_total_diviser: int) -> list[int]:
        """Return a list of monkey numbers to which items will be sent."""
        throw_to: list[int] = []
        # inspect items
        for item in self.items:
            # increment counter
            self.inspection_counter += 1
            # compute new worry level
            wl = self.operation(item.worry_level)
            if monkey_total_diviser == 0:
                wl //= 3
            else:
                wl %= monkey_total_diviser
            # update item worry level
            item.worry_level = wl
            throw_to.append(self.monkeys_to_throw_to[(wl % self.test_divisible_by) == 0])
        return throw_to


def parse_monkeys(data: list[str]) -> list[Monkey]:
    monkeys = []
    nb_monkeys = math.ceil(len(data) / 7)

    for no_monkey in range(nb_monkeys):
        start_index = 7 * no_monkey
        # parse monkey id from 'Monkey 0:'
        line: str = data[start_index]
        line = line.removeprefix('Monkey ')
        monkey_id = int(line.split(':')[0])

        # parse monkey starting items from ex: '  Starting items: 79, 98'
        line: str = data[start_index + 1]
        split = line.strip().replace(' ', '').split(':')[-1].split(',')
        monkey_items = [Item(int(wl)) for wl in split]

        # parse monkey operation from ex: '  Operation: new = old * 19'
        line: str = data[start_index + 2]
        *_, monkey_operator, monkey_operand = line.split()

        # parse monkey test from ex: '  Test: divisible by 23'
        line: str = data[start_index + 3]
        monkey_test_divisible_by = int(line.split()[-1])

        # parse monkey is true from ex: '    If true: throw to monkey 2'
        line: str = data[start_index + 4]
        monkey_if_true = int(line.split()[-1])

        # parse monkey is false from ex: '    If false: throw to monkey 3'
        line: str = data[start_index + 5]
        monkey_if_false = int(line.split()[-1])

        monkey = Monkey(monkey_id)
        monkey.items = monkey_items
        monkey.set_operation(monkey_operator, monkey_operand)
        monkey.test_divisible_by = monkey_test_divisible_by
        monkey.monkeys_to_throw_to = (monkey_if_false, monkey_if_true)

        monkeys.append(monkey)

    return monkeys


def resolve(data: list[str], nb_rounds: int, bored: bool) -> int:
    monkeys = parse_monkeys(data)
    if bored:
        monkey_total_diviser = 0
    else:
        monkey_total_diviser = functools.reduce(lambda a, b: a * b, [monkey.test_divisible_by for monkey in monkeys], 1)

    for monkey_round in range(nb_rounds):
        for monkey in monkeys:
            throw_to = monkey.take_turn(monkey_total_diviser)
            # add each item to corresponding monkeys
            for index, item in enumerate(monkey.items):
                monkeys[throw_to[index]].items.append(item)
            # remove these items from original monkey
            monkey.items = []

        # print(f'after round {monkey_round + 1}')
        # [print(f'Monkey {monkey.id}: {monkey.items}') for monkey in monkeys]

    first, second = sorted([monkey.inspection_counter for monkey in monkeys], reverse=True)[:2]
    monkey_business = first * second
    return monkey_business


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        return resolve(data, 20, True)

    def part2(self, data: list[str]) -> int | str:
        return resolve(data, 10_000, False)


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

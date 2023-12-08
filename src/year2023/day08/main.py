import math
import os

from utils.exercise import Exercise


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        steps = 0
        str_nodes: list[str]
        nodes: dict[str, tuple[str, str]] = {}

        instructions, _, *str_nodes = data
        for node in str_nodes:
            start, left, right = (node.replace(' ', '')
                                  .replace('(', '')
                                  .replace(')', '')
                                  .replace('=', ',')
                                  .split(','))
            nodes[start] = (left, right)

        current_node = 'AAA'

        while current_node != 'ZZZ':
            instruction = instructions[steps % len(instructions)]
            current_node = nodes.get(current_node)[instruction == 'R']
            steps += 1

        return steps

    def part2(self, data: list[str]) -> int | str:
        cycles: list[int] = []
        str_nodes: list[str]
        nodes: dict[str, tuple[str, str]] = {}
        start_nodes: list[str] = []
        end_nodes: list[str] = []

        instructions, _, *str_nodes = data
        for node in str_nodes:
            start, left, right = (node.replace(' ', '')
                                  .replace('(', '')
                                  .replace(')', '')
                                  .replace('=', ',')
                                  .split(','))
            nodes[start] = (left, right)
            if start.endswith('A'):
                start_nodes.append(start)
            if start.endswith('Z'):
                end_nodes.append(start)

        index = 0
        while len(end_nodes) > 0:
            steps = 0
            current_node = start_nodes[index]

            # search an ending node
            while not current_node.endswith('Z'):
                instruction = instructions[steps % len(instructions)]
                current_node = nodes.get(current_node)[instruction == 'R']
                steps += 1

            # remove the found ending node
            end_nodes.remove(current_node)
            cycles.append(steps)
            index += 1

        # solution is the least common multiple of all cycles
        steps = math.lcm(*cycles)

        return steps


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

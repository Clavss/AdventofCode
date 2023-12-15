import os
from collections import OrderedDict

from utils.exercise import Exercise


def holiday_hash(string: str) -> int:
    total: int = 0
    for char in string:
        total += ord(char)
        total *= 17
        total %= 256

    return total


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total: int = 0
        line: str = data[0]
        steps: list[str] = line.split(',')

        for step in steps:
            step_value = holiday_hash(step)
            total += step_value

        return total

    def part2(self, data: list[str]) -> int | str:
        total: int = 0
        line: str = data[0]
        steps: list[str] = line.split(',')
        boxes: dict[int, OrderedDict[str, int]] = {}
        label: str
        operation: str
        focal_length: int = -1

        for step in steps:
            # parse step
            if step[-1].isdigit():
                operation = '='
                split = step.split(operation)
                label = split[0]
                focal_length = int(split[1])
            else:
                operation = '-'
                split = step.split(operation)
                label = split[0]

            box_number: int = holiday_hash(label)
            box: OrderedDict[str, int] = boxes.get(box_number, OrderedDict())

            if operation == '=':
                # update OrderedDict if the element exists, otherwise append it at the end
                box[label] = focal_length
                boxes[box_number] = box
            else:  # operation == '-'
                # remove the element if it exists in the box
                if box.get(label, None) is not None:
                    del box[label]

        for box_number, box in boxes.items():
            for index, (label, focal_length) in enumerate(box.items()):
                total += (box_number + 1) * (int(index) + 1) * focal_length
        return total


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

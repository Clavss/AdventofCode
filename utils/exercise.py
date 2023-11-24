import os
from abc import ABC, abstractmethod

from utils.exceptions import TestFailException


def assert_equal(actual, expected) -> None:
    try:
        assert actual == expected
    except AssertionError:
        raise TestFailException(f'actual: \t{actual} !=\nexpected:\t{expected}')


class Exercise(ABC):
    def __init__(self, dir_name: str) -> None:
        self.name = dir_name

    def parse(self) -> list[str]:
        with open(os.path.join(self.name, 'input.txt'), 'r') as file:
            data = [line.strip() for line in file]
        return data

    def parse_example(self) -> list[str]:
        with open(os.path.join(self.name, 'test', 'example.txt'), 'r') as f:
            data = [line.strip() for line in f]
        return data

    def parse_result(self, part: int) -> str:
        with open(os.path.join(self.name, 'test', f'result_part{part}.txt'), 'r') as f:
            expected_result = f.readline()
        return expected_result

    @abstractmethod
    def part1(self, data: list[str]) -> int | str:
        """Abstract method to be implemented by each exercise."""
        pass

    @abstractmethod
    def part2(self, data: list[str]) -> int | str:
        """Abstract method to be implemented by each exercise."""
        pass

    def test_part(self, part: int, data: list[str]) -> None:
        partx = self.__getattribute__(f'part{part}')
        actual = str(partx(data))
        expected = self.parse_result(part)
        assert_equal(actual, expected)

    def exec_part(self, part: int, test=True) -> None:
        try:
            if test:
                data = self.parse_example()
                self.test_part(part, data)
        except TestFailException as e:
            e.print_message(part)
        else:
            if test:
                print(f'test part{part} passed')

            data = self.parse()
            partx = self.__getattribute__(f'part{part}')
            print(f'part{part}:', partx(data))

    def exec_all(self, test=True):
        self.exec_part(1, test)
        self.exec_part(2, test)

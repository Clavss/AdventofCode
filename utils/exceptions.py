import sys


class TestFailException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def print_message(self, part: int) -> None:
        print(f'test part{part} failed', file=sys.stderr)
        print(self.message, file=sys.stderr)

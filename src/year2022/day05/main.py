import os


class Cargo:
    def __init__(self) -> None:
        self.stacks = ['BZT',
                       'VHTDN',
                       'BFMD',
                       'TJGWVQL',
                       'WDGPVFQM',
                       'VZQGHFS',
                       'ZSNRLTCW',
                       'ZHWDJNRM',
                       'MQLFDS']

    def move_1_by_1(self, quantity: int, from_stack: int, to_stack: int) -> None:
        for _ in range(quantity):
            self.stacks[from_stack], moving = self.stacks[from_stack][:-1], self.stacks[from_stack][-1]
            self.stacks[to_stack] += moving

    def move_all_in_1(self, quantity: int, from_stack: int, to_stack: int) -> None:
        self.stacks[from_stack], moving = self.stacks[from_stack][:-quantity], self.stacks[from_stack][-quantity:]
        self.stacks[to_stack] += moving


def problem1(data: list[str]) -> str:
    cargo = Cargo()

    for instruction in data:
        _, quantity, _, _from, _, _to = instruction.split()
        cargo.move_1_by_1(int(quantity), int(_from) - 1, int(_to) - 1)

    return ''.join([stack[-1] for stack in cargo.stacks])


def problem2(data: list[str]) -> str:
    cargo = Cargo()

    for instruction in data:
        _, quantity, _, _from, _, _to = instruction.split()
        cargo.move_all_in_1(int(quantity), int(_from) - 1, int(_to) - 1)

    return ''.join([stack[-1] for stack in cargo.stacks])


def main() -> None:
    directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(directory, "input.txt")) as file:
        data = [line.strip() for line in file]

    print(problem1(data))  # NTWZZWHFV
    print(problem2(data))  # BRZGFVBTJ


if __name__ == "__main__":
    main()

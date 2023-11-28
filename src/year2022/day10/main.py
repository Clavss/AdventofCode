import os

from utils.exercise import Exercise


class Problem(Exercise):
    cycle: int = None
    x: int = None
    x_at_cycle: list[tuple[int, int]] = None

    def part1(self, data: list[str]) -> int | str:
        self.cycle = 0
        self.x = 1
        self.x_at_cycle = []
        res = 0

        for line in data:
            self.handle_instruction(line)

        cycles_asked = [20 + 40 * i for i in range(6)]
        for cycle in cycles_asked:
            res += cycle * self.get_x_at_cycle(cycle)

        return res

    def dichotomy_search(self, search: int, start: int, end: int) -> int:
        if self.x_at_cycle[start][0] == search:
            return self.x_at_cycle[start - 1][1]

        if start == end:
            return self.x_at_cycle[start][1]

        mid = start + (end - start) // 2
        if self.x_at_cycle[start][0] <= search <= self.x_at_cycle[mid][0]:
            return self.dichotomy_search(search, start, mid)
        elif self.x_at_cycle[mid + 1][0] <= search <= self.x_at_cycle[end][0]:
            return self.dichotomy_search(search, mid + 1, end)
        else:
            return self.x_at_cycle[mid][1]

    def get_x_at_cycle(self, cycle: int) -> int:
        x = self.dichotomy_search(cycle, 0, len(self.x_at_cycle) - 1)
        return x

    def handle_instruction(self, line: str) -> None:
        if line.startswith('addx'):
            self.cycle += 2
            quantity = line.split()[1]
            self.x += int(quantity)
            self.save()
        else:
            self.cycle += 1

    def save(self) -> None:
        self.x_at_cycle.append((self.cycle, self.x))

    def part2(self, data: list[str]) -> int | str:
        number_of_instruction_cycle = {'addx': 2, 'noop': 1}
        self.x = 1
        self.cycle = 0
        quantity = 0
        crt = ''

        for line in data:
            # instruction is addx
            if line.startswith('addx'):
                _split = line.split()
                current_instruction = _split[0]
                quantity = int(_split[1])
            # instruction is noop
            else:
                current_instruction = line

            instruction_cycles_left = number_of_instruction_cycle.get(current_instruction)

            for _ in range(instruction_cycles_left):
                # print(f'processing {self.current_instruction} {quantity}({_ + 1}/{self.instruction_cycles_left})')
                if self.is_sprite_visible():
                    crt += '#'
                else:
                    crt += '.'
                self.cycle += 1

            if current_instruction == 'addx':
                self.x += quantity

        # Show the answer in a readable format
        length = len(crt) // 6
        [print(crt[i * length:(i + 1) * length - 1]) for i in range(6)]

        return crt

    def is_sprite_visible(self):
        return self.x - 1 <= self.cycle % 40 <= self.x + 1


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

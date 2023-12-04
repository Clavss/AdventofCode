import os

from utils.exercise import Exercise


def points(count: int) -> int:
    # count:    0 1 2 3 4  5  6
    # return:   0 1 2 4 8 16 32
    if count <= 2:
        return count
    return 2 ** (count - 1)


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total = 0

        for line in data:
            split = line.split(':')[1].strip().split(' | ')
            winning_numbers, my_numbers = split[0].split(), split[1].split()

            count_matching_cards = len(set(winning_numbers) & set(my_numbers))
            total += points(count_matching_cards)

        return total

    def part2(self, data: list[str]) -> int | str:
        cards_count: dict[int, int] = {}

        for line in data:
            current_card = int(line.split(':')[0].removeprefix('Card '))
            split = line.split(':')[1].strip().split(' | ')
            winning_numbers, my_numbers = split[0].split(), split[1].split()

            count_matching_cards = len(set(winning_numbers) & set(my_numbers))
            for card_number in range(current_card + 1, current_card + count_matching_cards + 1):
                cards_count[card_number] = cards_count.get(card_number, 1) + cards_count.get(current_card, 1)

        total = 0
        for i in range(len(data)):
            total += cards_count.get(i + 1, 1)

        return total


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

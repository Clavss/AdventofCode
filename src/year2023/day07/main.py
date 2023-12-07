import os

from utils.exercise import Exercise


def card_value_with_jack(card: str):
    cards = [*[str(n) for n in range(2, 10)], 'T', 'J', 'Q', 'K', 'A']
    return cards.index(card)


def card_value_with_joker(card: str):
    cards = ['J', *[str(n) for n in range(2, 10)], 'T', 'Q', 'K', 'A']
    return cards.index(str(card))


def best_card_for_joker(hand: str) -> str:
    hand_without_j = hand.replace('J', '')
    if hand_without_j == '':
        return 'A'
    cards_count = [(hand_without_j.count(card), card) for card in set(hand)]
    max_card_count = sorted(cards_count, reverse=True)[0][0]
    best_cards = [card for count, card in cards_count if count == max_card_count]
    return sorted(best_cards, key=card_value_with_joker)[-1]


def hand_type(hand: str, joker=False) -> int:
    five_of_a_kind = 6
    four_of_a_kind = 5
    full_house = 4
    three_of_a_kind = 3
    two_pair = 2
    one_pair = 1
    high_card = 0

    if joker and 'J' in hand:
        _best_card = best_card_for_joker(hand)
        hand = hand.replace('J', _best_card)

    cards_count = {card: hand.count(card) for card in set(hand)}
    different_cards = len(cards_count)
    max_card_count = max(cards_count.values())

    match different_cards:
        case 1: return five_of_a_kind
        case 2: return four_of_a_kind if max_card_count == 4 else full_house
        case 3: return three_of_a_kind if max_card_count == 3 else two_pair
        case 4: return one_pair
        case _: return high_card


def value_card_based(hand: str, joker=False) -> int:
    res = 0

    for index, card in enumerate(hand[::-1]):
        if joker:
            card_value = card_value_with_joker(card)
        else:
            card_value = card_value_with_jack(card)
        res += pow(13, index) * card_value

    return res


def hand_order(hand: str, joker=False) -> tuple[int, int]:
    _type = hand_type(hand, joker)
    value = value_card_based(hand, joker)

    return _type, value


def resolve(data: list[str], joker=False) -> int | str:
    total_winnings = 0
    # [(hand, bid)]
    hands: list[tuple[str, int]] = []
    for line in data:
        split = line.split()
        hands.append((split[0], int(split[1])))

    hands.sort(key=lambda x: hand_order(x[0], joker))

    for index, (hand, bid) in enumerate(hands):
        # int cast on index is only here to remove wrong PyCharm linter warning
        total_winnings += (int(index) + 1) * bid
    return total_winnings


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        total_winnings = resolve(data, False)
        return total_winnings

    def part2(self, data: list[str]) -> int | str:
        total_winnings = resolve(data, True)
        return total_winnings


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    # test_hand_type()
    # test_value_card_based()
    problem.exec_all(True)


def test_hand_type() -> None:
    assert hand_type('AAAAA') == 6
    assert hand_type('AA8AA') == 5
    assert hand_type('23332') == 4
    assert hand_type('TTT98') == 3
    assert hand_type('23432') == 2
    assert hand_type('A23A4') == 1
    assert hand_type('23456') == 0


def test_value_card_based() -> None:
    expected = 0
    possibilities = [*range(2, 10), 'T', 'J', 'Q', 'K', 'A']
    for card1 in possibilities:
        for card2 in possibilities:
            for card3 in possibilities:
                for card4 in possibilities:
                    for card5 in possibilities:
                        hand = str(card1) + str(card2) + str(card3) + str(card4) + str(card5)
                        actual = value_card_based(hand)
                        assert actual == expected
                        expected += 1


if __name__ == "__main__":
    main()

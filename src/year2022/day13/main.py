import functools
import math
import os

from utils.exercise import Exercise


def compare(l1: list, l2: list) -> int:
    """Compare two lists.

    Return 1 if l1 and l2 are ordered, -1 if not, 0 if equal.
    """
    ordered = 1
    not_ordered = -1
    equal = 0

    if l1 == l2:
        return equal

    length_l1 = len(l1)
    length_l2 = len(l2)
    # l1 is empty
    if length_l1 == 0:
        return ordered
    # l2 is empty
    elif length_l2 == 0:
        return not_ordered

    # compare each element 1 by 1
    for index in range(length_l1):
        # l1 contains l2 plus additional elements
        if index >= length_l2:
            return not_ordered

        elm_packet1 = l1[index]
        elm_packet2 = l2[index]

        # compare 2 integers
        if type(elm_packet1) is type(elm_packet2) is int:
            compare_result = elm_packet2 - elm_packet1

        # compare 2 lists
        elif type(elm_packet1) is type(elm_packet2) is list:
            compare_result = compare(elm_packet1, elm_packet2)

        # compare a list with an integer
        # convert integer to list and continue comparing the elements as lists
        elif type(elm_packet1) is int:
            elm_packet1 = [elm_packet1]
            compare_result = compare(elm_packet1, elm_packet2)
        else:  # type(elm_packet2) is int
            elm_packet2 = [elm_packet2]
            compare_result = compare(elm_packet1, elm_packet2)

        if compare_result > 0:
            return ordered
        elif compare_result < 0:
            return not_ordered
        # no decision can be made if elements are equal, continue comparing next elements
        else:  # compare_result == 0
            continue

    # l2 contains l1 plus additional elements
    return ordered


class Problem(Exercise):

    def part1(self, data: list[str]) -> int | str:
        nb_pairs = math.ceil(len(data) / 3)
        ordered_pairs_index = []

        for index_pair in range(nb_pairs):
            start_index = 3 * index_pair
            packet1 = eval(data[start_index])
            packet2 = eval(data[start_index + 1])

            ordered = compare(packet1, packet2)
            if ordered == 1:
                ordered_pairs_index.append(index_pair + 1)

        res = sum(ordered_pairs_index)
        return res

    def part2(self, data: list[str]) -> int | str:
        divider_packet1 = [[2]]
        divider_packet2 = [[6]]

        packets = [eval(line) for line in data if line != '']
        packets += [divider_packet1] + [divider_packet2]
        packets.sort(key=functools.cmp_to_key(compare), reverse=True)

        divider_packet1_index = packets.index(divider_packet1) + 1
        divider_packet2_index = packets.index(divider_packet2) + 1
        decoder_key = divider_packet1_index * divider_packet2_index
        return decoder_key


def main() -> None:
    directory = os.path.dirname(__file__)
    problem = Problem(directory)

    problem.exec_all(True)


if __name__ == "__main__":
    main()

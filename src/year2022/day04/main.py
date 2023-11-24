from __future__ import annotations

import os


class SectionRange:
    def __init__(self, section_range: str) -> None:
        split_section_range = section_range.split('-')
        self.section_start = int(split_section_range[0])
        self.section_end = int(split_section_range[1])

    def is_fully_contained_in(self, other_range: SectionRange) -> bool:
        return other_range.section_start <= self.section_start <= self.section_end <= other_range.section_end

    def overlap_with(self, other_range: SectionRange) -> bool:
        return ((other_range.section_start <= self.section_start <= other_range.section_end) or
                (other_range.section_start <= self.section_end <= other_range.section_end))


def problem1(data: list[str]) -> int:
    count = 0

    for pair in data:
        # Assuming every line is well-formed
        split_pair = pair.split(',')
        section_range_str1, section_range_str2 = split_pair[0], split_pair[1]

        section_range1 = SectionRange(section_range_str1)
        section_range2 = SectionRange(section_range_str2)

        if section_range1.is_fully_contained_in(section_range2) or section_range2.is_fully_contained_in(section_range1):
            count += 1

    return count


def problem2(data: list[str]) -> int:
    count = 0

    for pair in data:
        # Assuming every line is well-formed
        split_pair = pair.split(',')
        section_range_str1, section_range_str2 = split_pair[0], split_pair[1]

        section_range1 = SectionRange(section_range_str1)
        section_range2 = SectionRange(section_range_str2)

        if section_range1.overlap_with(section_range2) or section_range1.is_fully_contained_in(
                section_range2) or section_range2.is_fully_contained_in(section_range1):
            count += 1

    return count


def main() -> None:
    directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(directory, "input.txt")) as file:
        data = [line.strip() for line in file]

    print(problem1(data))  # 305
    print(problem2(data))  # 811


if __name__ == "__main__":
    main()

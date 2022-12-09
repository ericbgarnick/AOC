"""
Part 1 answer: 453
Part 2 answer: 919
"""
from typing import Tuple

from y2022.python.shared import get_data_file_path

ALPHABET_START = ord("a")
ALPHABET_LENGTH = 26
GROUP_SIZE = 3


def main():
    num_subsets = 0
    num_overlaps = 0
    with open(get_data_file_path(__file__), "r") as f_in:
        for line in f_in:
            range1, range2 = line.strip().split(",")
            range1 = parse_range(range1)
            range2 = parse_range(range2)
            if is_a_subset(range1, range2) or is_a_subset(range2, range1):
                num_subsets += 1
            if overlaps(range1, range2) or overlaps(range2, range1):
                num_overlaps += 1
    print("PART 1:", num_subsets)
    print("PART 2:", num_overlaps)


def parse_range(raw_range: str) -> Tuple[int, int]:
    val1, val2 = raw_range.split("-")
    return int(val1), int(val2)


def is_a_subset(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    return range2[0] <= range1[0] and range1[1] <= range2[1]


def overlaps(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    if range2[0] <= range1[1] <= range2[1]:
        return True
    if range2[0] <= range1[0] <= range2[1]:
        return True
    return False


if __name__ == "__main__":
    main()

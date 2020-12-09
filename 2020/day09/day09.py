from sys import argv
from typing import Tuple, List

PREAMBLE = 25


def parse_input(filename: str) -> List[int]:
    return [int(line.strip()) for line in open(filename, "r")]


def find_not_sum(record: List[int]) -> int:
    """Return the first number in record that is not the sum of
    2 values in the preceding subsequence of length PREAMBLE"""
    for i in range(PREAMBLE, len(record)):
        num = record[i]
        if not can_sum_to_num(record, num, i):
            return num


def can_sum_to_num(record: List[int], target: int, segment_end: int) -> bool:
    """Return True if any 2 values in record from segment_end - PREAMBLE through segment_end
    can sum to target.  Otherwise return False."""
    complements = set()
    for num in record[segment_end - PREAMBLE:segment_end]:
        if num in complements:
            return True
        else:
            complements.add(target - num)
    return False


def find_weakness(record: List[int], target: int) -> int:
    """Return the sum of the smallest and largest values in the range
    that sums to target. Range is a subsequence in record."""
    range_start, range_end = find_range(record, target)
    weak_range = record[range_start:range_end + 1]
    return min(weak_range) + max(weak_range)


def find_range(record: List[int], target: int) -> Tuple[int, int]:
    """Return the start and end indexes of the subsequence of record that sums to target."""
    i = len(record) - 2
    j = i + 1
    total = sum(record[i:j + 1])
    while i > -1 and j > 0 and total != target:
        if total < target:
            i -= 1
        elif i == j - 1:
            i -= 1
            j -= 1
        else:  # total > target and i != j
            j -= 1
        total = sum(record[i:j + 1])
    return i, j


if __name__ == "__main__":
    input_file = argv[1]
    encrypted = parse_input(input_file)
    not_sum = find_not_sum(encrypted)
    print("PART 1:", not_sum)
    print("PART 2:", find_weakness(encrypted, not_sum))

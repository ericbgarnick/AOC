import sys
from typing import List


def day05_part1(puzzle_data: List[int]) -> int:
    pass


def day05_part2(puzzle_data: List[int]) -> int:
    pass


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(val) for val in open(data_file).read().strip().split(',')]
    print(f"PART 1: {day05_part1(data)}")
    print(f"PART 2: {day05_part2(data)}")

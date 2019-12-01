import sys
from typing import List


TOTAL = 0


def day02_part1(puzzle_data: List[str]):
    for line in puzzle_data:
        process_line(line)


def day02_part2(puzzle_data: List[str]):
    for line in puzzle_data:
        process_line(line)


def process_line(line: str):
    pass


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [l.strip() for l in open(data_file).readlines()]
    print(f"PART 1: {day02_part1(data)}")
    print(f"PART 2: {day02_part2(data)}")

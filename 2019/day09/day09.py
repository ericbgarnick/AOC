import sys
from typing import List

from intcode_computer_09 import IntcodeComputerV4


def day09(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV4(puzzle_data)
    return computer.run()[0]


def day09_part1(puzzle_data):
    pass


def day09_part2(puzzle_data):
    pass


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    day09(data)
    # print(f"PART 2:\n{day09_part2(data)}")

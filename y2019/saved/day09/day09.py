import sys
from typing import List

from intcode_computer_09 import IntcodeComputerV4


def day09(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV4(puzzle_data)
    return computer.run()[0]


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    print("* ENTER 1 FOR PART ONE *\n* ENTER 2 FOR PART TWO *")
    day09(data)

import sys
from typing import List

from intcode_computer_05 import IntcodeComputerV2


def day05(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV2(puzzle_data)
    return computer.run()[0]


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(val) for val in open(data_file).read().strip().split(',')]
    print("* ENTER 1 FOR PART ONE *\n* ENTER 5 FOR PART TWO *")
    day05(data)

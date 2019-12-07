import sys
from itertools import permutations
from typing import List

from intcode_computer_07 import IntcodeComputerV3

NUM_PHASES = 5


def day07_part1(puzzle_data: List[int]):
    best_result = float('-inf')
    for phase_setting_sequence in permutations(range(NUM_PHASES)):
        input_signal = 0
        for i in range(NUM_PHASES):
            phase_setting = phase_setting_sequence[i]
            computer = IntcodeComputerV3(puzzle_data, [phase_setting, input_signal])
            input_signal = computer.run()
        best_result = max(best_result, input_signal)
    return best_result


def day07_part2(puzzle_data: List[int]):
    pass


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    print(f"PART 1: {day07_part1(data)}")
    print(f"PART 2: {day07_part2(data)}")

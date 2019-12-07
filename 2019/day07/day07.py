import sys
from itertools import permutations
from typing import List, Tuple

from intcode_computer_07 import IntcodeComputerV3

NUM_PHASES = 5


def day07_part1(puzzle_data: List[int]) -> int:
    return run_computers(puzzle_data,
                         loop_until_done=False,
                         phase_setting_min=0,
                         phase_setting_max=NUM_PHASES)


def day07_part2(puzzle_data: List[int]) -> int:
    return run_computers(puzzle_data,
                         loop_until_done=True,
                         phase_setting_min=NUM_PHASES,
                         phase_setting_max=NUM_PHASES * 2)


def run_computers(program_data: List[int], loop_until_done: bool,
                  phase_setting_min: int, phase_setting_max: int) -> int:
    best_result = float('-inf')
    for phase_setting_sequence in permutations(range(phase_setting_min,
                                                     phase_setting_max)):
        computers = set_up_computers(program_data, phase_setting_sequence)
        cur_computer = computers[0]
        cur_computer.add_input(0)
        if loop_until_done:
            loop_repeat(computers, cur_computer)
        else:
            loop_once(computers)
        best_result = max(best_result, computers[-1].last_sent_signal)
    return best_result


def set_up_computers(input_sequence: List[int],
                     phase_setting_sequence: Tuple[int]) -> List[IntcodeComputerV3]:
    computers = [IntcodeComputerV3(input_sequence) for _ in range(NUM_PHASES)]
    for i in range(NUM_PHASES):
        next_idx = (i + 1) % NUM_PHASES
        computers[i].add_input(phase_setting_sequence[i])
        computers[i].set_receiver(computers[next_idx])
    return computers


def loop_once(computers: List[IntcodeComputerV3]):
    for i in range(NUM_PHASES):
        computer = computers[i]
        computer.run()


def loop_repeat(computers: List[IntcodeComputerV3],
                cur_computer: IntcodeComputerV3):
    while any(not c.done for c in computers):
        cur_computer.run()
        cur_computer = cur_computer.receiver


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    print(f"PART 1: {day07_part1(data)}")
    print(f"PART 2: {day07_part2(data)}")

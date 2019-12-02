import sys
from typing import List


HALT = 99
GOAL = 19690720


def day02_part1(puzzle_data: List[int]) -> int:
    copied = [v for v in puzzle_data]
    restore_alarm_state(copied, 12, 2)
    return run(copied)[0]


def day02_part2(puzzle_data: List[int]) -> int:
    copied = [v for v in puzzle_data]
    for noun in range(100):
        for verb in range(100):
            restore_alarm_state(copied, noun, verb)
            if run(copied)[0] == GOAL:
                return 100 * noun + verb


def run(original: List[int]) -> List[int]:
    program = [v for v in original]
    next_code_idx = 0
    while program[next_code_idx] != HALT:
        op_code = program[next_code_idx]
        input1, input2 = program[next_code_idx + 1: next_code_idx + 3]
        output = program[next_code_idx + 3]

        if op_code == 1:
            program[output] = program[input1] + program[input2]
        elif op_code == 2:
            program[output] = program[input1] * program[input2]
        else:
            raise ValueError(f"Unknown op code {op_code}")

        next_code_idx += 4

    return program


def restore_alarm_state(program_data: List[int], noun: int, verb: int):
    program_data[1] = noun
    program_data[2] = verb


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file).read().strip().split(',')]
    print(f"PART 1: {day02_part1(data)}")
    print(f"PART 2: {day02_part2(data)}")

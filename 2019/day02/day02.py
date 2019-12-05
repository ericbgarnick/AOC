import sys
from typing import List


HALT = 99
GOAL = 19690720


def day02_part1(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV1(puzzle_data)
    computer.restore_alarm_state(12, 2)
    return computer.run()[0]


def day02_part2(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV1(puzzle_data)
    for noun in range(100):
        for verb in range(100):
            computer.restore_alarm_state(noun, verb)
            if computer.run()[0] == GOAL:
                return 100 * noun + verb


class IntcodeComputerV1:
    def __init__(self, original_program: List[int]):
        self._original_program = [v for v in original_program]

    def run(self) -> List[int]:
        program = [v for v in self._original_program]
        next_code_idx = 0
        while program[next_code_idx] != HALT:
            self._execute_op_code(program, next_code_idx)
            next_code_idx += 4

        return program

    @staticmethod
    def _execute_op_code(program: List[int], next_code_idx: int):
        op_code = program[next_code_idx]
        input1, input2 = program[next_code_idx + 1: next_code_idx + 3]
        output = program[next_code_idx + 3]

        if op_code == 1:
            program[output] = program[input1] + program[input2]
        elif op_code == 2:
            program[output] = program[input1] * program[input2]
        else:
            raise ValueError(f"Unknown op code {op_code}")

    def restore_alarm_state(self, noun: int, verb: int):
        self._original_program[1] = noun
        self._original_program[2] = verb


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file).read().strip().split(',')]
    print(f"PART 1: {day02_part1(data)}")
    print(f"PART 2: {day02_part2(data)}")

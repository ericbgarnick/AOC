import sys
from typing import List, Tuple

from intcode_computer import IntcodeComputerV1

Instruction = Tuple[int, int, int, int]


class IntcodeComputerV2(IntcodeComputerV1):
    PARAMETERIZED_PROCESSES = [3, 4]
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    @staticmethod
    def _execute_op_code(program: List[int], next_code_idx: List[int]):
        idx_val = next_code_idx[0]
        instruction_code = program[idx_val]
        op_code, mode1, mode2, mode3 = IntcodeComputerV2._interpret_instruction(instruction_code)

        if op_code not in IntcodeComputerV2.PARAMETERIZED_PROCESSES:
            input1 = IntcodeComputerV2._input_for_mode(mode1, 1, idx_val, program)
            input2 = IntcodeComputerV2._input_for_mode(mode2, 2, idx_val, program)
            output = program[idx_val + 3]

            if op_code == 1:
                program[output] = input1 + input2
                next_code_idx[0] += 4
            elif op_code == 2:
                program[output] = input1 * input2
                next_code_idx[0] += 4
            elif op_code == 5:
                if input1:
                    next_code_idx[0] = input2
                else:
                    next_code_idx[0] += 3
            elif op_code == 6:
                if not input1:
                    next_code_idx[0] = input2
                else:
                    next_code_idx[0] += 3
            elif op_code == 7:
                if input1 < input2:
                    program[output] = 1
                else:
                    program[output] = 0
                next_code_idx[0] += 4
            elif op_code == 8:
                if input1 == input2:
                    program[output] = 1
                else:
                    program[output] = 0
                next_code_idx[0] += 4

        else:
            if op_code == 3:
                tgt_idx = program[idx_val + 1]
                param = int(input("Please enter your input value: "))
                program[tgt_idx] = param
            elif op_code == 4:
                tgt_idx = IntcodeComputerV2._input_for_mode(mode1, 1, idx_val, program)
                print(tgt_idx)
            else:
                raise ValueError(f"Unknown op code {op_code}")

            next_code_idx[0] += 2

    @staticmethod
    def _input_for_mode(mode: int, mode_pos: int, program_idx: int,
                        program: List[int]) -> int:
        if mode == IntcodeComputerV2.POSITION_MODE:
            input_idx = program[program_idx + mode_pos]
            input_val = program[input_idx]
        else:
            input_val = program[program_idx + mode_pos]
        return input_val

    @staticmethod
    def _interpret_instruction(instruction_code: int) -> Instruction:
        op_code = instruction_code % 100
        mode1 = instruction_code // 100 % 10
        mode2 = instruction_code // 1000 % 10
        mode3 = instruction_code // 10000 % 10
        return op_code, mode1, mode2, mode3


def day05_part1(puzzle_data: List[int]) -> int:
    computer = IntcodeComputerV2(puzzle_data)
    return computer.run()[0]


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(val) for val in open(data_file).read().strip().split(',')]
    print("* ENTER 1 FOR PART ONE *\n* ENTER 5 FOR PART TWO *")
    day05_part1(data)

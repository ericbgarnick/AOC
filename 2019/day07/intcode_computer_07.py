from typing import List, Tuple, Optional

Instruction = Tuple[int, int, int, int]


class IntcodeComputerV1:
    HALT = 99

    def __init__(self, original_program: List[int]):
        self._original_program = [v for v in original_program]

    def run(self) -> List[int]:
        program = [v for v in self._original_program]
        next_code_idx = [0]
        while program[next_code_idx[0]] != self.HALT:
            self._execute_op_code(program, next_code_idx)
        return program

    @staticmethod
    def _execute_op_code(program: List[int], next_code_idx: List[int]):
        idx_val = next_code_idx[0]
        op_code = program[idx_val]
        input1, input2 = program[idx_val + 1: idx_val + 3]
        output = program[idx_val + 3]

        if op_code == 1:
            program[output] = program[input1] + program[input2]
        elif op_code == 2:
            program[output] = program[input1] * program[input2]
        else:
            raise ValueError(f"Unknown op code {op_code}")

        next_code_idx[0] += 4

    def restore_alarm_state(self, noun: int, verb: int):
        self._original_program[1] = noun
        self._original_program[2] = verb


class IntcodeComputerV2(IntcodeComputerV1):
    PARAMETERIZED_PROCESSES = [3, 4]
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    @staticmethod
    def _execute_op_code(program: List[int],
                         next_code_idx: List[int]) -> Optional[int]:
        output = None
        idx_val = next_code_idx[0]
        instruction_code = program[idx_val]
        op_code, mode1, mode2, mode3 = IntcodeComputerV2._interpret_instruction(instruction_code)

        if op_code in IntcodeComputerV2.PARAMETERIZED_PROCESSES:
            if op_code == 3:
                tgt_idx = program[idx_val + 1]
                param = int(input("Please enter your input value: "))
                program[tgt_idx] = param
            else:
                # op_code == 4
                tgt_idx = IntcodeComputerV2._input_for_mode(mode1, 1, idx_val, program)
                output = tgt_idx

            next_code_idx[0] += 2

        else:
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

        return output

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


class IntcodeComputerV3(IntcodeComputerV2):
    def __init__(self, original_program: List[int], input_signals: List[int]):
        super().__init__(original_program)
        self._input_signals = input_signals
        self._result_program = None

    @property
    def result_program(self) -> Optional[List[int]]:
        return self._result_program

    def run(self) -> Optional[int]:
        output_signal = None
        program = [v for v in self._original_program]
        next_code_idx = [0]
        while program[next_code_idx[0]] != self.HALT:
            output_signal = self._execute_op_code(program, next_code_idx)
        return output_signal

    def _execute_op_code(self, program: List[int],
                         next_code_idx: List[int]) -> Optional[int]:
        output = None
        idx_val = next_code_idx[0]
        instruction_code = program[idx_val]
        op_code, mode1, mode2, mode3 = IntcodeComputerV2._interpret_instruction(instruction_code)

        if op_code in IntcodeComputerV2.PARAMETERIZED_PROCESSES:
            if op_code == 3:
                tgt_idx = program[idx_val + 1]
                param = self._input_signals.pop(0)
                program[tgt_idx] = param
            else:
                # op_code == 4
                tgt_idx = IntcodeComputerV2._input_for_mode(mode1, 1, idx_val, program)
                output = tgt_idx

            next_code_idx[0] += 2

        else:
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

        return output

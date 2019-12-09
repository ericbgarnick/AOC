from typing import List, Tuple

Instruction = Tuple[int, int, int, int]


class IntcodeComputerV4:
    HALT = 99
    PARAMETERIZED_PROCESSES = [3, 4]
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def __init__(self, original_program: List[int]):
        self._program = [v for v in original_program]
        self._next_code_idx = 0
        self._relative_base = 0

    def run(self) -> List[int]:
        while self._program[self._next_code_idx] != self.HALT:
            self._execute_op_code()
        return self._program

    def _execute_op_code(self):
        instruction_code = self._program[self._next_code_idx]
        op_code, mode1, mode2, mode3 = self._interpret_instruction(instruction_code)

        if op_code in self.PARAMETERIZED_PROCESSES:
            if op_code == 3:
                tgt_idx = self._program[self._next_code_idx + 1]
                param = int(input("Please enter your input value: "))
                self._program[tgt_idx] = param
            else:
                # op_code == 4
                tgt_idx = self._input_for_mode(mode1, 1)
                print(tgt_idx)

            self._next_code_idx += 2

        else:
            input1 = self._input_for_mode(mode1, 1)
            input2 = self._input_for_mode(mode2, 2)
            output = self._program[self._next_code_idx + 3]

            if op_code == 1:
                self._program[output] = input1 + input2
                self._next_code_idx += 4
            elif op_code == 2:
                self._program[output] = input1 * input2
                self._next_code_idx += 4
            elif op_code == 5:
                if input1:
                    self._next_code_idx = input2
                else:
                    self._next_code_idx += 3
            elif op_code == 6:
                if not input1:
                    self._next_code_idx = input2
                else:
                    self._next_code_idx += 3
            elif op_code == 7:
                if input1 < input2:
                    self._program[output] = 1
                else:
                    self._program[output] = 0
                self._next_code_idx += 4
            elif op_code == 8:
                if input1 == input2:
                    self._program[output] = 1
                else:
                    self._program[output] = 0
                self._next_code_idx += 4
            elif op_code == 9:
                self._relative_base += input1
                self._next_code_idx += 2

    def _input_for_mode(self, mode: int, mode_pos: int) -> int:
        if mode == self.POSITION_MODE:
            input_idx = self._program[self._next_code_idx + mode_pos]
            input_val = self._program[input_idx]
        elif mode == self.IMMEDIATE_MODE:
            input_val = self._program[self._next_code_idx + mode_pos]
        else:
            # RELATIVE MODE
            input_idx = self._program[self._relative_base + mode_pos]
            input_val = self._program[input_idx]
        return input_val

    @staticmethod
    def _interpret_instruction(instruction_code: int) -> Instruction:
        op_code = instruction_code % 100
        mode1 = instruction_code // 100 % 10
        mode2 = instruction_code // 1000 % 10
        mode3 = instruction_code // 10000 % 10
        return op_code, mode1, mode2, mode3

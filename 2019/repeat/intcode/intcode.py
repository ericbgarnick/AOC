from typing import List


class Computer:
    HALT = 99

    def __init__(self, code: List[int], debug: bool = False):
        self._code = code
        self._debug = debug

    def dump(self):
        return self._code

    def run(self):
        cur_idx = 0
        opcode = self._code[cur_idx]
        while opcode != Computer.HALT:
            self._process_opcode(cur_idx)
            cur_idx += 4
            opcode = self._code[cur_idx]

    def _process_opcode(self, opcode_idx: int):
        opcode = self._code[opcode_idx]
        input_idx_1 = self._code[opcode_idx + 1]
        input_idx_2 = self._code[opcode_idx + 2]
        output_idx = self._code[opcode_idx + 3]
        if self._debug:
            print("OPCODE:", opcode)
            print("INPUT 1:", input_idx_1)
            print("INPUT 2:", input_idx_2)
            print("OUTPUT:", output_idx)
        if opcode == 1:
            self._code[output_idx] = self._code[input_idx_1] + self._code[input_idx_2]
        elif opcode == 2:
            self._code[output_idx] = self._code[input_idx_1] * self._code[input_idx_2]

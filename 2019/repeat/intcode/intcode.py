from typing import List, Dict


class Computer:
    HALT = 99

    def __init__(self, code: List[int], debug: bool = False):
        self._code = code
        self._memory = []
        self.initialize({})  # Copy over initial code
        self._debug = debug

    def initialize(self, init_values: Dict[int, int]):
        """
        Update self._memory with init_values.

        Keys are indexes in memory, values are values to set in memory.
        """
        self._memory = [val for val in self._code]
        for index, value in init_values.items():
            self._memory[index] = value

    def run(self):
        cur_idx = 0
        opcode = self._memory[cur_idx]
        while opcode != Computer.HALT:
            self._process_opcode(cur_idx)
            cur_idx += 4
            opcode = self._memory[cur_idx]

    def _process_opcode(self, opcode_idx: int):
        opcode = self._memory[opcode_idx]
        input_idx_1 = self._memory[opcode_idx + 1]
        input_idx_2 = self._memory[opcode_idx + 2]
        output_idx = self._memory[opcode_idx + 3]
        if self._debug:
            print("OPCODE:", opcode)
            print("INPUT 1:", input_idx_1)
            print("INPUT 2:", input_idx_2)
            print("OUTPUT:", output_idx)
        if opcode == 1:
            self._memory[output_idx] = self._memory[input_idx_1] + self._memory[input_idx_2]
        elif opcode == 2:
            self._memory[output_idx] = self._memory[input_idx_1] * self._memory[input_idx_2]

    def dump(self):
        return self._memory

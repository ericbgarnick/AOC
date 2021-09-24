"""Implementation for Day 5"""
from typing import List, Dict, Tuple


class UnknownOpCode(Exception):
    def __init__(self, opcode):
        super().__init__(f"Received opcode {opcode}")


class Computer:
    # Parameter modes
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    # Instructions
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8

    # Distance to advance instruction pointer for an instruction
    POINTER_OFFSET = {
        ADD: 4,
        MULTIPLY: 4,
        INPUT: 2,
        OUTPUT: 2,
        JUMP_IF_TRUE: 3,
        JUMP_IF_FALSE: 3,
        LESS_THAN: 4,
        EQUALS: 4,
    }

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
        instruction_pointer = 0
        opcode, *pmodes = self._parse_opcode(instruction_pointer)
        while opcode != Computer.HALT:
            instruction_pointer = self._process_opcode(instruction_pointer, opcode, *pmodes)
            opcode, *pmodes = self._parse_opcode(instruction_pointer)

    def _parse_opcode(self, ptr: int) -> Tuple[int, int, int, int]:
        pmodes, opcode = divmod(self._memory[ptr], 100)
        pmode_1 = pmode_2 = pmode_3 = 0
        if pmodes:
            pmodes, pmode_1 = divmod(pmodes, 10)
        if pmodes:
            pmodes, pmode_2 = divmod(pmodes, 10)
        if pmodes:
            pmodes, pmode_3 = divmod(pmodes, 10)
        return opcode, pmode_1, pmode_2, pmode_3

    def _process_opcode(self, ptr: int, opcode: int, *pmodes: List[int]) -> int:
        pointer_offset = self.POINTER_OFFSET[opcode]
        params = self._memory[ptr + 1: ptr + pointer_offset]

        values = []
        for i, p in enumerate(params):
            mode = pmodes[i]
            if mode == self.POSITION_MODE:
                values.append(self._memory[p])
            elif mode == self.IMMEDIATE_MODE:
                values.append(p)

        if self._debug:
            print("INSTRUCTION POINTER:", ptr)
            print("OPCODE:", opcode)
            for i, p in enumerate(params):
                try:
                    v = values[i]
                except IndexError:
                    v = None
                print(f"PARAM {i}: {p} MODE: {pmodes[i]} VALUE: {v}")

        if opcode == self.ADD:
            self._memory[params[2]] = values[0] + values[1]
        elif opcode == self.MULTIPLY:
            self._memory[params[2]] = values[0] * values[1]
        elif opcode == self.INPUT:
            self._memory[params[0]] = int(input("INPUT: "))
        elif opcode == self.OUTPUT:
            print(values[0])
        elif opcode == self.JUMP_IF_TRUE:
            if values[0] != 0:
                ptr = values[1]
                pointer_offset = 0
        elif opcode == self.JUMP_IF_FALSE:
            if values[0] == 0:
                ptr = values[1]
                pointer_offset = 0
        elif opcode == self.LESS_THAN:
            self._memory[params[2]] = 1 if values[0] < values[1] else 0
        elif opcode == self.EQUALS:
            self._memory[params[2]] = 1 if values[0] == values[1] else 0
        else:
            raise UnknownOpCode(opcode)

        return ptr + pointer_offset

    def dump(self):
        return self._memory

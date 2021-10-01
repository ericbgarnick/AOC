"""Implementation for Day 7"""
from collections import deque
from typing import List, Dict, Tuple, Optional, Deque


class UnknownOpCode(Exception):
    def __init__(self, opcode):
        super().__init__(f"Received opcode {opcode}")


class UnknownIOSource(Exception):
    def __init__(self, source: str):
        super().__init__(source)


class UnknownIODestination(Exception):
    def __init__(self, destination: str):
        super().__init__(destination)


class EmptyInput(Exception):
    pass


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

    STDIN_IO_SRC = "stdin"
    STDOUT_IO_DEST = "stdout"
    MEMBUF_IO_SRC = "mem_src"
    MEMBUF_IO_DEST = "mem_dest"

    def __init__(
            self,
            code: List[int],
            identifier: str = "X",
            io_src: str = STDIN_IO_SRC,
            io_dest: str = STDOUT_IO_DEST,
            custom_input_buffer: Optional[Deque] = None,
            custom_output_buffer: Optional[Deque] = None,
            debug: bool = False,
    ):
        self._id = identifier
        self._instruction_pointer = 0
        self._code = code
        self._memory = []
        self.initialize({})  # Copy over initial code
        self._io_src = io_src
        self._io_dest = io_dest
        self._debug = debug
        self._input_buffer = deque() if custom_input_buffer is None else custom_input_buffer
        self._output_buffer = deque() if custom_output_buffer is None else custom_output_buffer
        self._input_history = []
        self._output_history = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def input_history(self) -> List[int]:
        return [val for val in self._input_history]

    @property
    def output_history(self) -> List[int]:
        return [val for val in self._output_history]

    def initialize(self, init_values: Dict[int, int]):
        """
        Update self._memory with init_values.

        Keys are indexes in memory, values are values to set in memory.
        """
        self._instruction_pointer = 0
        self._memory = [val for val in self._code]
        for index, value in init_values.items():
            self._memory[index] = value

    def set_input_buffer(self, input_buffer: Deque):
        self._input_buffer = input_buffer

    def set_output_buffer(self, output_buffer: Deque):
        self._output_buffer = output_buffer

    def get_input_buffer(self) -> Deque:
        return self._input_buffer

    def get_output_buffer(self) -> Deque:
        return self._output_buffer

    def add_input(self, input_value: int):
        self._input_buffer.append(input_value)

    def get_output(self) -> int:
        return self._output_buffer.popleft()

    def run(self) -> int:
        opcode, *pmodes = self._parse_opcode()
        while opcode != Computer.HALT:
            self._process_opcode(opcode, *pmodes)
            opcode, *pmodes = self._parse_opcode()
        return 0

    def _parse_opcode(self) -> Tuple[int, int, int, int]:
        pmodes, opcode = divmod(self._memory[self._instruction_pointer], 100)
        pmode_1 = pmode_2 = pmode_3 = 0
        if pmodes:
            pmodes, pmode_1 = divmod(pmodes, 10)
        if pmodes:
            pmodes, pmode_2 = divmod(pmodes, 10)
        if pmodes:
            pmodes, pmode_3 = divmod(pmodes, 10)
        return opcode, pmode_1, pmode_2, pmode_3

    def _process_opcode(self, opcode: int, *pmodes: List[int]):
        pointer_offset = self.POINTER_OFFSET[opcode]
        params = self._memory[self._instruction_pointer + 1: self._instruction_pointer + pointer_offset]

        values = []
        for i, p in enumerate(params):
            mode = pmodes[i]
            if mode == self.POSITION_MODE:
                values.append(self._memory[p])
            elif mode == self.IMMEDIATE_MODE:
                values.append(p)

        if self._debug:
            print("COMPUTER:", self._id)
            print("INSTRUCTION POINTER:", self._instruction_pointer)
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
            ipt = self._get_input()
            self._memory[params[0]] = ipt
            self._input_history.append(ipt)
        elif opcode == self.OUTPUT:
            self._output_history.append(values[0])
            self._add_output(values[0])
        elif opcode == self.JUMP_IF_TRUE:
            if values[0] != 0:
                self._instruction_pointer = values[1]
                pointer_offset = 0
        elif opcode == self.JUMP_IF_FALSE:
            if values[0] == 0:
                self._instruction_pointer = values[1]
                pointer_offset = 0
        elif opcode == self.LESS_THAN:
            self._memory[params[2]] = 1 if values[0] < values[1] else 0
        elif opcode == self.EQUALS:
            self._memory[params[2]] = 1 if values[0] == values[1] else 0
        else:
            raise UnknownOpCode(opcode)

        self._instruction_pointer += pointer_offset

    def _get_input(self) -> int:
        try:
            if self._io_src == Computer.STDIN_IO_SRC:
                return int(input("INPUT: "))
            elif self._io_src == Computer.MEMBUF_IO_SRC:
                return self._input_buffer.popleft()
            else:
                raise UnknownIOSource(self._io_src)
        except IndexError:
            raise EmptyInput()

    def _add_output(self, output_val: int):
        if self._io_dest == Computer.STDOUT_IO_DEST:
            print(output_val)
        elif self._io_dest == Computer.MEMBUF_IO_DEST:
            self._output_buffer.append(output_val)
        else:
            raise UnknownIODestination(self._io_dest)

    def dump(self):
        return self._memory

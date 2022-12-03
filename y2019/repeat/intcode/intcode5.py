"""Implementation for Day 9 - Add Relative Mode and relative offset"""
from collections import deque
from typing import List, Dict, Tuple, Optional, Deque


class UnknownOpCode(Exception):
    def __init__(self, opcode):
        super().__init__(opcode)


class UnknownMode(Exception):
    def __init__(self, mode: str):
        super().__init__(mode)


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
    RELATIVE_MODE = 2

    # Instructions
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    REL_BASE_OFFSET = 9

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
        REL_BASE_OFFSET: 2,
    }

    HALT = 99

    # Read from/write to stdin/stdout
    STDIN_IO_SRC = "stdin"
    STDOUT_IO_DEST = "stdout"
    # Maintain in-memory queue
    MEMBUF_IO_SRC = "mem_src"
    MEMBUF_IO_DEST = "mem_dest"
    # Interact with injected object dependency
    OBJECT_IO_SRC = "obj_src"
    OBJECT_IO_DEST = "obj_dest"

    def __init__(
            self,
            code: List[int],
            identifier: str = "X",
            io_src_type: str = STDIN_IO_SRC,
            io_dest_type: str = STDOUT_IO_DEST,
            custom_input_src: Optional = None,
            custom_output_dest: Optional = None,
            debug: bool = False,
    ):
        self._id = identifier
        self._instruction_pointer = 0
        self._relative_base = 0
        self._code = code
        self._memory = []
        self.initialize({})  # Copy over initial code
        self._io_src_type = io_src_type
        self._io_dest_type = io_dest_type
        self._debug = debug
        self._input_src = deque() if custom_input_src is None else custom_input_src
        self._output_dest = deque() if custom_output_dest is None else custom_output_dest
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
        self._relative_base = 0
        self._memory = [val for val in self._code]
        for index, value in init_values.items():
            self._set_value(value, index)

    def set_input_buffer(self, input_buffer: Deque):
        self._input_src = input_buffer

    def set_output_buffer(self, output_buffer: Deque):
        self._output_dest = output_buffer

    def get_input_buffer(self) -> Deque:
        return self._input_src

    def get_output_buffer(self) -> Deque:
        return self._output_dest

    def add_input(self, input_value: int):
        self._input_src.append(input_value)

    def get_output(self) -> int:
        return self._output_dest.popleft()

    def run(self) -> int:
        opcode, *pmodes = self._parse_opcode()
        while opcode != Computer.HALT:
            self._process_opcode(opcode, *pmodes)
            opcode, *pmodes = self._parse_opcode()
        return 0

    def _parse_opcode(self) -> Tuple[int, int, int, int]:
        pmodes, opcode = divmod(self._get_value(), 100)
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
        params = [self._get_value(self._instruction_pointer + i) for i in range(1, pointer_offset)]

        values = []
        for i, p in enumerate(params):
            mode = pmodes[i]
            if mode == Computer.POSITION_MODE:
                values.append(self._get_value(p))
            elif mode == Computer.IMMEDIATE_MODE:
                values.append(p)
            elif mode == Computer.RELATIVE_MODE:
                params[i] = self._relative_base + p
                values.append(self._get_value(params[i]))
            else:
                raise UnknownMode(mode)

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

        if opcode == Computer.ADD:
            self._set_value(values[0] + values[1], params[2])
        elif opcode == Computer.MULTIPLY:
            self._set_value(values[0] * values[1], params[2])
        elif opcode == Computer.INPUT:
            ipt = self._get_input()
            self._set_value(ipt, params[0])
            self._input_history.append(ipt)
        elif opcode == Computer.OUTPUT:
            self._output_history.append(values[0])
            self._add_output(values[0])
        elif opcode == Computer.JUMP_IF_TRUE:
            if values[0] != 0:
                self._instruction_pointer = values[1]
                pointer_offset = 0
        elif opcode == Computer.JUMP_IF_FALSE:
            if values[0] == 0:
                self._instruction_pointer = values[1]
                pointer_offset = 0
        elif opcode == Computer.LESS_THAN:
            value = 1 if values[0] < values[1] else 0
            self._set_value(value, params[2])
        elif opcode == Computer.EQUALS:
            value = 1 if values[0] == values[1] else 0
            self._set_value(value, params[2])
        elif opcode == Computer.REL_BASE_OFFSET:
            self._relative_base += values[0]
        else:
            raise UnknownOpCode(opcode)

        self._instruction_pointer += pointer_offset

    def _get_input(self) -> int:
        try:
            if self._io_src_type == Computer.STDIN_IO_SRC:
                return int(input("INPUT: "))
            elif self._io_src_type == Computer.MEMBUF_IO_SRC:
                return self._input_src.popleft()
            elif self._io_src_type == Computer.OBJECT_IO_SRC:
                return self._input_src.get_input()
            else:
                raise UnknownIOSource(self._io_src_type)
        except IndexError:
            raise EmptyInput()

    def _add_output(self, output_val: int):
        if self._io_dest_type == Computer.STDOUT_IO_DEST:
            print(output_val)
        elif self._io_dest_type == Computer.MEMBUF_IO_DEST:
            self._output_dest.append(output_val)
        elif self._io_dest_type == Computer.OBJECT_IO_DEST:
            self._output_dest.add_output(output_val)
        else:
            raise UnknownIODestination(self._io_dest_type)

    def _get_value(self, idx: Optional[int] = None) -> int:
        idx = self._instruction_pointer if idx is None else idx
        self._pad_memory(idx)
        return self._memory[idx]

    def _set_value(self, value: int, idx: int):
        self._pad_memory(idx)
        self._memory[idx] = value

    def _pad_memory(self, idx: int):
        self._memory.extend([0 for _ in range(idx + 1 - len(self._memory))])

    def dump(self):
        return self._memory

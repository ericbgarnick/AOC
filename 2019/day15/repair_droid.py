import sys
from enum import Enum
from typing import List, Tuple, Callable, Dict, Optional


Point = Tuple[int, int]


####################
# - Repair Droid - #
####################
class RepairDroid:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    COMMAND_CODES = {'w': NORTH, 's': SOUTH, 'a': WEST, 'd': EAST}
    SYMBOL_FOR_DIR = {NORTH: '^', SOUTH: 'v', WEST: '<', EAST: '>'}

    UNKNOWN = " "
    WALL = 0
    FLOOR = 1
    OXYGEN = 2
    TERRAIN_TYPES = {WALL: "#", FLOOR: ".", OXYGEN: "o"}

    def __init__(self):
        self._computer = None  # type: Optional[IntcodeComputerV5]
        self._cur_position = (0, 0)
        self._known_positions = {}  # type: Dict[Point, str]
        self._cur_direction = RepairDroid.NORTH
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0

    @property
    def symbol(self) -> str:
        return RepairDroid.SYMBOL_FOR_DIR[self._cur_direction]

    def run(self, program: List[int]):
        self._computer = IntcodeComputerV5(program, self)
        fd, oldterm = self._set_noncanonical_term()
        self._computer.run()
        self._reset_term(fd, oldterm)

    ###################
    # - I/O methods - #
    ###################
    @staticmethod
    def _set_noncanonical_term() -> Tuple:
        import sys
        import termios

        fd = sys.stdin.fileno()
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON
        newattr[3] = newattr[3] & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldterm = termios.tcgetattr(fd)

        return fd, oldterm

    @staticmethod
    def _reset_term(fd, oldterm):
        import termios
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    def get_input(self) -> int:
        self.display()
        next_cmd = sys.stdin.read(1)
        next_cmd = next_cmd[0] if next_cmd else next_cmd
        self._cur_direction = RepairDroid.COMMAND_CODES[next_cmd]
        return self._cur_direction

    def process_output(self, output_val: int):
        terrain_type = RepairDroid.TERRAIN_TYPES[output_val]
        if output_val == RepairDroid.WALL:
            self._record_terrain(terrain_type)
        elif output_val == RepairDroid.FLOOR:
            self._record_terrain(terrain_type, next_space=False)
            self._move()
        elif output_val == RepairDroid.OXYGEN:
            self._record_terrain(terrain_type)
        else:
            raise ValueError(f"Invalid output: {output_val}")

    #######################
    # - Display Methods - #
    #######################
    def display(self):
        screen = self._create_screen()
        self._mark_terrain(screen)
        self._mark_self(screen)
        print('\n'.join([''.join(row) for row in screen]))

    def _create_screen(self) -> List[List[str]]:
        empty = RepairDroid.UNKNOWN
        x_size = self._max_x - self._min_x + 1
        y_size = self._max_y - self._min_y + 1
        return [[empty for _ in range(x_size)]
                for _ in range(y_size)]

    def _mark_terrain(self, screen: List[List[str]]):
        for coords, terrain_type in self._known_positions.items():
            col, row = coords
            # Adjust row and col for moving screen
            screen[row - self._min_y][col - self._min_x] = terrain_type

    def _mark_self(self, screen: List[List[str]]):
        cur_col, cur_row = self._cur_position
        screen[cur_row - self._min_y][cur_col - self._min_x] = self.symbol

    ############################
    # - Game control methods - #
    ############################
    def _record_terrain(self, terrain_type: str, next_space: bool = True):
        if next_space:
            space = self._get_next_space()
            self._update_min_max(space)
        else:
            space = self._cur_position
        self._known_positions[space] = terrain_type

    def _move(self):
        self._cur_position = self._get_next_space()
        self._update_min_max(self._cur_position)

    def _update_min_max(self, pos: Point):
        cur_x, cur_y = pos

        self._max_x = max(self._max_x, cur_x)
        self._min_x = min(self._min_x, cur_x)

        self._max_y = max(self._max_y, cur_y)
        self._min_y = min(self._min_y, cur_y)

    def _get_next_space(self) -> Point:
        cur_x, cur_y = self._cur_position
        if self._cur_direction == RepairDroid.NORTH:
            next_space = cur_x, cur_y - 1
        elif self._cur_direction == RepairDroid.SOUTH:
            next_space = cur_x, cur_y + 1
        elif self._cur_direction == RepairDroid.WEST:
            next_space = cur_x - 1, cur_y
        else:
            next_space = cur_x + 1, cur_y
        return next_space


########################
# - Intcode Computer - #
########################
Instruction = Tuple[int, int, int, int]


class MemoryOperation(Enum):
    READ = 'READ'
    WRITE = 'WRITE'


class MemoryAccessError(Exception):
    DEFAULT_MESSAGE = "Invalid memory access operation: {}"

    def __init__(self, operation: str, message: str = None):
        self.operation = operation
        self.message = message or self.DEFAULT_MESSAGE.format(self.operation)


class IntcodeComputerV5:
    HALT = 99
    PARAMETERIZED_PROCESSES = [3, 4]
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def __init__(self, original_program: List[int], droid: RepairDroid):
        self._program = [v for v in original_program]
        self._droid = droid
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
                output = self._output_for_mode(mode1, 1)
                param = self._droid.get_input()
                self._access_memory(MemoryOperation.WRITE, output, param)
            elif op_code == 4:
                tgt_idx = self._input_for_mode(mode1, 1)
                self._droid.process_output(tgt_idx)
            else:
                raise ValueError(f"Invalid op code {op_code}")

            self._next_code_idx += 2

        else:
            input1 = self._input_for_mode(mode1, 1)
            input2 = self._input_for_mode(mode2, 2)
            output = self._output_for_mode(mode3, 3)

            if op_code == 1:
                self._combine_op(input1, input2, output, int.__add__)
            elif op_code == 2:
                self._combine_op(input1, input2, output, int.__mul__)
            elif op_code == 5:
                self._zero_val(input1, input2, int.__ne__)
            elif op_code == 6:
                self._zero_val(input1, input2, int.__eq__)
            elif op_code == 7:
                self._compare_op(input1, input2, output, int.__lt__)
            elif op_code == 8:
                self._compare_op(input1, input2, output, int.__eq__)
            elif op_code == 9:
                self._relative_base += input1
                self._next_code_idx += 2

    ###########################
    # - Instruction Parsing - #
    ###########################
    def _input_for_mode(self, mode: int, mode_pos: int) -> int:
        if mode == self.POSITION_MODE:
            input_idx = self._access_memory(MemoryOperation.READ,
                                            self._next_code_idx + mode_pos)
            input_val = self._access_memory(MemoryOperation.READ, input_idx)
        elif mode == self.IMMEDIATE_MODE:
            input_val = self._access_memory(MemoryOperation.READ,
                                            self._next_code_idx + mode_pos)
        else:
            # RELATIVE MODE
            offset = self._access_memory(MemoryOperation.READ,
                                         self._next_code_idx + mode_pos)
            input_idx = self._relative_base + offset
            input_val = self._access_memory(MemoryOperation.READ, input_idx)
        return input_val

    def _output_for_mode(self, mode: int, mode_pos: int) -> int:
        output = self._access_memory(MemoryOperation.READ,
                                     self._next_code_idx + mode_pos)
        if mode == self.RELATIVE_MODE:
            output += self._relative_base
        return output

    @staticmethod
    def _interpret_instruction(instruction_code: int) -> Instruction:
        op_code = instruction_code % 100
        mode1 = instruction_code // 100 % 10
        mode2 = instruction_code // 1000 % 10
        mode3 = instruction_code // 10000 % 10
        return op_code, mode1, mode2, mode3

    #########################
    # - Memory Management - #
    #########################
    def _access_memory(self, operation: MemoryOperation, address: int,
                       value: int = None,):
        if len(self._program) <= address:
            self._extend_memory(address)

        if operation == MemoryOperation.READ:
            return self._program[address]
        elif operation == MemoryOperation.WRITE:
            self._program[address] = value
        else:
            raise MemoryAccessError(operation.value)

    def _extend_memory(self, address: int):
        self._program += [0 for _ in range(address + 1 - len(self._program))]

    #########################
    # - Operation Helpers - #
    #########################
    def _combine_op(self, input1: int, input2: int, output: int,
                    operation: Callable):
        self._access_memory(MemoryOperation.WRITE, output,
                            operation(input1, input2))
        self._next_code_idx += 4

    def _zero_val(self, input1: int, input2: int, operation: Callable):
        if operation(input1, 0):
            self._next_code_idx = input2
        else:
            self._next_code_idx += 3

    def _compare_op(self, input1: int, input2: int, output: int,
                    operation: Callable):
        val = int(operation(input1, input2))
        self._access_memory(MemoryOperation.WRITE, output, val)
        self._next_code_idx += 4

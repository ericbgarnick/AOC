import pickle
import sys
from enum import Enum
from queue import Queue
from typing import List, Tuple, Callable, Dict, Optional


######################
# - Arcade Cabinet - #
######################

class OutputType(Enum):
    X_POS = "X_POS"
    Y_POS = "Y_POS"
    TILE_ID = "TILE_ID"


class ArcadeCabinet:
    # history saving
    INPUT_FILENAME = "save_file"
    YES = "Y"
    NO = "N"
    COMMAND_CUTOFF = 20

    # Runtime
    OUTPUT_LOOP = {
        OutputType.X_POS.value: OutputType.Y_POS.value,
        OutputType.Y_POS.value: OutputType.TILE_ID.value,
        OutputType.TILE_ID.value: OutputType.X_POS.value
    }
    TEST_MODE = 1
    PLAY_MODE = 2

    # Game-board display
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4
    TILE_SYMBOLS = {
        EMPTY: ' ',
        WALL: '#',
        BLOCK: 'x',
        PADDLE: '—',
        BALL: 'o'
    }

    # Input/Output
    SCORE_CODE = (-1, 0)
    COMMAND_CODES = {'a': -1, 's': 0, '': 0, 'd': 1}

    def __init__(self):
        self._computer = None  # type: Optional[IntcodeComputerV5]
        self._screen_contents = {}  # type: Dict[Tuple[int, int], int]
        self._next_output = OutputType.X_POS.value
        self._cur_x = None  # type: Optional[int]
        self._cur_y = None  # type: Optional[int]
        self._max_x = 0
        self._max_y = 0
        self._score = 0
        self._input_buffer = Queue()
        self._command_history = []

    def run(self, program: List[int]):
        mode = int(input(f"Enter {self.TEST_MODE} for TEST MODE, "
                         f"ENTER {self.PLAY_MODE} for PLAY MODE: "))
        program[0] = mode
        self._computer = IntcodeComputerV5(program, self)
        if mode == self.TEST_MODE:
            self._run_test_mode()
        else:
            self._run_play_mode()

    def _run_test_mode(self):
        self._computer.run()

    def _run_play_mode(self):
        load_input = input(f"Load saved command input? ({self.YES}/{self.NO}) ")
        if load_input.upper() == self.YES:
            self._load_input()

        fd, oldterm = self._set_noncanonical_term()
        self._computer.run()
        self._reset_term(fd, oldterm)

        save_history = input(f"Save command history? ({self.YES}/{self.NO}) ")
        if save_history.upper() == self.YES:
            self._dump_history()

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

    def tile_type_count(self, tile_type: int) -> int:
        return len([p for p, t in self._screen_contents.items()
                    if t == tile_type])

    def get_input(self) -> int:
        self.display()
        if not self._input_buffer.empty():
            next_cmd = self._input_buffer.get()
        else:
            print("Move <-a/-s/->d: ")
            next_cmd = sys.stdin.read(1)
        next_cmd = next_cmd[0] if next_cmd else next_cmd
        self._command_history.append(next_cmd)
        return self.COMMAND_CODES[next_cmd]

    def process_output(self, output_val: int):
        if self._next_output == OutputType.X_POS.value:
            self._cur_x = output_val
            self._max_x = max(self._max_x, self._cur_x)
        elif self._next_output == OutputType.Y_POS.value:
            self._cur_y = output_val
            self._max_y = max(self._max_y, self._cur_y)
        else:
            if (self._cur_x, self._cur_y) == self.SCORE_CODE:
                self._score = output_val
            else:
                self._screen_contents[(self._cur_x, self._cur_y)] = output_val
        self._next_output = self.OUTPUT_LOOP[self._next_output]

    def display(self):
        empty = self.TILE_SYMBOLS[self.EMPTY]
        screen = [[empty for _ in range(self._max_x + 1)]
                  for _ in range(self._max_y + 1)]
        for coords, tile_type in self._screen_contents.items():
            col, row = coords
            symbol = self.TILE_SYMBOLS[tile_type]
            screen[row][col] = symbol

        score_msg = f"SCORE: {self._score}"
        play_area = '\n'.join([''.join(row) for row in screen])
        print(f"{score_msg}\n{play_area}")

    def _load_input(self):
        try:
            with open(self.INPUT_FILENAME, 'rb') as save_file:
                for cmd in pickle.load(save_file):
                    self._input_buffer.put(cmd)
        except FileNotFoundError:
            return

    def _dump_history(self):
        to_save = self._command_history[:-self.COMMAND_CUTOFF]
        with open(self.INPUT_FILENAME, 'wb') as save_file:
            pickle.dump(to_save, save_file)
        print(f"Saved {len(to_save)} commands to history")


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

    def __init__(self, original_program: List[int], cabinet: ArcadeCabinet):
        self._program = [v for v in original_program]
        self._cabinet = cabinet
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
                param = self._cabinet.get_input()
                self._access_memory(MemoryOperation.WRITE, output, param)
            elif op_code == 4:
                tgt_idx = self._input_for_mode(mode1, 1)
                self._cabinet.process_output(tgt_idx)
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

from enum import Enum
from typing import List, Tuple, Callable, Dict, Optional


###################
# - Paint Robot - #
###################
class OutputType(Enum):
    COLOR = "COLOR"
    TURN = "TURN"


class Direction(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


class PaintRobot:
    OUTPUT_CYCLE = {OutputType.COLOR.value: OutputType.TURN.value,
                    OutputType.TURN.value: OutputType.COLOR.value}

    DIRECTIONS = {0: Direction.LEFT.value, 1: Direction.RIGHT.value}
    TURNS = {
        Direction.UP.value: {
            Direction.RIGHT.value: Direction.RIGHT.value,
            Direction.LEFT.value: Direction.LEFT.value
        },
        Direction.RIGHT.value: {
            Direction.RIGHT.value: Direction.DOWN.value,
            Direction.LEFT.value: Direction.UP.value
        },
        Direction.DOWN.value: {
            Direction.RIGHT.value: Direction.LEFT.value,
            Direction.LEFT.value: Direction.RIGHT.value
        },
        Direction.LEFT.value: {
            Direction.RIGHT.value: Direction.UP.value,
            Direction.LEFT.value: Direction.DOWN.value
        }
    }

    BLACK = 0
    WHITE = 1
    COLORS = {BLACK: '.', WHITE: '#'}

    def __init__(self):
        self._computer = None  # type: Optional[IntcodeComputerV5]
        self._location = (0, 0)  # type: Tuple[int, int]
        self._direction = Direction.UP.value
        self._output_to_receive = OutputType.COLOR.value
        # {(x, y): color}
        self._painted = {self._location: self.WHITE}

    @property
    def painted(self) -> Dict:
        return self._painted

    def paint(self, program: List[int]):
        self._computer = IntcodeComputerV5(program, self)
        self._computer.run()

    def display(self):
        canvas, x_offset, y_offset = self._create_blank_canvas()
        for loc, color_num in self._painted.items():
            adj_x = loc[0] + x_offset
            adj_y = loc[1] + y_offset
            paint_color = self.COLORS[color_num]
            canvas[adj_y][adj_x] = paint_color
        print('\n'.join(''.join(row) for row in canvas[-1::-1]))

    def _create_blank_canvas(self) -> Tuple[List[List[str]], int, int]:
        x_vals = sorted({p[0] for p in self._painted.keys()})
        y_vals = sorted({p[1] for p in self._painted.keys()})

        min_x = x_vals[0]
        max_x = x_vals[-1]
        min_y = y_vals[0]
        max_y = y_vals[-1]

        x_offset = min_x * -1
        y_offset = min_y * -1

        black_color = self.COLORS[self.BLACK]
        canvas = [[black_color for _ in range(max_x - min_x + 1)]
                  for _ in range(max_y - min_y + 1)]

        return canvas, x_offset, y_offset

    def get_input(self) -> int:
        return self._painted.get(self._location, self.BLACK)

    def process_output(self, output_val: int):
        if self._output_to_receive == OutputType.COLOR.value:
            self._record_paint(output_val)
        else:
            # TURN
            self._make_turn(output_val)
            self._advance()
        self._update_output_to_receive()

    def _record_paint(self, paint_val: int):
        self._painted[self._location] = paint_val

    def _make_turn(self, turn_num: int):
        turn_dir = self.DIRECTIONS[turn_num]
        self._direction = self.TURNS[self._direction][turn_dir]

    def _advance(self):
        if self._direction == Direction.UP.value:
            x = self._location[0]
            y = self._location[1] + 1
        elif self._direction == Direction.RIGHT.value:
            x = self._location[0] + 1
            y = self._location[1]
        elif self._direction == Direction.DOWN.value:
            x = self._location[0]
            y = self._location[1] - 1
        else:
            # LEFT
            x = self._location[0] - 1
            y = self._location[1]
        self._location = (x, y)

    def _update_output_to_receive(self):
        cur_type = self._output_to_receive
        self._output_to_receive = self.OUTPUT_CYCLE[cur_type]


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

    def __init__(self, original_program: List[int], robot: PaintRobot):
        self._program = [v for v in original_program]
        self._robot = robot
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
                param = self._robot.get_input()
                self._access_memory(MemoryOperation.WRITE, output, param)
            elif op_code == 4:
                tgt_idx = self._input_for_mode(mode1, 1)
                self._robot.process_output(tgt_idx)
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


from collections import deque
from typing import Optional

from intcode.intcode5 import Computer


class GameScreen:
    VALUE_TYPE_EMPTY = 0
    VALUE_TYPE_WALL = 1
    VALUE_TYPE_BLOCK = 2
    VALUE_TYPE_PADDLE = 3
    VALUE_TYPE_BALL = 4

    IMAGE_VALUES = {
        0: " ",
        1: "|",
        2: "#",
        3: "–",
        4: "o",
    }

    def __init__(self):
        self.width = 0
        self.height = 0
        self.screen = []

    def __str__(self) -> str:
        image = []
        for row in self.screen:
            image.append("".join([GameScreen.IMAGE_VALUES[val] for val in row]))
        return "\n".join(image)

    def display(self, score: int):
        print(f"SCORE: {score}\n")
        print(self)

    def set_pixel(self, col: int, row: int, val: int):
        while row >= self.height:
            self.screen.append([GameScreen.VALUE_TYPE_EMPTY for _ in range(self.width)])
            self.height += 1
        while col >= self.width:
            for screen_row in self.screen:
                screen_row.append(GameScreen.VALUE_TYPE_EMPTY)
                self.width += 1
        self.screen[row][col] = val


class SimulationState:
    STATE_TYPE_X_COORD = "x"
    STATE_TYPE_Y_COORD = "y"
    STATE_TYPE_VALUE = "v"
    STATE_TYPES = [STATE_TYPE_X_COORD, STATE_TYPE_Y_COORD, STATE_TYPE_VALUE]

    def __init__(self):
        self.score = 0
        self.type_idx = 0  # First output is x-coord
        self.x = None
        self.y = None

    def update(self, value: int) -> Optional[int]:
        state_type = SimulationState.STATE_TYPES[self.type_idx]
        self.type_idx = (self.type_idx + 1) % len(SimulationState.STATE_TYPES)
        if state_type == SimulationState.STATE_TYPE_X_COORD:
            self.x = value
            return None
        elif state_type == SimulationState.STATE_TYPE_Y_COORD:
            self.y = value
            return None
        else:
            if self.x == -1 and self.y == 0:
                self.score = value
                return None
            else:
                return value


class Simulation:
    CODE_SOURCE = "data.txt"

    JOYSTICK = {
        "a": -1,
        "s": 0,
        "d": 1,
    }

    def __init__(self):
        self.input_buffer = deque()
        self.output_buffer = deque()
        self.computer = self.setup_computer()

        self.game_screen = GameScreen()
        self.state = SimulationState()

    def setup_computer(self) -> Computer:
        with open(self.CODE_SOURCE, "r") as f_in:
            data = [int(val) for val in f_in.read().strip().split(",")]
        computer = Computer(
            data,
            io_src_type=Computer.OBJECT_IO_SRC,
            io_dest_type=Computer.OBJECT_IO_DEST,
            custom_input_src=self,
            custom_output_dest=self,
        )
        computer.initialize({0: 2})
        return computer

    def run(self) -> int:
        return self.computer.run()

    def add_output(self, output_val: int):
        pixel_value = self.state.update(output_val)
        if pixel_value is not None:
            self.game_screen.set_pixel(self.state.x, self.state.y, pixel_value)
            self.game_screen.display(self.state.score)

    def get_input(self) -> int:
        return Simulation.JOYSTICK[input()]

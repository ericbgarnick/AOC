from collections import defaultdict
from typing import Tuple


class UnknownOperation(Exception):
    def __init__(self, operation):
        super().__init__(operation)


class Canvas:
    BLACK_VALUE = 0
    WHITE_VALUE = 1

    PAINT = {BLACK_VALUE: " ", WHITE_VALUE: "#"}

    def __init__(self, origin_color: int = BLACK_VALUE):
        self._surface = defaultdict(int)
        self._surface[(0, 0)] = origin_color
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0

    def __str__(self) -> str:
        """
        Return the points in self._surface as a rectangle containing all painted points.

        BLACK spaces are represented as ' ' (blank space)
        WHITE spaces are represented as '#' (octothorpe)
        """
        black_paint = Canvas.PAINT[Canvas.BLACK_VALUE]
        width = self._max_x - self._min_x + 1
        height = self._max_y - self._min_y + 1
        grid = [[black_paint for _ in range(width)] for _ in range(height)]
        for point, value in self._surface.items():
            x = point[0] - self._min_x
            y = point[1] - self._min_y
            grid[y][x] = Canvas.PAINT[value]
        # Grid is built 'upside-down', needs to be flipped
        return "\n".join(["".join(row) for row in grid[::-1]])

    def __len__(self) -> int:
        return len(self._surface)

    def paint(self, value: int, point: Tuple[int, int]):
        self._surface[point] = value
        self._min_x = min(self._min_x, point[0])
        self._max_x = max(self._max_x, point[0])
        self._min_y = min(self._min_y, point[1])
        self._max_y = max(self._max_y, point[1])

    def get_value(self, point: Tuple[int, int]) -> int:
        return self._surface[point]


class Robot:
    UP = "^"
    DOWN = "V"
    LEFT = "<"
    RIGHT = ">"
    DIRECTIONS = {
        UP: {0: LEFT, 1: RIGHT},
        DOWN: {0: RIGHT, 1: LEFT},
        LEFT: {0: DOWN, 1: UP},
        RIGHT: {0: UP, 1: DOWN},
    }

    MOVE_DISTANCE = 1

    PAINT_PANEL = "paint"
    TURN_ROBOT = "turn"
    OUTPUT_OPERATIONS = {
        PAINT_PANEL: TURN_ROBOT,
        TURN_ROBOT: PAINT_PANEL,
    }

    def __init__(self, calibrate: bool = False):
        self._position = (0, 0)  # (X, Y) coords
        canvas_origin_color = Canvas.BLACK_VALUE if calibrate else Canvas.WHITE_VALUE
        self._canvas = Canvas(origin_color=canvas_origin_color)
        self._direction = Robot.UP
        self._next_operation = Robot.PAINT_PANEL

    @property
    def canvas_size(self) -> int:
        return len(self._canvas)

    def display_painting(self):
        print(self._canvas)

    def get_input(self) -> int:
        """
        Return the integer corresponding to the color
        of self._canvas at self._position.
        """
        return self._canvas.get_value(self._position)

    def add_output(self, value: int):
        """
        Receive output from computer and update
        self._canvas or self._direction.
        """
        if self._next_operation == Robot.PAINT_PANEL:
            self._canvas.paint(value, self._position)
        elif self._next_operation == Robot.TURN_ROBOT:
            self._direction = Robot.DIRECTIONS[self._direction][value]
            self._update_position()
        else:
            raise UnknownOperation(self._next_operation)
        self._next_operation = Robot.OUTPUT_OPERATIONS[self._next_operation]

    def _update_position(self, distance: int = MOVE_DISTANCE):
        if self._direction == Robot.UP:
            self._position = (self._position[0], self._position[1] + distance)
        elif self._direction == Robot.DOWN:
            self._position = (self._position[0], self._position[1] - distance)
        elif self._direction == Robot.RIGHT:
            self._position = (self._position[0] + distance, self._position[1])
        elif self._direction == Robot.LEFT:
            self._position = (self._position[0] - distance, self._position[1])

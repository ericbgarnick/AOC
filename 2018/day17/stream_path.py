from enum import Enum
from typing import Optional

from aoc_types import Point


class Direction(Enum):
    DN = "DN"
    LF = "LF"
    RT = "RT"


class StreamPath:
    def __init__(self, x_coord: int, y_coord: int,
                 direction: Direction = Direction.DN):
        self._direction = direction
        self._sibling = None  # type: Optional[StreamPath]
        self._x = x_coord
        self._y = y_coord
        self._source = (x_coord, y_coord)

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def sibling(self) -> 'StreamPath':
        return self._sibling

    @property
    def position(self) -> Point:
        return self._x, self._y

    @property
    def source(self) -> Point:
        return self._source

    @property
    def below(self) -> Point:
        return self._x, self._y + 1

    @property
    def next_position(self) -> Point:
        next_x, next_y = self._x, self._y
        if self._direction == Direction.LF:
            next_x -= 1
        else:
            next_x += 1
        return next_x, next_y

    @property
    def is_falling(self) -> bool:
        return self._direction == Direction.DN

    @property
    def is_alone(self):
        return self._sibling is None

    def set_sibling(self, sibling: 'StreamPath'):
        self._sibling = sibling

    def drop_sibling(self):
        self._sibling = None

    def spread(self):
        if self._direction == Direction.DN:
            print("INVALID DOWN AT", self.position)
        assert self._direction != Direction.DN
        self._x, self._y = self.next_position

    def descend(self):
        self._direction = Direction.DN
        self._y += 1

    def __str__(self):
        if self._direction == Direction.DN:
            dir_symbol = 'v'
        elif self._direction == Direction.LF:
            dir_symbol = '<'
        else:
            dir_symbol = '>'
        return f"({self._x}, {self._y}) {dir_symbol}"

    __repr__ = __str__

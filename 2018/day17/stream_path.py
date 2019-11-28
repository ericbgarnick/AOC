from enum import Enum
from typing import Optional, Set

from clay_map import Point, ClayMap


class Direction(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Material(Enum):
    SAND = 'SAND'
    CLAY = 'CLAY'


class RowEndType(Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class StreamPath:
    def __init__(self, clay_map: ClayMap, direction: Direction):
        self.clay_map = clay_map
        self.direction = direction
        self.dir_fn = getattr(self, '{}'.format(self.direction.value.lower()))
        self.head_pos = None        # type: Optional[Point]
        self.row_end_pos = None     # type: Optional[Point]
        self.row_end_type = None    # type: Optional[RowEndType]
        self.path_history = set()   # type: Set[Point]

    def open_end(self):
        return self.row_end_type == RowEndType.OPEN

    def fill_row(self, source_pos: Point):
        self.head_pos = source_pos
        self._record(self.head_pos)
        next_pos = self.dir_fn(self.head_pos)

        while self._available_to_fill(next_pos):
            self.head_pos = next_pos
            next_pos = self.dir_fn(self.head_pos)
            self._record(self.head_pos)

        self.row_end_pos = self.head_pos

        if self.clay_map.is_clay(next_pos):
            self.row_end_type = RowEndType.CLOSED
        else:
            self.row_end_type = RowEndType.OPEN

    def _record(self, point: Point):
        if self.clay_map.lowest_point >= point[1] >= self.clay_map.highest_point:
            self.path_history.add(point)

    def _available_to_fill(self, next_pos: Point) -> bool:
        """Return True if next_pos is not clay and has
        clay or water under it. Otherwise return False"""
        not_clay = not self.clay_map.is_clay(next_pos)
        clay_below = self.clay_map.is_clay(self.down(next_pos))
        water_below = self.down(next_pos) in self.path_history
        return not_clay and (clay_below or water_below)

    @staticmethod
    def down(point: Point) -> Point:
        """Return the next point down from point"""
        return point[0], point[1] + 1

    @staticmethod
    def up(point: Point) -> Point:
        """Return the next point up from point"""
        return point[0], point[1] - 1

    @staticmethod
    def left(point: Point) -> Point:
        """Return the next point to the left from point"""
        return point[0] - 1, point[1]

    @staticmethod
    def right(point: Point) -> Point:
        """Return the next point to the right from point"""
        return point[0] + 1, point[1]

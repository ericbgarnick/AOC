from typing import Set

from aoc_types import Point
from clay_map import ClayMap
from stream_path import StreamPath, Direction


class Seepage:
    def __init__(self, clay_map: ClayMap):
        self._clay_map = clay_map
        self._paths = [StreamPath(*ClayMap.SOURCE_SPRING)]
        self._water_map = set()  # type: Set[Point]

    def run(self):
        while self._paths:
            self.tick()

    def tick(self):
        """Advance each path if possible"""
        dead_paths = []
        for path in self._paths:
            if not self._in_bounds(path):
                dead_paths.append(path)
            elif self._path_open(path.below):
                path.descend()
                self._water_map.add(path.position)
            elif path.is_falling and path.below not in self._water_map:
                # Falling but clay is below
                self._spawn_streams(*path.position)
            elif self._path_open(path.next_position):
                path.spread()
                self._water_map.add(path.position)
            else:
                # Going sideways but something is in the way
                dead_paths.append(path)
                if path.is_alone:
                    source_x, source_y = path.source
                    self._spawn_streams(source_x, source_y - 1)
        self._paths = [p for p in self._paths if p not in dead_paths]

    def _path_open(self, point: Point) -> bool:
        return point not in (self._clay_map.clay_map | self._water_map)

    def _in_bounds(self, path: StreamPath) -> bool:
        return path.position[1] <= self._clay_map.lowest_point

    def _spawn_streams(self, start_x: int, start_y: int):
        for direction in [Direction.LF, Direction.RT]:
            self._paths.append(StreamPath(start_x, start_y, direction))

from typing import Set, List

from aoc_types import Point
from clay_map import ClayMap
from stream_path import StreamPath, Direction


class Seepage:
    def __init__(self, clay_map: ClayMap):
        self._clay_map = clay_map
        self._paths = [StreamPath(*ClayMap.SOURCE_SPRING)]
        self._water_map = set()  # type: Set[Point]

    @property
    def water_volume(self) -> int:
        return len(self._water_map)

    def run(self):
        num_ticks = 0
        while self._paths:
            print(f"Tick {num_ticks}: {self._paths}")
            self._tick()
            num_ticks += 1

    def _tick(self):
        """Advance each path if possible"""
        dead_paths = []
        new_paths = []
        for path in self._paths:
            if not self._in_bounds(path.position):
                self._kill_stream(path, dead_paths)
            elif self._path_open(path.below):
                path.descend()
                self._record_position(path.position)
            elif path.is_falling and path.below not in self._water_map:
                # Falling but clay is below
                self._kill_stream(path, dead_paths)
                cur_x, cur_y = path.position
                self._spawn_streams(cur_x, cur_y, new_paths)
            elif self._path_open(path.next_position):
                path.spread()
                self._record_position(path.position)
            else:
                # Going sideways but something is in the way
                self._kill_stream(path, dead_paths)
                if path.is_alone:
                    source_x, source_y = path.source
                    self._spawn_streams(source_x, source_y - 1, new_paths)
        self._paths = [p for p in self._paths if p not in dead_paths]
        self._paths.extend(new_paths)

    def _path_open(self, point: Point) -> bool:
        return point not in (self._clay_map.clay_map | self._water_map)

    def _in_bounds(self, position: Point) -> bool:
        return position[1] <= self._clay_map.lowest_point

    def _record_position(self, position: Point):
        down_to_top_clay = position[1] >= self._clay_map.highest_point
        if self._in_bounds(position) and down_to_top_clay:
            self._water_map.add(position)

    @staticmethod
    def _spawn_streams(start_x: int, start_y: int,
                       new_paths: List[StreamPath]):
        left_stream = StreamPath(start_x, start_y, Direction.LF)
        right_stream = StreamPath(start_x, start_y, Direction.RT)

        left_stream.set_sibling(right_stream)
        right_stream.set_sibling(left_stream)

        new_paths.extend([left_stream, right_stream])

    @staticmethod
    def _kill_stream(path: StreamPath, dead_paths: List[StreamPath]):
        if not path.is_alone:
            path.sibling.drop_sibling()
        dead_paths.append(path)

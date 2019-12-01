import time
from typing import Set, List

from aoc_types import Point
from clay_map import ClayMap
from stream_path import StreamPath, Direction


class Seepage:
    def __init__(self, clay_map: ClayMap):
        self._clay_map = clay_map
        self._paths = [StreamPath(*ClayMap.SOURCE_SPRING)]
        self._water_map = set()  # type: Set[Point]
        self._falling_water = set()  # type: Set[Point]
        self._occupied = {p for p in self._clay_map.clay_map}

    @property
    def water_volume(self) -> int:
        return len(self._water_map)

    def run(self):
        num_ticks = 0
        origin = start = time.time()
        while self._paths and num_ticks < 10000:
            # print(f"Tick {num_ticks}: {self._paths}")
            self._tick()
            num_ticks += 1
            if num_ticks % 500 == 0:
                tick_at = time.time()
                print(f"{num_ticks} TICKS IN {tick_at - start} SECONDS")
                start = tick_at
        print(f"TOTAL TIME: {time.time() - origin}")

    def _tick(self):
        """Advance each path if possible"""
        dead_paths = []
        new_paths = []
        for path in self._paths:
            if not self._in_bounds(path.position):
                self._kill_stream(path, dead_paths)
            elif ((path.is_falling and self._path_open(path.below)) or
                  (not path.is_falling and self._path_open(path.below,
                                                           pooling=True))):
                # Falling and not on clay or pooling
                # and not on clay or pooled water
                path.descend()
                self._record_position(path.position, falling=True)
            elif path.is_falling:
                # Fell onto clay
                dead_paths.append(path)
                try:
                    self._falling_water.remove(path.position)
                    self._occupied.add(path.position)
                except KeyError:
                    # Already removed by sibling
                    pass
                self._spawn_streams(path, new_paths)
            elif self._path_open(path.next_position):
                path.spread()
                self._record_position(path.position)
            else:
                # Going sideways but something is in the way
                self._kill_stream(path, dead_paths)
                if path.is_alone:
                    if not self._at_parent_depth(path):
                        # spawn from same stream
                        source_path = path
                    elif path.parent.is_alone:
                        # spawn from parent
                        source_path = path.parent
                    else:
                        # At parent depth but parent has another sibling
                        self._kill_stream(path.parent, dead_paths)
                        continue
                    # Move up 1 from prior source
                    self._spawn_streams(source_path, new_paths, ascend=True)
        self._paths = [p for p in self._paths if p not in dead_paths]
        self._paths.extend(new_paths)

    def _path_open(self, point: Point, pooling: bool = False) -> bool:
        if pooling:
            return point not in self._occupied
        return point not in self._clay_map.clay_map

    def _in_bounds(self, position: Point) -> bool:
        return position[1] <= self._clay_map.lowest_point

    def _record_position(self, position: Point, falling: bool = False):
        reached_top_clay = position[1] >= self._clay_map.highest_point
        if self._in_bounds(position) and reached_top_clay:
            self._water_map.add(position)
            if falling:
                self._falling_water.add(position)
            else:
                self._occupied.add(position)

    def _spawn_streams(self, source_path: StreamPath,
                       new_paths: List[StreamPath],
                       ascend: bool = False):
        if ascend:
            # Spawn above source
            start_x, start_y = source_path.source
            try:
                self._falling_water.remove((start_x, start_y))
                self._occupied.add((start_x, start_y))
            except KeyError:
                # Already removed by sibling
                pass
            start_y -= 1
        else:
            # Spawn at current position
            start_x, start_y = source_path.position

        left_stream = StreamPath(start_x, start_y, Direction.LF)
        right_stream = StreamPath(start_x, start_y, Direction.RT)

        if ascend:
            parent = source_path.parent
        else:
            parent = source_path
        left_stream.add_parent(parent)
        right_stream.add_parent(parent)

        left_stream.set_sibling(right_stream)
        right_stream.set_sibling(left_stream)

        new_paths.extend([left_stream, right_stream])

    @staticmethod
    def _kill_stream(path: StreamPath, dead_paths: List[StreamPath]):
        if not path.is_alone:
            path.sibling.drop_sibling()
        dead_paths.append(path)

    @staticmethod
    def _at_parent_depth(path: StreamPath) -> bool:
        try:
            return path.position[1] == path.parent.source[1]
        except AttributeError:
            # No parent
            return False

    def __str__(self):
        map_grid = self._clay_map.map_grid
        for col, row in self._water_map:
            try:
                map_grid[row][col] = '|'
            except IndexError:
                print(f"Missing water point row: {row}, col: {col}")
        return "\n".join("".join(row) for row in map_grid)

    __repr__ = __str__

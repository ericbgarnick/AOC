import time
from typing import Set

from aoc_types import Point
from clay_map import ClayMap
from stream_path import StreamPath, Direction
from metric import Metric

METRIC_NAMES = ('tick', 'path_open', 'record_position',
                'spawn_streams', 'spread', 'update_paths')


class Seepage:
    def __init__(self, clay_map: ClayMap):
        self.metrics = {n: Metric(n) for n in METRIC_NAMES}
        self._clay_map = clay_map
        self._paths = {StreamPath(*ClayMap.SOURCE_SPRING)}
        self._water_map = set()  # type: Set[Point]
        self._falling_water = set()  # type: Set[Point]
        self._occupied = {p for p in self._clay_map.clay_map}

    @property
    def water_volume(self) -> int:
        return len(self._water_map)

    @property
    def standing_water_volume(self) -> int:
        raise NotImplementedError()

    def run(self):
        num_ticks = 0
        origin = start = time.time()
        while self._paths and num_ticks < 20000:
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
        self.metrics['tick'].start()
        dead_paths = set()
        new_paths = set()
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
                try:
                    self._falling_water.remove(path.position)
                    self._occupied.add(path.position)
                except KeyError:
                    # Already removed by sibling
                    pass
                dead_paths.add(path)
                self._spawn_streams(path, new_paths)
            elif self._path_open(path.next_position):
                self.metrics['spread'].start()
                path.spread()
                self.metrics['spread'].stop()
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
        self.metrics['update_paths'].start()
        if dead_paths:
            self._paths -= dead_paths
        if new_paths:
            self._paths |= new_paths
        self.metrics['update_paths'].stop()
        self.metrics['tick'].stop()

    def _path_open(self, point: Point, pooling: bool = False) -> bool:
        self.metrics['path_open'].start()
        if pooling:
            result = point not in self._occupied
        else:
            result = point not in self._clay_map.clay_map
        self.metrics['path_open'].stop()
        return result

    def _in_bounds(self, position: Point) -> bool:
        return position[1] <= self._clay_map.lowest_point

    def _record_position(self, position: Point, falling: bool = False):
        self.metrics['record_position'].start()
        reached_top_clay = position[1] >= self._clay_map.highest_point
        if self._in_bounds(position) and reached_top_clay:
            self._water_map.add(position)
            if falling:
                self._falling_water.add(position)
            else:
                self._occupied.add(position)
        self.metrics['record_position'].stop()

    def _spawn_streams(self, source_path: StreamPath,
                       new_paths: Set[StreamPath],
                       ascend: bool = False):
        self.metrics['spawn_streams'].start()
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

        new_paths |= {left_stream, right_stream}
        self.metrics['spawn_streams'].stop()

    @staticmethod
    def _kill_stream(path: StreamPath, dead_paths: Set[StreamPath]):
        if not path.is_alone:
            path.sibling.drop_sibling()
        dead_paths.add(path)

    @staticmethod
    def _at_parent_depth(path: StreamPath) -> bool:
        try:
            return path.position[1] == path.parent.source[1]
        except AttributeError:
            # No parent
            return False

    def print_metrics(self):
        print("METRICS:")
        print('\n\n'.join(str(metric) for metric in
                          sorted(self.metrics.values(),
                                 key=lambda m: m.total_time)))

    def __str__(self):
        map_grid = self._clay_map.map_grid
        for col, row in self._water_map:
            try:
                map_grid[row][col] = '|'
            except IndexError:
                print(f"Missing water point row: {row}, col: {col}")
        return "\n".join("".join(row) for row in map_grid)

    __repr__ = __str__

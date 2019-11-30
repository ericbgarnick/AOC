from typing import Set, List, Callable

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
            # print(f"Tick {num_ticks}: {self._paths}")
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
            elif path.is_falling:
                if path.below in self._water_map:
                    # Fell into existing water
                    if self._in_container(path):
                        # More space to fill in container
                        dead_paths.append(path)
                        self._spawn_streams(path, new_paths)
                    else:
                        # existing water is at the top of a container
                        self._kill_stream(path, dead_paths)
                else:
                    # Fell onto clay
                    dead_paths.append(path)
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
                        # print("\nSPAWNING FROM PARENT STREAM\n")
                        # spawn from parent
                        source_path = path.parent
                    else:
                        # At parent depth but parent has another sibling
                        # print("\nKILLING PARENT STREAM\n")
                        self._kill_stream(path.parent, dead_paths)
                        continue
                    # Move up 1 from prior source
                    self._spawn_streams(source_path, new_paths, ascend=True)
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
    def _spawn_streams(source_path: StreamPath, new_paths: List[StreamPath],
                       ascend: bool = False):
        if ascend:
            # Spawn above source
            start_x, start_y = source_path.source
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
            # print("PARENT DEPTH:", path.parent.source[1])
            # print("PATH DEPTH:", path.position[1])
            return path.position[1] == path.parent.source[1]
        except AttributeError:
            # No parent
            return False

    def _in_container(self, path: StreamPath) -> bool:
        cur_x, cur_y = path.position
        left_x = right_x = cur_x

        # check left
        left_x = self._check_sideways(left_x, cur_y, int.__sub__)

        # check right
        right_x = self._check_sideways(right_x, cur_y, int.__add__)

        # Both sides enclosed
        return (not self._path_open((left_x, cur_y)) and
                not self._path_open((right_x, cur_y)))

    def _check_sideways(self, pos_x: int, cur_y: int, op: Callable) -> int:
        while (not self._path_open((pos_x, cur_y + 1))
               and self._path_open((op(pos_x, 1), cur_y))):
            pos_x = op(pos_x, 1)
        return pos_x

    def __str__(self):
        map_grid = self._clay_map.map_grid
        for col, row in self._water_map:
            map_grid[row][col] = '|'
        return "\n".join("".join(row) for row in map_grid)

    __repr__ = __str__

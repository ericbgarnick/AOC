from typing import List, Set, Optional, Dict

from clay_map import Point, ClayMap
from stream_path_old import StreamPath, Direction


class WaterTracer:
    """Recursive solution for Advent of Code Day 17"""
    def __init__(self, clay_locs: List[str]):
        self.clay_map = ClayMap(clay_locs)
        self.path_history = set()
        self.to_explore = [self.clay_map.SOURCE_SPRING]
        self.branch_parents = {}        # type: Dict[Point, Point]

    def trace(self):
        self.run()
        return len(self.path_history)

    def run(self):
        while len(self.to_explore):
            start_pos = self.get_start_pos()
            if start_pos is not None:
                print("STARTING AT", start_pos)
                bottom = self.drop(start_pos)
                print("DROPPED TO", bottom)
                self.path_history |= self.drop_history(start_pos, bottom)
                if bottom[1] == self.clay_map.lowest_point:
                    continue
                left = StreamPath(self.clay_map, Direction.LEFT)
                right = StreamPath(self.clay_map, Direction.RIGHT)
                while not (left.open_end() or
                           right.open_end()):
                    print("FILL LEFT")
                    left.fill_row(bottom)
                    print("L END", left.head_pos)
                    print("FILL RIGHT")
                    right.fill_row(bottom)
                    print("R END", right.head_pos)
                    bottom = StreamPath.up(bottom)
                    print("MOVED UP TO", bottom)
                    if bottom == start_pos:
                        print("BOTTOM == START AT", bottom)
                        try:
                            # Last bottom already went up 1
                            bottom = self.branch_parents[bottom]
                            print("WENT BACK TO", bottom)
                        except KeyError:
                            # parent is in the current path
                            pass
                self.path_history |= left.path_history | right.path_history
                if left.open_end():
                    l_start = StreamPath.left(left.head_pos)
                    self.branch_parents[l_start] = self.branch_parents.get(l_start, bottom)
                    if l_start not in self.to_explore:
                        self.to_explore.append(l_start)
                if right.open_end():
                    r_start = StreamPath.right(right.head_pos)
                    self.branch_parents[r_start] = self.branch_parents.get(r_start, bottom)
                    if r_start not in self.to_explore:
                        self.to_explore.append(r_start)

    def get_start_pos(self) -> Optional[Point]:
        start_pos = self.to_explore.pop(0)
        while start_pos is not None and start_pos in self.path_history:
            print("SKIPPING ALREADY SEEN")
            try:
                start_pos = self.to_explore.pop(0)
            except IndexError:
                start_pos = None
        return start_pos

    def drop(self, cur_pos: Point) -> Point:
        next_pos = StreamPath.down(cur_pos)
        while (not self.clay_map.is_clay(next_pos) and
               next_pos not in self.path_history and
               cur_pos[1] < self.clay_map.lowest_point):
            cur_pos = next_pos
            next_pos = StreamPath.down(cur_pos)
        return cur_pos

    def drop_history(self, start: Point, stop: Point) -> Set[Point]:
        """Return the set of Points between start and stop (inclusive).
        Both start and stop MUST have the same x-value."""
        assert start[0] == stop[0]
        return {(start[0], y) for y in range(start[1], stop[1] + 1)
                if y >= self.clay_map.highest_point}

    @property
    def water_grid(self):
        clay_grid = [[x for x in row] for row in self.clay_map.map_grid]
        for row in range(len(clay_grid)):
            for col in range(len(clay_grid[0])):
                if (col, row) in self.path_history:
                    clay_grid[row][col] = 'X'
        return clay_grid

    def __str__(self):
        return "\n".join("".join(row) for row in self.water_grid)

    __repr__ = __str__

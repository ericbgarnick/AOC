# from typing import List, Set, Optional
#
# from clay_map import Point, ClayMap
# from stream_path import StreamPath, Direction
#
#
# class WaterTracerI:
#     """Recursive solution for Advent of Code Day 17"""
#     def __init__(self, clay_locs: List[str]):
#         self.clay_map = ClayMap(clay_locs)
#         self.path_history = set()
#         self.lowest = 0
#         self.to_explore = {self.clay_map.SOURCE_SPRING}
#
#     def trace(self):
#         self.run()
#         return len(self.path_history)
#
#     def run(self):
#         while len(self.to_explore):
#             start_pos = self.get_start_pos()
#             if start_pos is not None:
#
#                 bottom = self.drop(start_pos)
#
#                 self.lowest = max(self.lowest, bottom[1])
#
#                 self.path_history |= self.drop_history(start_pos, bottom)
#                 if bottom[1] < self.clay_map.lowest_point:
#                     self.step(bottom)
#                 else:
#                     # done with this path
#                     pass
#
#     def get_start_pos(self) -> Optional[Point]:
#         start_pos = self.to_explore.pop()
#         while start_pos is not None and start_pos in self.path_history:
#             try:
#                 start_pos = self.to_explore.pop()
#             except KeyError:
#                 # Nothing more to explore
#                 start_pos = None
#         return start_pos
#
#     def step(self, bottom: Point):
#         left = StreamPath(self.clay_map, Direction.LEFT)
#         right = StreamPath(self.clay_map, Direction.RIGHT)
#         while not (left.open_end() or right.open_end()):
#             left.fill_row(bottom)
#             right.fill_row(bottom)
#             bottom = StreamPath.up(bottom)
#         self.path_history |= left.path_history | right.path_history
#         if left.open_end():
#             self.to_explore.add(StreamPath.left(left.head_pos))
#         if right.open_end():
#             self.to_explore.add(StreamPath.right(right.head_pos))
#
#     def drop(self, cur_pos: Point) -> Point:
#         next_pos = StreamPath.down(cur_pos)
#         while (not self.clay_map.is_clay(next_pos) and
#                cur_pos[1] < self.clay_map.lowest_point):
#             cur_pos = next_pos
#             next_pos = StreamPath.down(cur_pos)
#         return cur_pos
#
#     def drop_history(self, start: Point, stop: Point) -> Set[Point]:
#         """Return the set of Points between start and stop (inclusive).
#         Both start and stop MUST have the same x-value."""
#         assert start[0] == stop[0]
#         return {(start[0], y) for y in range(start[1], stop[1] + 1)
#                 if y >= self.clay_map.highest_point}

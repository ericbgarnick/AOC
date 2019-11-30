import re
import sys
from typing import List, Set

from aoc_types import Point


class ClayMap:

    SOURCE_SPRING = (500, 0)

    X_GROUP_REGEX = re.compile(r'x=(\d+\.{0,2}\d*)')
    Y_GROUP_REGEX = re.compile(r'y=(\d+\.{0,2}\d*)')

    def __init__(self, clay_locs: List[str]):
        self.most_left = float('inf')
        self.most_right = float('-inf')
        self.highest_point = float('inf')
        self.lowest_point = self.SOURCE_SPRING[1]
        self.clay_map = self._build_clay_map(clay_locs)

    def _build_clay_map(self, clay_locs: List[str]) -> Set[Point]:
        """Return a set of tuples of all the x,y
        coordinates where clay is located."""
        clay_map = set()
        for group in clay_locs:
            group = group.strip()
            x_group = self.X_GROUP_REGEX.search(group).group(1)
            y_group = self.Y_GROUP_REGEX.search(group).group(1)
            for x in self._expand_group(x_group):
                for y in self._expand_group(y_group):
                    p = (x, y)
                    self.lowest_point = max(self.lowest_point, y)
                    self.highest_point = min(self.highest_point, y)
                    self.most_left = min(self.most_left, x)
                    self.most_right = max(self.most_right, x)
                    clay_map.add(p)
        return clay_map

    @staticmethod
    def _expand_group(clay_group: str) -> List[int]:
        val_range = clay_group.split('..')
        if len(val_range) == 1:
            return [int(val_range[0])]
        else:
            return list(range(int(val_range[0]), int(val_range[1]) + 1))

    def is_clay(self, coords: Point) -> bool:
        return coords in self.clay_map

    @property
    def map_grid(self):
        output = [[]]
        for ver in range(self.lowest_point + 1):
            for hor in range(int(self.most_right + 1)):
                if (hor, ver) in self.clay_map:
                    output[-1].append('#')
                else:
                    output[-1].append(".")
            output.append([])
        return output

    def __str__(self):
        return "\n".join("".join(row) for row in self.map_grid)

    __repr__ = __str__


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, "r").readlines()]
    cm = ClayMap(data)

    with open("clay_map1.out", "w") as f_out:
        f_out.write(str(cm))

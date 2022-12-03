from collections import deque
from typing import List
from sys import argv


class FloorMap:
    def __init__(self, heights: List[int], width: int):
        self.heights = heights
        self.width = width

    def find_low_points(self) -> List[int]:
        """Return the indexes of low points in self.heights."""
        h_low = self._find_h_low()
        return self._find_v_low(h_low)

    def _find_h_low(self) -> List[int]:
        """Return the indexes of low points checking horizontally."""
        return [
            i for i, h in enumerate(self.heights)
            if h < min(self._h_neighbor_heights(i))
        ]

    def _find_v_low(self, h_low: List[int]) -> List[int]:
        """Return the indexes of low points checking vertically."""
        return [
            i for i in h_low
            if self.heights[i] < min(self._v_neighbor_heights(i))
        ]

    def _h_neighbor_heights(self, i: int) -> List[int]:
        """
        Return the values horizontally on either side
        of the value at index i in self.heights.
        """
        return [self.heights[j] for j in self._h_neighbors(i)]

    def _h_neighbors(self, i: int) -> List[int]:
        """
        Return the indexes horizontally on either side
        of index i in self.heights.
        """
        if i % self.width == 0:
            neighbors = [i + 1]
        elif (i + 1) % self.width == 0:
            neighbors = [i - 1]
        else:
            neighbors = [i - 1, i + 1]
        return neighbors

    def _v_neighbor_heights(self, i: int) -> List[int]:
        """
        Return the values vertically on either side
        of the value at index i in self.heights.
        """
        return [self.heights[j] for j in self._v_neighbors(i)]

    def _v_neighbors(self, i: int) -> List[int]:
        """
        Return the indexes vertically on either side
        of index i in self.heights.
        """
        if i < self.width:
            neighbors = [i + self.width]
        elif i >= len(self.heights) - self.width:
            neighbors = [i - self.width]
        else:
            neighbors = [i - self.width, i + self.width]
        return neighbors

    def calc_basin_size(self, low_point: int) -> int:
        """Return the size of the basin having the given low point."""
        basin = set()
        to_check = deque([low_point])
        while to_check:
            cur_pt = to_check.popleft()
            if cur_pt not in basin:
                basin.add(cur_pt)
                neighbors = self._h_neighbors(cur_pt) + self._v_neighbors(cur_pt)
                for new_pt in neighbors:
                    valid_height = self.heights[cur_pt] <= self.heights[new_pt] < 9
                    if new_pt not in basin and valid_height:
                        to_check.append(new_pt)
        return len(basin)


def parse_input(filename: str) -> FloorMap:
    width = 0
    heights = []
    for line in open(filename, "r"):
        line = line.strip()
        width = len(line)
        heights.extend([int(v) for v in line])
    return FloorMap(heights, width)


def part1(floor_map: FloorMap) -> int:
    """
    Return the sum of all low point risk levels in floor_map.

    A risk level is the low point height + 1.
    """
    low_points = floor_map.find_low_points()
    return sum(floor_map.heights[i] for i in low_points) + len(low_points)


def part2(floor_map: FloorMap) -> int:
    """Return the product of the areas of the 3 largest basins in floor_map."""
    basin_sizes = []
    low_points = floor_map.find_low_points()
    for lp in low_points:
        basin_sizes.append(floor_map.calc_basin_size(lp))
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def main():
    try:
        input_file = argv[1]
        floor_map = parse_input(input_file)
        print("PART 1:", part1(floor_map))
        print("PART 2:", part2(floor_map))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

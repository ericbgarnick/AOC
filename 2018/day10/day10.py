import re
from sys import argv
from typing import List


class Point:
    def __init__(self, x_pos: int, y_pos: int, x_vel: int, y_vel: int):
        self.value = "#"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self._x_vel = x_vel
        self._y_vel = y_vel

    def step(self):
        self.x_pos += self._x_vel
        self.y_pos += self._y_vel

    def __repr__(self):
        return "({}, {})".format(self.x_pos, self.y_pos)

    def __str__(self):
        return self.value


class DisplayGrid:
    def __init__(self, points: List[Point]):
        self._points = points
        self._min_x = None  # Set in _grid_size() call
        self._min_y = None  # Set in _grid_size() call
        self._x_size = self._grid_size('x')
        self._y_size = self._grid_size('y')
        self._normalize_points()
        self._grid = None

    def _grid_size(self, axis: str) -> int:
        def by_x(p: Point) -> int:
            return p.x_pos

        def by_y(p: Point) -> int:
            return p.y_pos

        point_func = {'x': by_x, 'y': by_y}[axis]

        max_point = max(self._points, key=point_func)
        min_point = min(self._points, key=point_func)

        max_val = getattr(max_point, "{}_pos".format(axis))
        min_val = getattr(min_point, "{}_pos".format(axis))

        setattr(self, "_min_{}".format(axis), min_val)

        # Add 1 to account for values at extreme positions
        return max_val - min_val + 1

    def _normalize_points(self):
        for p in self._points:
            p.x_pos -= self._min_x
            p.y_pos -= self._min_y

    @property
    def size(self) -> int:
        return self._x_size * self._y_size

    def move(self):
        for p in self._points:
            p.step()

    def fill(self):
        self._grid = [['.' for _ in range(self._x_size)]
                      for _ in range(self._y_size)]
        for p in self._points:
            # print(repr(p))
            self._grid[p.y_pos][p.x_pos] = p

    def display(self):
        for row in self._grid:
            print(' '.join([str(p) for p in row]))
        print("")


def parse_data(data_rows: List[str]) -> List[Point]:
    return [_parse_row(r) for r in data_rows]


def _parse_row(row: str) -> Point:
    x_pos, y_pos, x_vel, y_vel = [int(val) for val in
                                  re.findall(r'-?\d+', row)]
    return Point(x_pos, y_pos, x_vel, y_vel)


def run_display(points: List[Point], initialization: int, part_num: int):
    _find_smallest(points, initialization)

    if part_num == 1:
        grid = DisplayGrid(points)
        grid.fill()
        grid.display()


def _find_smallest(points: List[Point], initialization: int):
    best_iteration = 0
    min_size = float('inf')
    for i in range(1, initialization + 1):
        for p in points:
            p.step()
        g_temp = DisplayGrid(points)
        size = g_temp.size
        if size < min_size:
            min_size = size
            best_iteration = i

    print("best iteration:", best_iteration)


if __name__ == '__main__':
    data_file = argv[1]
    parsed_data = parse_data([l.strip() for l in
                              open(data_file, 'r').readlines()])
    inits = int(argv[2])
    part = int(argv[3])
    kwargs = {'points': parsed_data, 'initialization': inits,
              'part_num': part}

    run_display(**kwargs)

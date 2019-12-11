import sys
from fractions import Fraction
from typing import Tuple, Set, List


ASTEROID = '#'


def day10_part1(puzzle_data: List[List[str]]) -> int:
    max_x = len(puzzle_data[0])
    max_y = len(puzzle_data)
    best_num_visible = 0
    best_position = None
    asteroid_coords = _find_asteroid_coords(puzzle_data)
    for candidate in asteroid_coords:
        num_visible = 0
        seen_asteroids = {candidate}
        for other in asteroid_coords:
            if other not in seen_asteroids:
                num_visible += 1
                seen_asteroids.add(other)
                seen_asteroids |= _calc_points_in_line(candidate, other,
                                                       max_x, max_y)
        if num_visible > best_num_visible:
            best_num_visible = num_visible
            best_position = candidate
    print("BEST POSITION:", best_position)
    return best_num_visible


def day10_part2(puzzle_data: List[List[str]]):
    pass


def _find_asteroid_coords(asteroid_map: List[List[str]]) -> Set[Tuple[int, int]]:
    asteroid_coords = set()
    for y, row in enumerate(asteroid_map):
        for x, pos in enumerate(row):
            if pos == ASTEROID:
                asteroid_coords.add((x, y))
    return asteroid_coords


def _calc_points_in_line(candidate: Tuple[int, int], other: Tuple[int, int],
                         max_x: int, max_y: int) -> Set[Tuple[int, int]]:
    diff_x = other[0] - candidate[0]
    diff_y = other[1] - candidate[1]

    last_x = max_x if diff_x > 0 else -1
    last_y = max_y if diff_y > 0 else -1

    if diff_x != 0:
        slope = Fraction(diff_y, diff_x)
        diff_y = _diff_from_slope(slope, last_y)
        diff_x = _diff_from_slope(slope, last_x)
    else:
        diff_y = 1 if last_y > -1 else -1
        diff_x = 0

    if diff_x and diff_y:
        # diagonal
        x_vals = [x for x in range(candidate[0], last_x, diff_x)]
        y_vals = [y for y in range(candidate[1], last_y, diff_y)]
        points_in_line = set(zip(x_vals, y_vals))
    elif diff_x:
        # horizontal
        points_in_line = {(x, candidate[1]) for x in
                          range(candidate[0], last_x, diff_x)}
    else:
        # vertical
        points_in_line = {(candidate[0], y) for y in
                          range(candidate[1], last_y, diff_y)}
    return points_in_line


def _diff_from_slope(slope: Fraction, last_coord: int) -> int:
    return (abs(slope.numerator) if last_coord > -1
            else -1 * abs(slope.numerator))


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [list(line.strip()) for line in open(data_file, 'r').readlines()]
    print(f"PART 1:\n{day10_part1(data)}")
    print(f"PART 2:\n{day10_part2(data)}")

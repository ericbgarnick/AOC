import math
import sys
from fractions import Fraction
from functools import partial
from typing import Tuple, Set, List


Point = Tuple[int, int]
ASTEROID = '#'


def day10_part1(puzzle_data: List[List[str]]) -> Tuple[Point, int]:
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
                seen_asteroids |= set(_calc_points_in_line(candidate, other,
                                                           asteroid_coords,
                                                           max_x, max_y))
        if num_visible > best_num_visible:
            best_num_visible = num_visible
            best_position = candidate
    return best_position, best_num_visible


def day10_part2(puzzle_data: List[List[str]], origin: Point) -> int:
    laser_count = 200
    max_x = len(puzzle_data[0])
    max_y = len(puzzle_data)
    asteroid_coords = _find_asteroid_coords(puzzle_data)
    seen_asteroids = {origin}
    radii = []
    for other in asteroid_coords:
        if other not in seen_asteroids:
            seen_asteroids.add(other)
            radius = _calc_points_in_line(origin, other, asteroid_coords,
                                          max_x, max_y)
            radii.append(radius)
            seen_asteroids |= set(radius)
    ordered_radii = _sort_radii(origin, radii)
    lasered = _laser_asteroids(ordered_radii, laser_count)
    last_x, last_y = lasered[-1]
    return last_x * 100 + last_y


def _find_asteroid_coords(asteroid_map: List[List[str]]) -> Set[Point]:
    asteroid_coords = set()
    for y, row in enumerate(asteroid_map):
        for x, pos in enumerate(row):
            if pos == ASTEROID:
                asteroid_coords.add((x, y))
    return asteroid_coords


def _calc_points_in_line(candidate: Point, other: Point, asteroids: Set[Point],
                         max_x: int, max_y: int) -> List[Point]:
    diff_x = other[0] - candidate[0]
    diff_y = other[1] - candidate[1]

    last_x = max_x if diff_x > 0 else -1
    last_y = max_y if diff_y > 0 else -1

    if diff_x != 0:
        slope = Fraction(diff_y, diff_x)
        diff_y = abs(slope.numerator) if last_y > -1 else -1 * abs(slope.numerator)
        diff_x = abs(slope.denominator) if last_x > -1 else -1 * abs(slope.denominator)
    else:
        diff_y = 1 if last_y > -1 else -1
        diff_x = 0

    if diff_x and diff_y:
        # diagonal
        x_vals = [x for x in range(candidate[0], last_x, diff_x)]
        y_vals = [y for y in range(candidate[1], last_y, diff_y)]
        points_in_line = list(zip(x_vals, y_vals))
    elif diff_x:
        # horizontal
        points_in_line = [(x, candidate[1]) for x in
                          range(candidate[0], last_x, diff_x)]
    else:
        # vertical
        points_in_line = [(candidate[0], y) for y in
                          range(candidate[1], last_y, diff_y)]

    # skip candidate coords and those that are not asteroids
    return [p for p in points_in_line[1:] if p in asteroids]


def _sort_radii(origin: Point, radii: List[List[Point]]) -> List[List[Point]]:
    sort_func = partial(_angle_from_origin, origin)
    return sorted(radii, key=sort_func)


def _angle_from_origin(origin: Point, radius: List[Point]) -> float:
    origin_x, origin_y = origin
    point_x, point_y = radius[0]

    # Switch y because this coordinate system is upside-down
    delta_y = origin_y - point_y
    delta_x = point_x - origin_x

    if delta_x < 0 < delta_y:
        delta_y *= -1
        to_add = math.pi
    elif delta_x < 0 and delta_y == 0:
        to_add = math.pi
    elif delta_x < 0 and delta_y < 0:
        delta_y *= -1
        to_add = math.pi
    else:
        to_add = 0
    try:
        angle = math.acos(delta_y / math.sqrt(delta_x ** 2 + delta_y ** 2))
    except ZeroDivisionError:
        angle = 0

    angle += to_add

    return angle


def _laser_asteroids(asteroid_radii: List[List[Point]], num_shots: int) -> List[Point]:
    cur_radius_idx = -1
    shot_asteroids = []
    while len(shot_asteroids) < num_shots and len(asteroid_radii):
        cur_radius_idx = (cur_radius_idx + 1) % len(asteroid_radii)
        try:
            cur_radius = asteroid_radii[cur_radius_idx]
        except IndexError as e:
            raise e
        shot_asteroids.append(cur_radius[0])
        if len(cur_radius) == 1:
            # drop current radius and decrement idx
            asteroid_radii = (asteroid_radii[:cur_radius_idx] +
                              asteroid_radii[cur_radius_idx + 1:])
            cur_radius_idx -= 1
        else:
            cur_radius = cur_radius[1:]
            asteroid_radii[cur_radius_idx] = cur_radius
    return shot_asteroids


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [list(line.strip()) for line in open(data_file, 'r').readlines()]
    position, visible = day10_part1(data)
    print(f"PART 1:\n{visible} visible asteroids from {position}")
    print(f"PART 2:\n{day10_part2(data, position)}")

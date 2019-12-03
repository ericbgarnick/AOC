import sys
from functools import partial
from typing import Set, Tuple, Dict, Callable


def day03_part1(w1: str, w2: str) -> int:
    w1_path = get_path(w1)
    w2_path = get_path(w2)
    overlaps = set(w1_path.keys()) & set(w2_path.keys())
    dist_fn = man_distance
    cp = best_overlap(overlaps, dist_fn)
    return man_distance(cp)


def day03_part2(w1: str, w2: str) -> int:
    w1_path = get_path(w1)
    w2_path = get_path(w2)
    overlaps = set(w1_path.keys()) & set(w2_path.keys())
    dist_fn = partial(path_distance, path1=w1_path, path2=w2_path)
    cp = best_overlap(overlaps, dist_fn)
    return path_distance(cp, w1_path, w2_path)


def get_path(wire: str) -> Dict[Tuple[int, int], int]:
    path = {}
    point = start = (0, 0)
    total_dist = -1  # Will be incremented before adding (0, 0)
    for instr in wire.split(','):
        direction = instr[0]
        dist = int(instr[1:])
        if direction == 'U':
            for y in range(start[1], start[1] + dist + 1):
                total_dist += 1
                point = (start[0], y)
                add_point(path, point, total_dist)
        elif direction == 'D':
            for y in range(start[1], start[1] - dist - 1, -1):
                total_dist += 1
                point = (start[0], y)
                add_point(path, point, total_dist)
        elif direction == 'R':
            for x in range(start[0], start[0] + dist + 1):
                total_dist += 1
                point = (x, start[1])
                add_point(path, point, total_dist)
        else:
            for x in range(start[0], start[0] - dist - 1, -1):
                total_dist += 1
                point = (x, start[1])
                add_point(path, point, total_dist)
        start = point
        total_dist -= 1  # Don't double-increment corners

    del path[(0, 0)]
    return path


def add_point(path: Dict, point: Tuple[int, int], total_dist: int):
    path[point] = min(total_dist, path.get(point, float('inf')))


def best_overlap(overlaps: Set[Tuple[int, int]],
                 dist_fn: Callable) -> Tuple[int, int]:
    closest_dist = float('inf')
    closest_point = (None, None)
    for overlap in overlaps:
        new_dist = dist_fn(point=overlap)
        if new_dist < closest_dist:
            closest_dist = new_dist
            closest_point = overlap
    return closest_point


def man_distance(point: Tuple[int, int]) -> int:
    return sum([abs(c) for c in point])


def path_distance(point: Tuple[int, int], path1: Dict, path2: Dict) -> int:
    return path1[point] + path2[point]


if __name__ == '__main__':
    data_file = sys.argv[1]
    wire1, wire2 = [line.strip() for line in open(data_file).readlines()]
    print(f"PART 1: {day03_part1(wire1, wire2)}")
    print(f"PART 2: {day03_part2(wire1, wire2)}")

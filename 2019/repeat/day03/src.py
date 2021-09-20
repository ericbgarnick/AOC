import argparse
from typing import List, Set, Tuple


def solve(path_1: List[str], path_2: List[str], day_num: int) -> int:
    wire_1_points = follow_wire(path_1)
    wire_2_points = follow_wire(path_2)
    closest_intersection, closest_distance = min(
        intersection_distances(wire_1_points, wire_2_points),
        key=lambda pair: pair[1]
    )
    return closest_distance


def follow_wire(path: List[str]) -> Set[Tuple[int, int]]:
    points = set()
    cur_pos = [0, 0]
    for step in path:
        next_pos = [cur_pos[0], cur_pos[1]]
        direction = step[0]
        distance = int(step[1:])
        if direction in "DL":
            distance *= -1
            step = -1
        else:
            step = 1

        if direction in "UD":
            next_pos[1] += distance
            for y in range(cur_pos[1] + step, next_pos[1] + step, step):
                points.add((cur_pos[0], y))
        elif direction in "LR":
            next_pos[0] += distance
            for x in range(cur_pos[0] + step, next_pos[0] + step, step):
                points.add((x, cur_pos[1]))

        cur_pos = [next_pos[0], next_pos[1]]

    return points


def intersection_distances(
        points_1: Set[Tuple[int, int]], points_2: Set[Tuple[int, int]]
) -> List[Tuple[Tuple[int, int], int]]:
    return [(point, point_dist(point)) for point in points_1 & points_2]


def point_dist(point: Tuple[int, int]) -> int:
    return abs(point[0]) + abs(point[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        path_1 = next(f_in).strip().split(",")
        path_2 = next(f_in).strip().split(",")

    print(f"PART 1: {solve(path_1, path_2, day_num=1)}")
    print(f"PART 2: {solve(path_1, path_2, day_num=2)}")


if __name__ == "__main__":
    main()
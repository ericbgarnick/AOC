import argparse
from typing import List, Set, Tuple, Dict


def solve(path_1: List[str], path_2: List[str], day_num: int) -> int:
    wire_1_points = follow_wire(path_1)
    wire_2_points = follow_wire(path_2)
    if day_num == 1:
        only_points_1 = set(wire_1_points.keys())
        only_points_2 = set(wire_2_points.keys())
        closest_intersection, closest_distance = min(
            intersection_distances(only_points_1, only_points_2),
            key=lambda pair: pair[1]
        )
        return closest_distance
    else:
        closest_intersection, fewest_steps = min(
            intersection_steps(wire_1_points, wire_2_points),
            key=lambda pair: pair[1]
        )
        return fewest_steps


def follow_wire(path: List[str]) -> Dict[Tuple[int, int], int]:
    points = {}
    cur_pos = [0, 0]
    num_steps = 0
    for step in path:
        next_pos = [cur_pos[0], cur_pos[1]]
        direction = step[0]
        distance = int(step[1:])
        if direction in "DL":  # Going "backwards" relative to (0, 0) start point
            distance *= -1
            step = -1
        else:
            step = 1

        if direction in "UD":  # move along Y-axis
            next_pos[1] += distance
            for y in range(cur_pos[1] + step, next_pos[1] + step, step):
                num_steps += 1
                next_pair = (cur_pos[0], y)
                if next_pair not in points:
                    points[next_pair] = num_steps
        elif direction in "LR":  # move along X-axis
            next_pos[0] += distance
            for x in range(cur_pos[0] + step, next_pos[0] + step, step):
                num_steps += 1
                next_pair = (x, cur_pos[1])
                if next_pair not in points:
                    points[next_pair] = num_steps

        cur_pos = [next_pos[0], next_pos[1]]

    return points


def intersection_distances(
        points_1: Set[Tuple[int, int]], points_2: Set[Tuple[int, int]]
) -> List[Tuple[Tuple[int, int], int]]:
    """Return pairs of each point encountered and the Manhattan
    distance to that point from the wires' starting point."""
    return [(point, point_dist(point)) for point in points_1 & points_2]


def intersection_steps(
        wire_1_points: Dict[Tuple[int, int], int],
        wire_2_points: Dict[Tuple[int, int], int]
) -> List[Tuple[Tuple[int, int], int]]:
    """Return pairs of each point encountered and the minimum
    number of steps taken to reach that point for each wire."""
    only_points_1 = set(wire_1_points.keys())
    only_points_2 = set(wire_2_points.keys())
    return [
        (point, point_steps(point, wire_1_points, wire_2_points))
        for point
        in only_points_1 & only_points_2
    ]


def point_dist(point: Tuple[int, int]) -> int:
    return abs(point[0]) + abs(point[1])


def point_steps(
        point: Tuple[int, int],
        points_1: Dict[Tuple[int, int], int],
        points_2: Dict[Tuple[int, int], int]
) -> int:
    return points_1[point] + points_2[point]


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

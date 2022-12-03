import math
import re
from sys import argv
from typing import Tuple


# ((min_x, max_x), (min_y, max_y))
TargetBox = Tuple[Tuple[int, int], Tuple[int, int]]


def parse_input(filename: str) -> TargetBox:
    min_x, max_x, min_y, max_y = re.findall(r"-?\d+", open(filename, "r").read())
    return (int(min_x), int(max_x)), (int(min_y), int(max_y))


def part1(target_box: TargetBox) -> int:
    """
    Return the highest point the projectile can reach and
    still appear in the target box at some point in time.
    """
    x_vel, y_vel = calc_highest_trajectory(target_box)
    return sum_series(y_vel)


def part2(target_box: TargetBox) -> int:
    """
    Return the total number of trajectories for which the projectile
    ever appears in the target box at some point in time.
    """
    total_trajectories = 0
    min_x_vel, max_y_vel = calc_highest_trajectory(target_box)
    max_x_vel = target_box[0][1]
    min_y_vel = target_box[1][0]
    for x_vel in range(min_x_vel, max_x_vel + 1):
        for y_vel in range(min_y_vel, max_y_vel + 1):
            if simulate(x_vel, y_vel, target_box):
                total_trajectories += 1
    return total_trajectories


def calc_highest_trajectory(target_box: TargetBox) -> Tuple[int, int]:
    """
    Sum of 1 to x should fall inside target_box x values.

    If so, projectile will be falling straight down, and must have reached its highest point.
    """
    min_x = quad_solve(-2 * target_box[0][0])
    x_vel = int(math.ceil(min_x))
    # Assumes bottom of target box is always below 0
    y_vel = abs(target_box[1][0]) - 1
    return x_vel, y_vel


def quad_solve(c: int) -> float:
    """Quadratic formula, both 'a' anc 'b' are 1."""
    res_minus = (-1 - (1 - 4 * c) ** 0.5) / 2
    res_plus = (-1 + (1 - 4 * c) ** 0.5) / 2
    return max(res_minus, res_plus)


def sum_series(max_val: int) -> int:
    return max_val * (max_val + 1) // 2


def simulate(x_vel: int, y_vel: int, target_box: TargetBox) -> bool:
    """Return True if given start velocity will hit target_box. Otherwise, return False."""
    pos = (0, 0)
    while pos[0] <= target_box[0][1] and pos[1] >= target_box[1][0]:
        if pos[0] >= target_box[0][0] and pos[1] <= target_box[1][1]:
            return True
        pos = (pos[0] + x_vel, pos[1] + y_vel)
        x_vel = max(0, x_vel - 1)
        y_vel -= 1
    return False


def main():
    try:
        input_file = argv[1]
        target_box = parse_input(input_file)
        print("PART 1:", part1(target_box))
        print("PART 2:", part2(target_box))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

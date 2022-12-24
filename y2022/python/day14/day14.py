"""
Part 1 answer: 757
Part 2 answer: 24943
"""
import re
from enum import Enum
from typing import Tuple

from y2022.python.shared import get_data_file_path

AIR = "."
ROCK = "#"
SAND = "o"

ABS_X_SOURCE = 500


class DescentResult(Enum):
    rest = "rest"
    fall = "fall"
    block = "block"


def main():
    x_min = float("inf")
    x_max = float("-inf")
    y_min = float("inf")
    y_max = float("-inf")
    rocks = []
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        for line in f_in:
            coords = [int(c) for c in re.findall(r"\d+", line)]
            rock = []
            for i in range(0, len(coords), 2):
                x_min = min(x_min, coords[i])
                x_max = max(x_max, coords[i])
                y_min = min(y_min, coords[i + 1])
                y_max = max(y_max, coords[i + 1])
                rock.append((coords[i], coords[i + 1]))
            rocks.append(rock)

    # Construct cave
    depth = y_max + 1
    width = 2 * (depth + 2) - 1
    midpoint = (width - 1) // 2
    x_offset = ABS_X_SOURCE - midpoint
    cave = [[AIR for _ in range(width)] for _ in range(depth)]
    for rock in rocks:
        place_rock(cave, rock, x_offset)
    source = (midpoint, 0)

    # PART 1
    result = None
    counter = 0
    while result != DescentResult.fall:
        result = descend_1(cave, source)
        if result == DescentResult.rest:
            counter += 1
    print("PART 1:", counter)

    # PART 2
    clear_sand(cave)
    cave.append([AIR] * width)
    cave.append([ROCK] * width)

    result = None
    counter = 0
    while result != DescentResult.block:
        result = descend_2(cave, source)
        if result == DescentResult.rest:
            counter += 1
    print("PART 2:", counter)


def place_rock(
    cave: list[list[str]],
    rock: [list[Tuple[int, int]]],
    x_offset: int,
):
    for i in range(len(rock) - 1):
        x1, y1 = rock[i]
        x2, y2 = rock[i + 1]
        x_diff = abs(x2 - x1)
        y_diff = abs(y2 - y1)
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        for x_val in range(x_min, x_min + x_diff + 1):
            for y_val in range(y_min, y_min + y_diff + 1):
                cave[y_val][x_val - x_offset] = ROCK


def clear_sand(cave: list[list[str]]):
    for row in cave:
        for i, material in enumerate(row):
            if material == SAND:
                row[i] = AIR


def descend_1(cave: list[list[str]], cur_pos: Tuple[int, int]) -> DescentResult:
    cur_x, cur_y = cur_pos

    if cur_y == len(cave) - 1:
        return DescentResult.fall
    elif cave[cur_y + 1][cur_x] == AIR:
        return descend_1(cave, (cur_x, cur_y + 1))
    elif cur_x == 0:
        return DescentResult.fall
    elif cave[cur_y + 1][cur_x - 1] == AIR:
        return descend_1(cave, (cur_x - 1, cur_y + 1))
    elif cur_x == len(cave[0]) - 1:
        return DescentResult.fall
    elif cave[cur_y + 1][cur_x + 1] == AIR:
        return descend_1(cave, (cur_x + 1, cur_y + 1))
    else:
        cave[cur_y][cur_x] = SAND
        return DescentResult.rest


def descend_2(cave: list[list[str]], cur_pos: Tuple[int, int]) -> DescentResult:
    cur_x, cur_y = cur_pos

    if cur_y == 0 and cave[cur_y][cur_x] != AIR:
        return DescentResult.block

    if cave[cur_y + 1][cur_x] == AIR:
        return descend_2(cave, (cur_x, cur_y + 1))
    elif cave[cur_y + 1][cur_x - 1] == AIR:
        return descend_2(cave, (cur_x - 1, cur_y + 1))
    elif cave[cur_y + 1][cur_x + 1] == AIR:
        return descend_2(cave, (cur_x + 1, cur_y + 1))
    else:
        cave[cur_y][cur_x] = SAND
        return DescentResult.rest


def print_cave(cave: list[list[str]]):
    print("\n".join(["".join(row) for row in cave]))


if __name__ == "__main__":
    main()

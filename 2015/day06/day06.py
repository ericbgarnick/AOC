import re
from sys import argv
from typing import Dict, Tuple, Callable


def solution(filename: str, part_num: int) -> int:
    grid = {}
    for row in open(filename, "r"):
        update_grid(grid, row.strip(), part_num)
    return sum(grid.values())


def update_grid(grid: Dict, instruction: str, part_num: int):
    min_x, min_y, max_x, max_y, update_function = parse_instruction(
        instruction, part_num
    )
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            update_function(grid, (x, y))


def parse_instruction(
        instruction: str, part_num: int
) -> Tuple[int, int, int, int, Callable]:
    """
    Return coords and update function:
      min-x, min-y, max-x, max-y, func
    """
    top_left, bottom_right = [
        [int(coord) for coord in pair.split(",")]
        for pair in re.findall(r"\d+,\d+", instruction)
    ]
    update_function_name = re.search(r"^t[a-z ]+", instruction).group().strip().replace(" ", "_")
    return (
        top_left[0],
        top_left[1],
        bottom_right[0],
        bottom_right[1],
        globals()[f"{update_function_name}_{part_num}"],
    )


def toggle_1(grid: Dict, pos: Tuple[int, int]):
    try:
        grid[pos] ^= 1
    except KeyError:
        grid[pos] = 1


def turn_off_1(grid: Dict, pos: Tuple[int, int]):
    grid[pos] = 0


def turn_on_1(grid: Dict, pos: Tuple[int, int]):
    grid[pos] = 1


def toggle_2(grid: Dict, pos: Tuple[int, int]):
    try:
        grid[pos] += 2
    except KeyError:
        grid[pos] = 2


def turn_off_2(grid: Dict, pos: Tuple[int, int]):
    try:
        grid[pos] = max(grid[pos] - 1, 0)
    except KeyError:
        grid[pos] = 0


def turn_on_2(grid: Dict, pos: Tuple[int, int]):
    try:
        grid[pos] += 1
    except KeyError:
        grid[pos] = 1


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1", solution(input_file, 1))
        print("PART 2", solution(input_file, 2))
    except IndexError:
        print("Enter path to data file!")


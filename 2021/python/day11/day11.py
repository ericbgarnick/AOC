from sys import argv
from typing import List, Tuple, Set

Grid = List[List[int]]
Point = Tuple[int, int]  # row index, col index

NUM_STEPS_PART_1 = 100


def parse_input(filename: str) -> List[List[int]]:
    return [
        [int(num) for num in line.strip()]
        for line in open(filename, "r")
    ]


def part1(octopus_grid: Grid) -> int:
    """Return the total number of flashes seen in 100 steps."""
    num_flashes = 0
    for _ in range(NUM_STEPS_PART_1):
        num_flashes += count_flashes(octopus_grid)
    return num_flashes


def part2(octopus_grid: Grid) -> int:
    """Return the step number at which all octopuses flash simultaneously."""
    num_octopuses = len(octopus_grid) * len(octopus_grid[0])
    step = 1
    while count_flashes(octopus_grid) < num_octopuses:
        step += 1
    return NUM_STEPS_PART_1 + step


def count_flashes(octopus_grid: Grid) -> int:
    """Return the total number of octopuses that flash in 1 time interval."""
    flash_indexes = time_advance(octopus_grid)
    num_flashes = len(flash_indexes)
    flash_indexes = flash_advance(octopus_grid, flash_indexes)
    num_flashes += len(flash_indexes)
    while flash_indexes:
        flash_indexes = flash_advance(octopus_grid, flash_indexes)
        num_flashes += len(flash_indexes)
    return num_flashes


def time_advance(octopus_grid: Grid) -> Set[Point]:
    """Advance octopus energy levels for a time increment."""
    flash_indexes = set()
    for r, row in enumerate(octopus_grid):
        for c, val in enumerate(row):
            if val == 9:
                flash_indexes.add((r, c))
            row[c] = (val + 1) % 10
    return flash_indexes


def flash_advance(
        octopus_grid: Grid, flash_indexes: Set[Point]
) -> Set[Point]:
    """Advance octopus energy levels for other octopus flashes."""
    grid_size = len(octopus_grid[0])
    new_flash_indexes = set()

    for r, c in flash_indexes:
        for nr, nc in neighbors(r, c, grid_size):
            val = octopus_grid[nr][nc]
            if val == 9:
                new_flash_indexes.add((nr, nc))
                octopus_grid[nr][nc] = 0
            elif val != 0:
                octopus_grid[nr][nc] = (val + 1) % 10

    return new_flash_indexes


def neighbors(row_idx: int, col_idx: int, grid_size: int) -> List[Point]:
    """Return all points adjacent to (row_idx, col_idx), including diagonal."""
    neighbor_indexes = []
    at_top = row_idx == 0
    at_bottom = row_idx + 1 == grid_size
    at_left = col_idx % grid_size == 0
    at_right = (col_idx + 1) % grid_size == 0
    if not at_top:
        neighbor_indexes.append((row_idx - 1, col_idx))
        if not at_left:
            neighbor_indexes.append((row_idx - 1, col_idx - 1))
        if not at_right:
            neighbor_indexes.append((row_idx - 1, col_idx + 1))
    if not at_left:
        neighbor_indexes.append((row_idx, col_idx - 1))
    if not at_right:
        neighbor_indexes.append((row_idx, col_idx + 1))
    if not at_bottom:
        neighbor_indexes.append((row_idx + 1, col_idx))
        if not at_left:
            neighbor_indexes.append((row_idx + 1, col_idx - 1))
        if not at_right:
            neighbor_indexes.append((row_idx + 1, col_idx + 1))
    return neighbor_indexes


def print_grid(octopus_grid: Grid):
    print("\n".join(["".join([str(val) for val in row]) for row in octopus_grid]), end="\n\n")


def main():
    try:
        input_file = argv[1]
        octopus_grid = parse_input(input_file)
        print("PART 1:", part1(octopus_grid))
        print("PART 2:", part2(octopus_grid))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

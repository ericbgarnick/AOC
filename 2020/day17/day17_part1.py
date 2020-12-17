from sys import argv
from typing import Set, Tuple


Cube = Tuple[int, int, int]
PocketDimension = Set[Cube]

NUM_CYCLES = 6


def run(filename: str, num_cycles: int = NUM_CYCLES) -> int:
    pocket_dimension = create_pocket_dimension(filename)
    pocket_dimension = cycle(pocket_dimension, num_cycles)
    return len(pocket_dimension)


def create_pocket_dimension(filename: str) -> PocketDimension:
    pocket_dimension = set()
    y_dim = z_dim = 0
    for line in open(filename, "r"):
        x_dim = 0
        for cube in line.strip():
            if cube == "#":
                pocket_dimension.add((x_dim, y_dim, z_dim))
            x_dim += 1
        y_dim += 1
    return pocket_dimension


def cycle(pocket_dimension: PocketDimension, num_cycles: int) -> PocketDimension:
    """Run the PocketDimension through num_cycles update cycles"""
    while num_cycles:
        pocket_dimension = next_dimension(pocket_dimension)
        num_cycles -= 1
    return pocket_dimension


def next_dimension(pocket_dimension: PocketDimension) -> PocketDimension:
    """Return a new PocketDimension with cubes updated for the next cycle"""
    new_dimension = set()
    checked = set()
    # Update cubes already active
    for cube in pocket_dimension:
        if not cube_change(pocket_dimension, cube):
            new_dimension.add(cube)
        checked.add(cube)
        # Check for neighboring inactive cubes to activate
        for x_diff in (-1, 0, 1):
            for y_diff in (-1, 0, 1):
                for z_diff in (-1, 0, 1):
                    neighbor = (cube[0] + x_diff, cube[1] + y_diff, cube[2] + z_diff)
                    if neighbor not in checked | pocket_dimension:
                        if cube_change(pocket_dimension, neighbor):
                            new_dimension.add(neighbor)
                    checked.add(neighbor)
    return new_dimension


def cube_change(pocket_dimension: PocketDimension, cube: Cube) -> int:
    """Return 1 if position should be switched from inactive to active,
    -1 to switch from active to inactive, 0 to leave as is."""
    already_on = set()
    for x_diff in (-1, 0, 1):
        for y_diff in (-1, 0, 1):
            for z_diff in (-1, 0, 1):
                to_check = (cube[0] + x_diff, cube[1] + y_diff, cube[2] + z_diff)
                if to_check != cube and to_check in pocket_dimension:
                    already_on.add(to_check)
    if cube in pocket_dimension and len(already_on) not in [2, 3]:
        return -1
    elif cube not in pocket_dimension and len(already_on) == 3:
        return 1
    else:
        return 0


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", run(input_file))

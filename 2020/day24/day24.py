from sys import argv
from typing import Set, Tuple


TileType = Tuple[float, int]


def set_floor(filename: str) -> Set[TileType]:
    hex_to_xy = {"e": 1, "w": -1, "n": 1, "s": -1}
    flipped = set()
    for tile_location in open(filename, "r"):
        tile_location = tile_location.strip()
        x, y = 0, 0
        i = 0
        while i < len(tile_location):
            if tile_location[i] in "ns":
                step = tile_location[i:i + 2]
                y_step = hex_to_xy[step[0]]
                x_step = .5 * hex_to_xy[step[1]]
                i += 2
            else:
                step = tile_location[i]
                y_step = 0
                x_step = hex_to_xy[step[0]]
                i += 1
            x += x_step
            y += y_step

        try:
            flipped.remove((x, y))
        except KeyError:
            flipped.add((x, y))

    return flipped


def elapse_days(floor: Set[TileType], duration: int) -> Set[TileType]:
    for _ in range(duration):
        floor = elapse_one_day(floor)
    return floor


def elapse_one_day(floor: Set[TileType]) -> Set[TileType]:
    next_floor = set()
    for tile in floor:
        neighbors = get_neighbors(tile)
        white_neighbors = neighbors - floor
        if len(white_neighbors) in {4, 5}:
            next_floor.add(tile)
        for neighbor in white_neighbors:
            if neighbor not in next_floor:
                noan = get_neighbors(neighbor)  # neighbors of a neighbor
                white_noan = noan - floor
                if len(white_noan) == 4:
                    next_floor.add(neighbor)
    return next_floor


def get_neighbors(tile: TileType) -> Set[TileType]:
    neighbors = set()
    x, y = tile
    # Get diagonal neighbors
    for x_diff in [0.5, -0.5]:
        for y_diff in [1, -1]:
            neighbors.add((x + x_diff, y + y_diff))
    # Get horizontal neighbors
    neighbors.add((x - 1, y))
    neighbors.add((x + 1, y))

    return neighbors


if __name__ == "__main__":
    input_file = argv[1]
    initial_floor = set_floor(input_file)
    print("PART 1:", len(initial_floor))
    print("PART 2:", len(elapse_days(initial_floor, 100)))

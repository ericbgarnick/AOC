"""
Part 1 answer: 3081
Part 2 answer: 1524637681145
"""
from y2022.python.shared import get_data_file_path

# coords from bottom left corner of shape,
# not accounting for padding spaces
SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]
CAVE_WIDTH = 7
VERTICAL_GAP = 3
HORIZONTAL_GAP = 2
AIR = "."
ROCK = "#"
SHAPE_COUNT_GOAL = 2022


def main():
    cave = []
    cur_shape_idx = 0
    cur_shape = SHAPES[cur_shape_idx]
    cur_shape_pos = (HORIZONTAL_GAP, VERTICAL_GAP)
    grow_cave(cave, cur_shape, cur_shape_pos)
    settled_shapes = 0
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        jet_pattern = f_in.read().strip()
    jet_idx = 0
    # Used for Part 2
    iterations = 0
    shape_count_at_iteration = [0]
    while settled_shapes < SHAPE_COUNT_GOAL:
        jet = jet_pattern[jet_idx]
        jet_idx = (jet_idx + 1) % len(jet_pattern)
        if jet_idx == 0:
            iterations += 1
            shape_count_at_iteration.append(settled_shapes)
        new_shape_pos = tick(jet, cave, cur_shape, cur_shape_pos)
        if new_shape_pos[1] == cur_shape_pos[1]:
            settle_shape(cave, cur_shape, new_shape_pos)
            settled_shapes += 1
            cur_shape_idx = (cur_shape_idx + 1) % len(SHAPES)
            cur_shape = SHAPES[cur_shape_idx]
            cur_shape_pos = get_new_shape_pos(cave)
            grow_cave(cave, cur_shape, cur_shape_pos)
        else:
            cur_shape_pos = new_shape_pos
    print("PART 1:", get_new_shape_pos(cave)[1] - HORIZONTAL_GAP - 1)

    # PART 2:

    # for i in range(iterations):
    #     print(f"{shape_count_at_iteration[i + 1]} shapes settled after {i + 1} iterations")

    # First cycle through input data uses 1723 rocks for height 2611
    # Every subsequent cycle through input data uses 1725 rocks adding height 2630

    # (1_000_000_000_000 - 1723) // 1725 = 579710143 (remainder 1602)
    # final height = first iteration height + (579710143 iterations * height per iteration) + height of remaining rocks
    # final height = 2611 + (579710143 * 2630) + 2444
    # final height = 1524637681145
    print("PART 2:", 1524637681145)


def get_new_shape_pos(cave: list[list[str]]) -> tuple[int, int]:
    shape_pos_x = HORIZONTAL_GAP
    shape_pos_y = len(cave) + VERTICAL_GAP
    row_idx = len(cave) - 1
    while all(space == AIR for space in cave[row_idx]):
        shape_pos_y -= 1
        row_idx -= 1
    return shape_pos_x, shape_pos_y


def tick(
    jet: str,
    cave: list[list[str]],
    shape: list[tuple[int, int]],
    shape_pos: tuple[int, int],
) -> tuple[int, int]:
    shape_pos_x, shape_pos_y = shape_pos
    if shape_can_move(jet, cave, shape, (shape_pos_x, shape_pos_y)):
        if jet == ">":
            shape_pos_x += 1
        else:
            shape_pos_x -= 1
    if shape_can_drop(cave, shape, (shape_pos_x, shape_pos_y)):
        shape_pos_y -= 1
    return shape_pos_x, shape_pos_y


def shape_can_move(
    jet: str,
    cave: list[list[str]],
    shape: list[tuple[int, int]],
    shape_pos: tuple[int, int],
) -> bool:
    shape_origin_x, shape_origin_y = shape_pos
    for x, y in shape:
        shape_x, shape_y = shape_origin_x + x, shape_origin_y + y
        if jet == "<":
            if shape_x == 0:
                return False
            if cave[shape_y][shape_x - 1] == ROCK:
                return False
        if jet == ">":
            if shape_x + 1 == CAVE_WIDTH:
                return False
            if cave[shape_y][shape_x + 1] == ROCK:
                return False
    return True


def shape_can_drop(
    cave: list[list[str]],
    shape: list[tuple[int, int]],
    shape_pos: tuple[int, int],
) -> bool:
    shape_origin_x, shape_origin_y = shape_pos
    for x, y in shape:
        shape_x, shape_y = shape_origin_x + x, shape_origin_y + y
        if shape_y == 0:
            return False
        if cave[shape_y - 1][shape_x] == ROCK:
            return False
    return True


def settle_shape(
    cave: list[list[str]],
    shape: list[tuple[int, int]],
    shape_pos: tuple[int, int],
):
    """Add rock to the cave for the given shape at shape_pos."""
    shape_origin_x, shape_origin_y = shape_pos
    for x, y in shape:
        cave[shape_origin_y + y][shape_origin_x + x] = ROCK


def grow_cave(
    cave: list[list[str]],
    shape: list[tuple[int, int]],
    shape_pos: tuple[int, int],
):
    """Add rows of air to the cave until it reaches the top of the new shape."""
    shape_height = max([pt[1] for pt in shape]) + 1
    target_cave_height = shape_pos[1] + shape_height
    height_diff = target_cave_height - len(cave)
    for _ in range(height_diff):
        cave.append([AIR] * CAVE_WIDTH)


def print_cave(cave: list[list[str]]):
    print("\n".join("".join(row) for row in cave[-1::-1]))


if __name__ == "__main__":
    main()

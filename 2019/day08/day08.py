import sys
from typing import List, Tuple

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH * LAYER_HEIGHT

BLACK_VAL = '0'
BLACK_PXL = ' '
WHITE_VAL = '1'
WHITE_PXL = '#'
CLEAR_VAL = '2'
CLEAR_PXL = 'X'
COLORS = {BLACK_VAL: BLACK_PXL, WHITE_VAL: WHITE_PXL, CLEAR_VAL: CLEAR_PXL}


def day08_part1(puzzle_data: str) -> int:
    best_offset = find_min_val_count_offset(puzzle_data, BLACK_VAL)
    return get_check_for_offset(puzzle_data, best_offset, [WHITE_VAL, CLEAR_VAL])


def day08_part2(puzzle_data: str) -> str:
    image = [[CLEAR_PXL for _ in range(LAYER_WIDTH)]
             for _ in range(LAYER_HEIGHT)]
    for i, pixel in enumerate(puzzle_data):
        row, col = coords_for_idx(i)
        if image[row][col] == CLEAR_PXL:
            image[row][col] = COLORS[pixel]
    return create_image(image)


def find_min_val_count_offset(image_data: str, val: str) -> int:
    min_val_count = LAYER_SIZE
    best_offset = None
    for start in range(0, len(image_data) - LAYER_SIZE, LAYER_SIZE):
        val_count = image_data[start:start + LAYER_SIZE].count(val)
        if val_count < min_val_count:
            min_val_count = val_count
            best_offset = start
    return best_offset


def get_check_for_offset(image_data: str, offset: int,
                         to_check: List[str]) -> int:
    total = 1
    for val in to_check:
        total *= image_data[offset:offset + LAYER_SIZE].count(val)
    return total


def coords_for_idx(idx: int) -> Tuple[int, int]:
    relative_idx = idx % LAYER_SIZE
    return relative_idx // LAYER_WIDTH, relative_idx % LAYER_WIDTH


def create_image(image_data: List[List[str]]) -> str:
    return '\n'.join([''.join(row) for row in image_data])


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = open(data_file, 'r').read().strip()
    print(f"PART 1:\n{day08_part1(data)}")
    print(f"PART 2:\n{day08_part2(data)}")

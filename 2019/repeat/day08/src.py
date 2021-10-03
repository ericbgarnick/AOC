import argparse
from typing import List, Dict, Iterable

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

BLACK_DATA = "0"
WHITE_DATA = "1"
CLEAR_DATA = "2"

BLACK_PIXEL = " "
WHITE_PIXEL = "#"
CLEAR_PIXEL = "-"


CONVERSIONS = {
    BLACK_DATA: BLACK_PIXEL,
    WHITE_DATA: WHITE_PIXEL,
    CLEAR_DATA: CLEAR_PIXEL,
}


def solve(data: str, day_num: int) -> int:
    layers = parse_layers(data)
    if day_num == 1:
        fewest_zeroes = find_fewest_zeroes(layers)
        digit_counts = count_digits(layers[fewest_zeroes], WHITE_DATA + CLEAR_DATA)
        product = 1
        for count in digit_counts.values():
            product *= count
        return product
    else:
        final = merge_layers(layers)
        convert_image(final)
        display_image(final)


def parse_layers(raw_data: str) -> List[List[str]]:
    row_start = 0
    layers = []
    while row_start <= len(raw_data) - IMAGE_WIDTH:
        layer = []
        while len(layer) < IMAGE_HEIGHT:
            layer.append(raw_data[row_start:row_start + IMAGE_WIDTH])
            row_start += IMAGE_WIDTH
        layers.append(layer)
    return layers


def find_fewest_zeroes(layers: List[List[str]]) -> int:
    """Return the index of the layer with the fewest zeroes."""
    idx = None
    min_num_zeroes = IMAGE_WIDTH
    for i, layer in enumerate(layers):
        cur_num_zeroes = sum(row.count(BLACK_DATA) for row in layer)
        if cur_num_zeroes < min_num_zeroes:
            min_num_zeroes = cur_num_zeroes
            idx = i
    return idx


def count_digits(layer: List[str], digits: Iterable[str]) -> Dict[str, int]:
    result = {}
    for digit in digits:
        result[digit] = sum(row.count(digit) for row in layer)
    return result


def merge_layers(layers: List[List[str]]) -> List[str]:
    result = [[CLEAR_DATA for _ in range(IMAGE_WIDTH)] for _ in range(IMAGE_HEIGHT)]
    for row_idx in range(IMAGE_HEIGHT):
        for layer in layers:
            for pixel_idx in range(IMAGE_WIDTH):
                if result[row_idx][pixel_idx] == CLEAR_DATA:
                    result[row_idx][pixel_idx] = layer[row_idx][pixel_idx]
    return ["".join(row) for row in result]


def convert_image(layer: List[str]):
    """Converts integer values to pixels in layer."""
    for i in range(IMAGE_HEIGHT):
        row = layer[i]
        row = row.replace(BLACK_DATA, CONVERSIONS[BLACK_DATA])
        row = row.replace(WHITE_DATA, CONVERSIONS[WHITE_DATA])
        row = row.replace(CLEAR_DATA, CONVERSIONS[CLEAR_DATA])
        layer[i] = row


def display_image(pixels: List[str]):
    print("\n".join(pixels))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    data = open(data_file).read().strip()

    print(f"PART 1: {solve(data, day_num=1)}")
    print(f"PART 2:")
    solve(data, day_num=2)


if __name__ == "__main__":
    main()

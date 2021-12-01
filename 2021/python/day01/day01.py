from typing import List
from sys import argv


def parse_input(filename: str) -> List[int]:
    return [int(line.strip()) for line in open(filename, "r")]


def part1(depths: List[int]) -> int:
    """
    Return the number of values in depths that are
    greater than the preceding value.
    """
    count = 0
    i = 1
    while i < len(depths):
        if depths[i] > depths[i - 1]:
            count += 1
        i += 1
    return count


def part2(depths: List[int]) -> int:
    """
    Return the number of 3-value windows in depths that are
    greater than the preceding 3-value window.
    """
    window_1 = sum(depths[:3])
    window_2 = sum(depths[1:4])
    count = 1 if window_2 > window_1 else 0
    end = 4
    while end < len(depths):
        window_1 += depths[end - 1] - depths[end - 4]
        window_2 += depths[end] - depths[end - 3]
        if window_2 > window_1:
            count += 1
        end += 1
    return count


def main():
    try:
        input_file = argv[1]
        depths = parse_input(input_file)
        print("PART 1:", part1(depths))
        print("PART 2:", part2(depths))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

from typing import List
from sys import argv


def parse_input(filename: str) -> List[int]:
    return [int(line.strip()) for line in open(filename, "r")]


def part1(depths: List[int]) -> int:
    count = 0
    i = 1
    while i < len(depths):
        if depths[i] > depths[i - 1]:
            count += 1
        i += 1
    return count


def part2(depths: List[int]) -> int:
    window_1 = sum(depths[:3])
    window_2 = sum(depths[1:4])
    count = 1 if window_2 > window_1 else 0
    windows_end = 4
    while windows_end < len(depths):
        window_2 += depths[windows_end] - depths[windows_end - 3]
        window_1 += depths[windows_end - 1] - depths[windows_end - 4]
        if window_2 > window_1:
            count += 1
        windows_end += 1
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

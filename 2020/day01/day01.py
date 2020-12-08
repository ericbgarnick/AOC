from sys import argv
from typing import List

TARGET_VALUE = 2020


def parse_input(filename: str) -> List[int]:
    return [int(line.strip()) for line in open(filename, "r")]


def sum_for_target(numbers: List[int], target_value: int = TARGET_VALUE) -> int:
    needed = set()
    for entry_num in numbers:
        if entry_num in needed:
            return entry_num
        else:
            needed.add(target_value - entry_num)
    return 0


def part1(numbers: List[int]) -> int:
    result = sum_for_target(numbers)
    return result * (TARGET_VALUE - result)


def part2(numbers: List[int]) -> int:
    for entry_num in numbers:
        temp_target = TARGET_VALUE - entry_num
        result = sum_for_target(numbers, temp_target)
        if result:
            return entry_num * result * (temp_target - result)


if __name__ == "__main__":
    try:
        input_file = argv[1]
        entry_numbers = parse_input(input_file)
        print("PART 1:", part1(entry_numbers))
        print("PART 2:", part2(entry_numbers))
    except IndexError:
        print("Enter path to data file!")

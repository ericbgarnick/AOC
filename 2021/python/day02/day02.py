import re
from typing import List
from sys import argv


def parse_input(filename: str) -> List[str]:
    return [line.strip() for line in open(filename, "r")]


def part1(instructions: List[str]) -> int:
    position = 0
    depth = 0
    for instruction in instructions:
        value = int(re.search(r"\d+", instruction).group())
        if instruction[0] == "u":
            depth -= value
        elif instruction[0] == "d":
            depth += value
        else:
            position += value
    return position * depth


def part2(instructions: List[str]) -> int:
    position = 0
    depth = 0
    aim = 0
    for instruction in instructions:
        value = int(re.search(r"\d+", instruction).group())
        if instruction[0] == "u":
            aim -= value
        elif instruction[0] == "d":
            aim += value
        else:
            position += value
            depth += aim * value
    return position * depth


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

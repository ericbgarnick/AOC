from sys import argv
from typing import List


def parse_input(filename: str) -> List[str]:
    pass


def part1(instructions: List[str]) -> int:
    reactor_core = set()
    for step in instructions:
        action, cubes = step.split(" ", maxsplit=1)
        for cube in parse_cubes(cubes):
            if action == "on":
                reactor_core.add(cube)
            else:
                try:
                    reactor_core.remove(cube)
                except KeyError:
                    pass


def part2(stuff) -> int:
    pass


def main():
    try:
        input_file = argv[1]
    except IndexError:
        print("Enter path to data file!")
        return

    nums = parse_input(input_file)
    print("PART 1:", part1(nums))
    print("PART 2:", part2(nums))


if __name__ == "__main__":
    main()
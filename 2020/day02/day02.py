import re
from sys import argv
from typing import Tuple


def solution(filename: str) -> Tuple[int, int]:
    valid_part_1 = valid_part_2 = 0
    for line in open(filename):
        policy, password = line.strip().split(": ")
        first, second = [int(val) for val in re.findall(r"\d+", policy)]
        required_letter = policy[-1]

        # Part 1
        if first <= password.count(required_letter) <= second:
            valid_part_1 += 1

        # Part 2
        occurrence1 = password[first - 1]
        occurrence2 = password[second - 1]
        if occurrence1 != occurrence2 and required_letter in [occurrence1, occurrence2]:
            valid_part_2 += 1

    return valid_part_1, valid_part_2


if __name__ == "__main__":
    try:
        input_file = argv[1]
        part1, part2 = solution(input_file)
        print("DAY 1:", part1)
        print("DAY 2:", part2)
    except IndexError:
        print("Enter path to data file!")

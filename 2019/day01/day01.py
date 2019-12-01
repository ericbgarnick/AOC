import sys
from typing import List


TOTAL = 0


def day01_part1(puzzle_data: List[int]):
    res = 0
    for mass in puzzle_data:
        res += calc_fuel(mass)
    return res


def day01_part2(puzzle_data: List[int]):
    global TOTAL
    for mass in puzzle_data:
        res = mass
        while res > 0:
            res = calc_fuel(res)
            if res > 0:
                TOTAL += res

    return TOTAL


def calc_fuel(mass: int):
    return int(mass / 3) - 2


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(l.strip()) for l in open(data_file).readlines()]
    print(f"PART 1: {day01_part1(data)}")
    print(f"PART 2: {day01_part2(data)}")

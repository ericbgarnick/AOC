import re
from functools import reduce
from sys import argv
from typing import Tuple


def paper_area(x: int, y: int, z: int) -> int:
    return 2 * (x * y + x * z + y * z) + x * y


def ribbon_length(x: int, y: int, z: int) -> int:
    return (x * y * z) + 2 * (x + y)


def solution(filename: str) -> Tuple[int, int]:
    total_paper = total_ribbon = 0
    with open(filename, "r") as f_in:
        for line in f_in:
            x, y, z = sorted(int(dim) for dim in line.split("x"))
            total_paper += paper_area(x, y, z)
            total_ribbon += ribbon_length(x, y, z)
    return total_paper, total_ribbon


if __name__ == "__main__":
    if __name__ == "__main__":
        try:
            file = argv[1]
            paper, ribbon = solution(file)
            print("PART 1:", paper)
            print("PART 2:", ribbon)
        except IndexError:
            print("Must enter path to input data file!")
from sys import argv
from typing import Tuple


def solution(filename: str) -> Tuple[int, int]:
    total_1 = total_2 = 0
    for line in open(filename, "r"):
        line = line.strip()
        wrapping_quotes = 2
        num_esc_quotes = eval(line).count("\"")
        total_1 += len(line) - len(eval(line))
        total_2 += (
                len(repr(line)) - len(line) +
                wrapping_quotes +
                num_esc_quotes
        )
    return total_1, total_2


if __name__ == "__main__":
    try:
        input_file = argv[1]
        p1, p2 = solution(input_file)
        print("PART 1:", p1)
        print("PART 2:", p2)
    except IndexError:
        print("Enter path to data file!")

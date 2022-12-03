from sys import argv
from typing import Tuple


def parse_line(line_data: str) -> Tuple[str, int]:
    return line_data[0], int(line_data[1:])


if __name__ == '__main__':
    data_file = argv[1]
    total = 0
    seen = set()

    all_lines = [parse_line(line.strip()) for line in
                 open(data_file, 'r').readlines()]

    line_idx = -1
    while total not in seen:
        seen.add(total)
        line_idx = (line_idx + 1) % len(all_lines)

        sign, val = all_lines[line_idx]
        if sign == '+':
            total += val
        else:
            total -= val

    print("Result:", total)


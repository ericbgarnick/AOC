from sys import argv
from typing import Tuple, List


def part1(filename: str) -> int:
    jolts = sorted(int(line.strip()) for line in open(filename, "r"))
    ones, threes = 0, 1  # last diff to device is always three

    last_jolt = 0
    for jolt in jolts:
        diff = jolt - last_jolt
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1
        last_jolt = jolt

    return ones * threes


def part2(filename: str) -> int:
    jolts = {int(line.strip()): 0 for line in open(filename, "r")}
    device = max(jolts.keys()) + 3
    jolts[device] = 0

    # Base case:
    # 1: 0 + 1
    # 2: 0 + 1 + 1, 0 + 2
    # 3: 0 + 1 + 1 + 1, 0 + 1 + 2, 0 + 2 + 1, 0 + 3
    for j in range(3):
        if jolts.get(j + 1) is not None:
            jolts[j + 1] = 2 ** j

    # 1-3 already filled in
    for i in range(4, device + 1):
        if jolts.get(i) is not None:
            total = sum(jolts.get(i - j, 0) for j in range(1, 4))
            jolts[i] = total

    return jolts[device]


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", part1(input_file))
    print("PART 2:", part2(input_file))

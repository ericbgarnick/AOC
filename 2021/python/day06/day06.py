from collections import defaultdict
from typing import List
from sys import argv


NEW_FISH_GESTATION = 9
OLD_FISH_GESTATION = 7


def parse_input(filename: str) -> List[int]:
    return [int(val) for val in open(filename, "r").read().strip().split(",")]


def part1(fish_times: List[int]) -> int:
    """Simulate fish population growth over 80 days."""
    return simulate(fish_times, 80)


def part2(fish_times: List[int]) -> int:
    """Simulate fish population growth over 256 days."""
    return simulate(fish_times, 256)


def simulate(fish_times: List[int], duration) -> int:
    """Return the number of lanternfish in the school after duration days."""
    countdowns = defaultdict(int)
    for f_time in fish_times:
        countdowns[f_time] += 1
    for tick in range(duration):
        new_fish = 0
        reset_fish = 0
        for t in range(NEW_FISH_GESTATION):
            if t == 0:
                reset_fish = new_fish = countdowns[t]
            else:
                countdowns[t - 1] = countdowns[t]
        countdowns[NEW_FISH_GESTATION - 1] = new_fish
        countdowns[OLD_FISH_GESTATION - 1] += reset_fish
    return sum(countdowns.values())


def main():
    try:
        input_file = argv[1]
        fish_times = parse_input(input_file)
        print("PART 1:", part1(fish_times))
        print("PART 2:", part2(fish_times))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

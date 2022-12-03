from collections import defaultdict
from typing import List, Dict
from sys import argv


def parse_input(filename: str) -> List[int]:
    return [int(val) for val in open(filename, "r").read().strip().split(",")]


def part1(positions: List[int]) -> int:
    """
    Return the minimum amount of fuel crabs must spend to align at the same horizontal point.
    Fuel costs are constant over distance.

    O(nlogn) solution - O(nlogn) for sorting + O(n) for finding best position.
    """
    positions.sort()
    last_val = positions[0]
    best_dist = total_dist = sum(val - last_val for val in positions)
    i = 1
    while i < len(positions):
        if positions[i] != last_val:
            cur_val = positions[i]
            total_dist += (i - (len(positions) - i)) * (cur_val - last_val)
            best_dist = min(total_dist, best_dist)
            last_val = cur_val
        i += 1
    return best_dist


def part2(positions: List[int]) -> int:
    """
    Return the minimum amount of fuel crabs must spend to align at the same horizontal point.
    Fuel costs increase linearly over distance.

    O(n^2) solution - O(n) for counting positions + O(n^2) for finding best position.
    """
    pos_counts = defaultdict(int)
    min_pos = float("inf")
    max_pos = -1
    for pos in positions:
        min_pos = min(pos, min_pos)
        max_pos = max(pos, max_pos)
        pos_counts[pos] += 1
    best_fuel_cost = calc_fuel_cost(pos_counts, min_pos)
    for p in range(min_pos + 1, max_pos + 1):
        cur_fuel_cost = calc_fuel_cost(pos_counts, p)
        best_fuel_cost = min(best_fuel_cost, cur_fuel_cost)
    return best_fuel_cost


def calc_fuel_cost(pos_counts: Dict[int, int], cur_pos: int) -> int:
    total_cost = 0
    for pos, count in pos_counts.items():
        dist = abs(pos - cur_pos)
        total_cost += int(dist * (dist + 1) / 2) * count
    return total_cost


def main():
    try:
        input_file = argv[1]
        positions = parse_input(input_file)
        print("PART 1:", part1(positions))
        print("PART 2:", part2(positions))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

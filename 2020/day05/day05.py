from sys import argv
from typing import List

NUM_ROWS = 128
NUM_COLS = 8


def parse_input(filename: str) -> List[str]:
    return [line.strip() for line in open(filename, "r")]


def part1(passes: List[str]) -> int:
    max_seat = 0
    for boarding_pass in passes:
        seat = parse_boarding_pass(boarding_pass.strip())
        max_seat = max(max_seat, seat)
    return max_seat


def part2(passes: List[str], max_seat: int) -> int:
    all_seats = [0 for _ in range(max_seat + 1)]
    min_seat = linear_sort_seats(passes, all_seats)
    for i in range(min_seat, len(all_seats) - 1):
        if all_seats[i] != i:
            return i


def parse_boarding_pass(code: str) -> int:
    row = boarding_pass_helper(code[:7], 1, NUM_ROWS, "F")
    col = boarding_pass_helper(code[7:], 1, NUM_COLS, "L")
    return 8 * row + col


def boarding_pass_helper(code: str, range_min: int, range_max: int, low_symbol: str) -> int:
    if range_max - range_min == 1:
        if code == low_symbol:
            return range_min - 1  # adjust 1 to 0-indexing
        else:
            return range_max - 1

    halfway = range_min + (range_max - range_min) // 2
    if code[0] == low_symbol:
        return boarding_pass_helper(code[1:], range_min, halfway, low_symbol)
    else:
        return boarding_pass_helper(code[1:], halfway, range_max, low_symbol)


def linear_sort_seats(passes: List[str], all_seats: List[int]) -> int:
    """
    Return the lowest seat number found in passes

    SIDE-EFFECT: put each seat number in the corresponding index of all_seats
    e.g. all_seats[n] = n
    """
    min_seat = float("inf")
    for p in passes:
        seat_num = parse_boarding_pass(p)
        min_seat = min(min_seat, seat_num)
        all_seats[seat_num] = seat_num
    return min_seat


if __name__ == "__main__":
    input_file = argv[1]
    boarding_passes = parse_input(input_file)
    max_seat_num = part1(boarding_passes)
    print("DAY 1:", max_seat_num)
    print("DAY 2:", part2(boarding_passes, max_seat_num))

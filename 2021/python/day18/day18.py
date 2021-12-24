from sys import argv
from typing import List

from fish_number import FishNumber, magnitude, sum_fish_numbers


def parse_input(filename: str) -> List[FishNumber]:
    return [eval(line.strip()) for line in open(filename, "r")]


def part1(nums: List[FishNumber]) -> int:
    """
    Return the magnitude of the snailfish number
    obtained by summing all values in nums.
    """
    result = sum_fish_numbers(nums[0], nums[1])
    for num in nums[2:]:
        result = sum_fish_numbers(result, num)
    return magnitude(result)


def part2(nums: List[FishNumber]) -> int:
    """
    Return the highest magnitude possible
    from summing any two snailfish numbers in nums.
    """
    best_magnitude = 0
    for sn1 in nums:
        for sn2 in nums:
            if sn1 != sn2:
                best_magnitude = max(
                    [
                        best_magnitude,
                        magnitude(sum_fish_numbers(sn1, sn2)),
                        magnitude(sum_fish_numbers(sn2, sn1)),
                    ],
                )
    return best_magnitude


def main():
    try:
        input_file = argv[1]
        nums = parse_input(input_file)
        print("PART 1:", part1(nums))
        print("PART 2:", part2(nums))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

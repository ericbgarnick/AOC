import re
from sys import argv


def has_enough_vowels(candidate: str) -> bool:
    return len(re.findall(r"[aeiou]", candidate)) >= 3


def has_a_double_letter(candidate: str) -> bool:
    return re.search(r"([a-z])\1", candidate) is not None


def has_no_bad_strings(candidate: str) -> bool:
    for bad_str in ["ab", "cd", "pq", "xy"]:
        if bad_str in candidate:
            return False
    return True


def has_2_pair(candidate: str) -> bool:
    return re.search(r"([a-z]{2}).*\1", candidate) is not None


def has_a_sandwich(candidate: str) -> bool:
    return re.search(r"([a-z]).\1", candidate) is not None


def is_nice_part_1(candidate: str) -> int:
    return int(
        has_enough_vowels(candidate) and
        has_a_double_letter(candidate) and
        has_no_bad_strings(candidate)
    )


def is_nice_part_2(candidate: str) -> int:
    return int(
        has_2_pair(candidate) and
        has_a_sandwich(candidate)
    )


def count_nice_part_1(filename: str) -> int:
    return sum(is_nice_part_1(line.strip()) for line in open(filename, "r"))


def count_nice_part_2(filename: str) -> int:
    return sum(is_nice_part_2(line.strip()) for line in open(filename, "r"))


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1", count_nice_part_1(input_file))
        print("PART 2", count_nice_part_2(input_file))
    except IndexError:
        print("Enter path to data file!")

import re
from typing import Optional

PUZZLE_INPUT = "vzbxkghb"

zero_idx = ord("0")
a_idx = ord("a")
BAD_VALS_0 = [ord(val) for val in "8be"]  # zero-based "bad values"


def alpha_to_zeroed(alpha: str) -> str:
    return "".join(
        chr(ord(a) - 10) if ord(a) > (a_idx + 9) else
        str(ord(a) - a_idx)
        for a in alpha
    )


def zeroed_to_alpha(zeroed: str) -> str:
    return "".join(
        chr(int(z) + a_idx) if z.isdecimal() else
        chr(ord(z) + 10)
        for z in zeroed
    )


def has_a_straight(candidate: str) -> bool:
    for i, letter in enumerate(candidate[:-2]):
        start_val = int(letter, 26)
        if (int(candidate[i + 1], 26) == start_val + 1 and
                int(candidate[i + 2], 26) == start_val + 2):
            return True
    return False


def has_no_bad_letters(candidate: str) -> bool:
    """Converted i, l, 0 to base 26 (starting with 0-9)"""
    return re.search(r"[8be]", candidate) is None


def has_two_pairs(candidate: str) -> bool:
    return re.search(r"(.)\1.*(.)\2", candidate) is not None


def increment(password: str, char_idx: Optional[int] = None) -> str:
    char_idx = len(password) - 1 if char_idx is None else char_idx
    next_ord = ord(password[char_idx]) + 1
    if next_ord == zero_idx + 10:
        # skip from numerals to alphabetical
        password = password[:char_idx] + "a" + password[char_idx + 1:]
    elif next_ord in BAD_VALS_0:
        # skip bad characters and zero out the rest of the password
        password = password[:char_idx] + chr(next_ord + 1) + "0" * (len(password) - char_idx - 1)
    elif next_ord == a_idx + 16:
        # carry to the next column
        temp_pw = password[:char_idx] + "0" + password[char_idx + 1:]
        password = increment(temp_pw, char_idx - 1)
    else:
        password = password[:char_idx] + chr(next_ord) + password[char_idx + 1:]
    return password


def solution(old_pw: Optional[str] = None):
    old_pw = old_pw or PUZZLE_INPUT
    zeroed = alpha_to_zeroed(old_pw)
    while not (has_a_straight(zeroed) and has_two_pairs(zeroed)):
        zeroed = increment(zeroed)
    return zeroed_to_alpha(zeroed)


if __name__ == "__main__":
    part1_output = solution()
    print("PART 1:", part1_output)
    part2_input = zeroed_to_alpha(increment(alpha_to_zeroed(part1_output)))
    part2_output = solution(part2_input)
    print("PART 2:", part2_output)

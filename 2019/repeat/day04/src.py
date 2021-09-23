from typing import Callable

PASSWORD_MIN = "245318"
PASSWORD_MAX = "765747"


def has_repeated_digit(value: str) -> bool:
    """Return True if any digit occurs more than once in a row.
    Otherwise return False."""
    for i in range(len(value) - 1):
        if value[i] == value[i + 1]:
            return True
    return False


def has_paired_digit(value: str) -> bool:
    """Return True if any digit appears exactly twice in a row.
    Otherwise return False."""
    i = 0
    while i < len(value) - 1:
        j = i + 1
        while j < len(value) and value[i] == value[j]:
            j += 1
        if j - i == 2:
            return True
        i = j

    return False


def solve(day_num: int) -> int:
    if day_num == 1:
        return count_possible_passwords(has_repeated_digit)
    else:
        return count_possible_passwords(has_paired_digit)


def count_possible_passwords(check_fn: Callable) -> int:
    guess = next_non_decreasing_value(PASSWORD_MIN)
    valid_guesses = 0

    while guess <= PASSWORD_MAX:
        if check_fn(guess):
            valid_guesses += 1
        guess = next_non_decreasing_value(str(int(guess) + 1))

    return valid_guesses


def next_non_decreasing_value(value: str) -> str:
    digits = [value[0]]

    for digit in value[1:]:
        if digit >= digits[-1]:
            digits.append(digit)
        else:
            break

    while len(digits) < len(value):
        digits.append(digits[-1])

    return "".join(digits)


def main():
    print(f"PART 1: {solve(day_num=1)}")
    print(f"PART 2: {solve(day_num=2)}")


if __name__ == "__main__":
    main()

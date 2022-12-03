
def day04_part1(passcode_min: str, passcode_max: str) -> int:
    return count_possible_passwords(passcode_min, passcode_max, False)


def day04_part2(passcode_min: str, passcode_max: str) -> int:
    return count_possible_passwords(passcode_min, passcode_max, True)


def count_possible_passwords(passcode_min: str, passcode_max: str,
                             single_pair: bool) -> int:
    num_passwords = 0
    for candidate in range(int(passcode_min), int(passcode_max) + 1):
        cand_str = str(candidate)
        if not_decreasing(cand_str) and has_adjacent_pair(cand_str, single_pair):
            num_passwords += 1
    return num_passwords


def not_decreasing(passcode: str) -> bool:
    return ''.join(sorted(passcode)) == passcode


def has_adjacent_pair(passcode: str, single_pair: bool) -> bool:
    pair_func = one_pair if single_pair else any_pair
    for i in range(len(passcode) - 1):
        if pair_func(passcode, i):
            return True
    return False


def one_pair(passcode: str, i: int) -> bool:
    return any_pair(passcode, i) and passcode.count(passcode[i]) == 2


def any_pair(passcode: str, i: int) -> bool:
    return passcode[i] == passcode[i + 1]


if __name__ == '__main__':
    min_val, max_val = '245318-765747'.split('-')
    print(f"PART 1: {day04_part1(min_val, max_val)}")
    print(f"PART 2: {day04_part2(min_val, max_val)}")

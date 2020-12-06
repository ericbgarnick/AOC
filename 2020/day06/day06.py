from functools import reduce, partial
from sys import argv
from typing import List


def parse_input(filename: str) -> List[List[str]]:
    seating_groups = [[]]
    for line in open(filename, "r"):
        line = line.strip()
        if not line:
            seating_groups.append([])
        else:
            seating_groups[-1].append(line)
    return seating_groups


def sum_group_totals(seating_groups: List[List[str]], part_num: int) -> int:
    """Return the sum of distinct or common answers for each seating group,
    depending on part_num"""
    if part_num == 1:
        count_func = partial(count_answers, distinct=True)
    else:
        count_func = partial(count_answers, distinct=False)
    return reduce(int.__add__, map(count_func, seating_groups))


def count_answers(group: List[str], distinct: bool) -> int:
    """Return the number of letters in group, either distinct or in common"""
    if distinct:
        result = set()
    else:
        result = {chr(i) for i in range(ord("a"), ord("z") + 1)}

    for response in group:
        response = set(list(response))
        if distinct:
            result |= response
        else:
            result &= response
    return len(result)


if __name__ == "__main__":
    input_file = argv[1]
    grouped_responses = parse_input(input_file)
    print("DAY 1:", sum_group_totals(grouped_responses, 1))
    print("DAY 2:", sum_group_totals(grouped_responses, 2))

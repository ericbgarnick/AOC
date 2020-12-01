from sys import argv
from typing import Set

FACTOR_TABLE = {}


def math_stuff(goal: int, part_num: int) -> int:
    if part_num == 1:
        goal /= 10
    else:
        goal /= 11
    house_num = int(goal // 10)
    p_at_h = presents_at_house(house_num, part_num)
    while p_at_h < goal:
        house_num += 1
        p_at_h = presents_at_house(house_num, part_num)

    return house_num


def presents_at_house(house_num: int, part_num: int) -> int:
    limit = -1 if part_num == 1 else 50
    fact_sum = sum(factors(house_num, limit))
    return fact_sum


def factors(num: int, limit: int) -> Set[int]:
    global FACTOR_TABLE
    facts = {num}
    test_factor = num >> 1
    stop = 1 if limit == -1 else num // limit

    while test_factor >= stop:
        if test_factor not in facts:
            div, mod = divmod(num, test_factor)
            if not mod:
                # try:
                #     facts |= FACTOR_TABLE[test_factor]
                # except KeyError:
                facts.add(test_factor)
        test_factor -= 1

    FACTOR_TABLE[num] = facts
    return facts


if __name__ == "__main__":
    presents_goal = int(argv[1])
    # print("PART 1:", math_stuff(presents_goal, 1))
    print("PART 2:", math_stuff(presents_goal, 2))

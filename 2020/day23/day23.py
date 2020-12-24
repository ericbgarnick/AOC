from typing import Dict

# Real start values
CUP_LABELS = [3, 1, 8, 9, 4, 6, 5, 7, 2]
# Sample start values
# CUP_LABELS = [3, 8, 9, 1, 2, 5, 4, 6, 7]


def play(num_moves, max_cup: int = 9, part_num: int = 1) -> int:
    """Linked list of dicts for cups, extra dict for constant-time access to cups"""
    cup_map = set_up_cups(max_cup)

    cur_cup = cup_map[CUP_LABELS[0]]
    for i in range(num_moves):
        move_cups(cur_cup, cup_map, max_cup)
        cur_cup = cur_cup["next"]

    return after_1(cup_map, part_num)


def set_up_cups(max_cup: int) -> Dict:
    prev_cup = {"val": CUP_LABELS[0], "next": {}}
    cup_map = {CUP_LABELS[0]: prev_cup}

    for cup_label in CUP_LABELS[1:]:
        cur_cup = {"val": cup_label, "next": {}}
        cup_map[cup_label] = cur_cup
        prev_cup["next"] = cur_cup
        prev_cup = cur_cup

    for addl_cup_labal in range(len(CUP_LABELS) + 1, max_cup + 1):
        cur_cup = {"val": addl_cup_labal, "next": {}}
        cup_map[addl_cup_labal] = cur_cup
        prev_cup["next"] = cur_cup
        prev_cup = cur_cup

    # Loop last cup to first
    prev_cup["next"] = cup_map[CUP_LABELS[0]]

    return cup_map


def move_cups(cur_cup: Dict, cup_map: Dict, max_cup: int):
    first_pick = cur_cup["next"]
    last_pick = first_pick["next"]["next"]

    destination = cur_cup["val"] - 1 or max_cup
    while destination in [first_pick["val"], first_pick["next"]["val"], last_pick["val"]]:
        destination = destination - 1 or max_cup

    dest_cup = cup_map[destination]
    cur_cup["next"] = last_pick["next"]
    last_pick["next"] = dest_cup["next"]
    dest_cup["next"] = first_pick


def after_1(cup_map: Dict, part_num: int) -> int:
    one_cup = cup_map[1]
    if part_num == 1:
        result = []
        next_cup = one_cup["next"]
        while next_cup["val"] != 1:
            result.append(str(next_cup["val"]))
            next_cup = next_cup["next"]
        return int("".join(result))
    else:
        return one_cup['next']['val'] * one_cup['next']['next']['val']


if __name__ == "__main__":
    print("PART 1:", play(100))
    # Part 2 takes about 15s
    print("PART 2:", play(10_000_000, 1_000_000, 2))

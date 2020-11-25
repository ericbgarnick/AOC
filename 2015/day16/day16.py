from sys import argv
from typing import Dict

PRESENT_ANALYSIS = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def find_aunt_sue(filename: str, part_num: int) -> int:
    for line in open(filename, "r"):
        sue_num_raw, props_raw = line.strip().split(": ", maxsplit=1)
        cur_sue = {}
        for p in props_raw.split(", "):
            p_name, p_val = p.split(": ")
            cur_sue[p_name] = int(p_val)

        if part_num == 1:
            match = match_part_1(cur_sue)
        else:
            match = match_part_2(cur_sue)

        if match:
            return int(sue_num_raw.split()[1])


def match_part_1(cur_sue: Dict[str, int]) -> int:
    for name, val in cur_sue.items():
        if val != PRESENT_ANALYSIS[name]:
            return False
    return True


def match_part_2(cur_sue: Dict[str, int]) -> int:
    for name, val in cur_sue.items():
        if name in {"cats", "trees"}:
            if val <= PRESENT_ANALYSIS[name]:
                return False
        elif name in {"pomeranians", "goldfish"}:
            if val >= PRESENT_ANALYSIS[name]:
                return False
        elif val != PRESENT_ANALYSIS[name]:
            return False
    return True


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1:", find_aunt_sue(input_file, 1))
        print("PART 2:", find_aunt_sue(input_file, 2))
    except IndexError:
        print("Enter path to data file!")
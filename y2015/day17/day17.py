from sys import argv
from typing import List


TARGET_VOLUME = 150


def parse_input(filename: str) -> List[int]:
    return sorted(int(bottle.strip()) for bottle in open(filename, "r"))


def fill_bottles(
        bottles_avail: List[int],
        cur_vol: int = 0,
        bottles_used: int = 0,
        combos: List[int] = None
) -> List[int]:
    combos = combos or []
    if cur_vol == TARGET_VOLUME:
        combos.append(bottles_used)
    elif cur_vol < TARGET_VOLUME and len(bottles_avail):
        for idx, bottle in enumerate(bottles_avail):
            combos += fill_bottles(bottles_avail[idx + 1:], cur_vol + bottle, bottles_used + 1)
    return combos


if __name__ == "__main__":
    try:
        input_file = argv[1]
        result = fill_bottles(parse_input(input_file))
        print("PART 1:", len(result))
        print("PART 2:", result.count(min(result)))
    except IndexError:
        print("Enter path to data file!")

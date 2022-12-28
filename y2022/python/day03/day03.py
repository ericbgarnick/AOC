"""
Part 1 answer: 7581
Part 2 answer: 2525
"""
from itertools import accumulate

from y2022.python.shared import get_data_file_path

ALPHABET_START = ord("a")
ALPHABET_LENGTH = 26
GROUP_SIZE = 3


def main():
    per_rucksack = 0
    per_group = 0
    group = []
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        for line in f_in:
            line = line.strip()
            per_rucksack += get_priority_per_rucksack(line)
            group.append(line)
            if len(group) == GROUP_SIZE:
                per_group += get_common_item_priority(group)
                group = []
    print("PART 1:", per_rucksack)
    print("PART 2:", per_group)


def get_priority_per_rucksack(contents: str) -> int:
    mid_idx = len(contents) // 2
    return get_common_item_priority([contents[:mid_idx], contents[mid_idx:]])


def get_common_item_priority(item_lists: list[str]) -> int:
    common_item = list(
        accumulate([set(contents) for contents in item_lists], set.intersection)
    )[-1].pop()
    priority = ord(common_item.lower()) - ALPHABET_START + 1
    if common_item.lower() != common_item:
        priority += ALPHABET_LENGTH
    return priority


if __name__ == "__main__":
    main()

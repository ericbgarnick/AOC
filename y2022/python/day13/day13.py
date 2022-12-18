from functools import cmp_to_key
from typing import List

from y2022.python.shared import get_data_file_path


DIVIDER_PACKETS = [[[2]], [[6]]]


def main():
    pair_idx = 1
    pair = []
    result = 0
    all_packets = eval(str(DIVIDER_PACKETS))
    with open(get_data_file_path(__file__, sample=False), "r") as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                if compare_packets(*pair) < 0:
                    result += pair_idx
                pair = []
                pair_idx += 1
            else:
                pair.append(eval(line))
                all_packets.append(eval(line))
        if compare_packets(*pair) < 0:
            result += pair_idx
    print("PART 1:", result)
    # Part 2
    sorted_packets = sorted(all_packets, key=cmp_to_key(compare_packets))
    decoder_key = 1
    for i, packet in enumerate(sorted_packets):
        if packet in DIVIDER_PACKETS:
            decoder_key *= (i + 1)
    print("PART 2:", decoder_key)


def compare_packets(packet1: List, packet2: List) -> int:
    """
    Return:
        -1 if packet1 <  packet2
         0 if packet1 == packet2
         1 if packet1 >  packet2
    """
    for i, p1_item in enumerate(packet1):
        try:
            p2_item = packet2[i]
        except IndexError:
            return 1
        if isinstance(p1_item, int) and isinstance(p2_item, int):
            if p1_item < p2_item:
                return -1
            elif p1_item > p2_item:
                return 1
        elif isinstance(p1_item, list) and isinstance(p2_item, list):
            in_order = compare_packets(p1_item, p2_item)
            if in_order != 0:
                return in_order
        else:
            if isinstance(p1_item, int):
                p1_item = [p1_item]
            else:
                p2_item = [p2_item]
            in_order = compare_packets(p1_item, p2_item)
            if in_order != 0:
                return in_order
    if len(packet1) < len(packet2):
        return -1
    return 0



if __name__ == "__main__":
    main()

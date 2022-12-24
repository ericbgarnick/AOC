"""
Part 1 answer: 1766
Part 2 answer: 2383
"""
from collections import Counter

from y2022.python.shared import get_data_file_path

PACKET_MARKER_LENGTH = 4
MESSAGE_MARKER_LENGTH = 14


def main():
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        datastream = f_in.read().strip()
        packet_marker_pos = find_marker(datastream, PACKET_MARKER_LENGTH)
        message_marker_pos = find_marker(datastream, MESSAGE_MARKER_LENGTH)
    print("PART 1:", packet_marker_pos)
    print("PART 2:", message_marker_pos)


def find_marker(datastream: str, marker_length: int) -> int:
    window_start = 0
    window_contents = Counter(datastream[:marker_length])
    while len(window_contents) < marker_length:
        old_item = datastream[window_start]
        new_item = datastream[window_start + marker_length]
        if window_contents[old_item] == 1:
            del window_contents[old_item]
        else:
            window_contents[old_item] -= 1
        window_contents[new_item] += 1
        window_start += 1
    return window_start + marker_length


if __name__ == "__main__":
    main()

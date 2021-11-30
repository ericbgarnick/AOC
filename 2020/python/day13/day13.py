import re
from sys import argv
from typing import Tuple, List


def parse_input(filenae: str) -> Tuple[int, List[int]]:
    time, lines = open(filenae, "r").readlines()
    lines = re.sub(r"x", "0", lines)
    return int(time), [int(line) for line in lines.split(",")]


def find_earliest_bus(time: int, lines: List[int]) -> int:
    shortest_wait = float("inf")
    best_line = None
    for line in filter(lambda x: x > 0, lines):
        prior_bus = time % line
        wait_time = line - prior_bus if prior_bus else 0
        if wait_time < shortest_wait:
            best_line = line
            shortest_wait = wait_time
    return best_line * shortest_wait


def find_first_bus_time(lines: List[int]) -> int:
    """Return the first arrival time of the first bus such that
    each subsequent bus arrives at its required offset"""
    offsets_from_first = get_offsets_from_first_bus(lines)
    first_bus, first_bus_idx = offsets_from_first[0]
    multiple = find_offset_multiple(first_bus, *offsets_from_first[1])
    v1 = first_bus * multiple
    lcm1 = first_bus * offsets_from_first[1][0]
    for next_bus, offset in offsets_from_first[2:]:
        next_mult = find_offset_multiple(first_bus, next_bus, offset)
        v2 = first_bus * next_mult
        lcm2 = first_bus * next_bus
        v1 = find_match(v1, v2, lcm1, lcm2)
        lcm1 *= next_bus
    return v1


def get_offsets_from_first_bus(lines: List[int]) -> List[Tuple[int, int]]:
    """Return the number of each bus line and the offset
     of its required arrival from the first bus"""
    return [(bus_line, idx) for idx, bus_line in enumerate(lines) if bus_line]


def find_offset_multiple(v1: int, v2: int, offset: int) -> int:
    """
    Return the first multiple of v1 (m1) for which
        v2 * m2 - v1 * m1 == offset
    where m2 is some multiple of v2
    """
    o2 = v2  # original value

    reduction = 0
    if offset >= v1:
        reduction, offset = divmod(offset, v1)

    v2 *= v1 // o2 + 1  # Jump v2 past v1 if smaller
    diff = v2 % v1
    while diff != offset:
        v2 += o2
        diff = v2 % v1
    m1 = v2 // v1 - reduction

    return m1


def find_match(start1: int, start2: int, increment1: int, increment2: int) -> int:
    """
    Return the first value:
        value = start1 + n * increment1 = start2 + m * increment2
    """
    total1, total2 = start1, start2

    while total1 != total2:
        greater_val = max(total1, total2)
        if greater_val == total1:
            total1 += increment1
            total2 += increment2 * ((total1 - total2) // increment2)
        else:
            total2 += increment2
            total1 += increment1 * ((total2 - total1) // increment1)
    return total2


if __name__ == "__main__":
    input_file = argv[1]
    departure_time, bus_lines = parse_input(input_file)
    print("PART 1:", find_earliest_bus(departure_time, bus_lines))
    print("PART 2:", find_first_bus_time(bus_lines))

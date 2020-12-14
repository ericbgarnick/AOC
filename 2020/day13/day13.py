import re
from pprint import pprint
from sys import argv
from typing import Tuple, List, Dict


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


def alignment_time(lines: List[int]) -> List[Dict]:
    # Bus line data:
    # {
    #     "curr_v": <int>,
    #     "curr_i": <int>,
    #     "next_v": <int>,
    #     "next_i": <int>,
    #     "offset": <int>,
    #     "curr_offset_multiple": <int>,
    #     "next_offset_multiple": <int>,
    # }
    lines_data = []
    for i, curr_line_num in enumerate(lines):
        if lines[i]:
            cur_data = {"curr_v": curr_line_num, "curr_i": i}
            for j in range(i + 1, len(lines)):
                next_line_num = lines[j]
                if next_line_num != 0:
                    cur_data["next_v"] = next_line_num
                    cur_data["next_i"] = j
                    cur_data["offset"] = j - i
                    m1, m2 = find_offset_multiples(curr_line_num, next_line_num, j - i)
                    cur_data["curr_offset_multiple"] = m1
                    cur_data["next_offset_multiple"] = m2
                    lines_data.append(cur_data)
                    break  # Only consider the next bus line
    return lines_data


def find_offset_multiples(v1: int, v2: int, offset: int) -> Tuple[int, int]:
    """Return the first multiples of v1 and v2 (m1, m2)
    for which v2 *m2 - v1 * m1 == offset"""
    o1, o2 = v1, v2  # original values
    diff = 0
    v1 = v2 = m1 = m2 = 0  # Set values and their multiples to 0
    while diff != offset:
        if diff > o1:
            v1 += o1
            m1 += 1
        else:
            v2 += o2
            m2 += 1
        diff = v2 - v1
    return m1, m2


def find_match(v1: int, v2: int, m1: int, m2: int) -> int:
    t1, t2 = v1, v2
    diff = t2 - t1
    while diff:
        if diff >= m1:
            t1 += m1
        else:
            t2 += m2
        diff = t2 - t1
    return t1


if __name__ == "__main__":
    input_file = argv[1]
    departure_time, bus_lines = parse_input(input_file)
    print("PART 1:", find_earliest_bus(departure_time, bus_lines))
    print(bus_lines)
    a_times = alignment_time(bus_lines)
    pprint(a_times)
    for i in range(len(a_times) - 1):
        curr_t = a_times[i]
        next_t = a_times[i + 1]
        oset = next_t["curr_offset_multiple"] - curr_t["next_offset_multiple"]
        val1, val2 = curr_t["curr_v"], next_t["next_v"]
        if oset > 0:
            mul2, mul1 = find_offset_multiples(val2, val1, oset)
            print(f"{val2} x {mul2} is {oset} greater than {val1} x {mul1}")
        elif oset < 0:
            oset *= -1
            mul1, mul2 = find_offset_multiples(val1, val2, oset)
            print(f"{val2} x {mul2} is {oset} greater than {val1} x {mul1}")
        else:
            pass
    print("PART 2:", pprint(alignment_time(bus_lines)))

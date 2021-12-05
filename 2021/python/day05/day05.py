import collections
import re
from typing import List, Dict, Tuple
from sys import argv


VentLine = collections.namedtuple("VentLine", ["start_x", "start_y", "end_x", "end_y"])
VentMap = Dict[str, int]


def parse_input(filename: str) -> List[VentLine]:
    return [
        VentLine(*[int(val) for val in re.findall(r"\d+", line)])
        for line in open(filename, "r")
    ]


def create_vent_maps(vent_lines: List[VentLine]) -> Tuple[VentMap, VentMap]:
    """
    Return dictionaries of 'x:y' coord keys mapped to count of vents at that location.

    First dictionary maps horizontal and vertical lines, second dictionary maps diagonal lines.
    """
    h_v_vent_map = collections.defaultdict(int)
    d_vent_map = collections.defaultdict(int)
    for vl in vent_lines:
        if vl.start_x == vl.end_x:
            x = vl.start_x
            start_y = min(vl.start_y, vl.end_y)
            end_y = max(vl.start_y, vl.end_y)
            for y in range(start_y, end_y + 1):
                update_vent_map(x, y, h_v_vent_map)
        elif vl.start_y == vl.end_y:
            y = vl.start_y
            start_x = min(vl.start_x, vl.end_x)
            end_x = max(vl.start_x, vl.end_x)
            for x in range(start_x, end_x + 1):
                update_vent_map(x, y, h_v_vent_map)
        else:
            for offset in range(abs(vl.end_x - vl.start_x) + 1):
                x = vl.start_x + offset if vl.end_x >= vl.start_x else vl.start_x - offset
                y = vl.start_y + offset if vl.end_y >= vl.start_y else vl.start_y - offset
                update_vent_map(x, y, d_vent_map)
    return h_v_vent_map, d_vent_map


def update_vent_map(x: int, y: int, vent_map: Dict[str, int]):
    key = f"{x}:{y}"
    vent_map[key] += 1


def part1(h_v_vent_map: VentMap) -> int:
    """
    Return the number of points where at least 2
    horizontal or vertical ys of vents overlap.
    """
    return sum(1 for val in h_v_vent_map.values() if val > 1)


def part2(h_v_vent_map: VentMap, d_vent_map: VentMap) -> int:
    """
    Return the number of points where at least 2
    horizontal, vertical or diagonal ys of vents overlap.
    """
    count = 0
    for k in set(h_v_vent_map.keys()) | set(d_vent_map.keys()):
        if h_v_vent_map[k] + d_vent_map[k] > 1:
            count += 1
    return count


def main():
    try:
        input_file = argv[1]
        vent_lines = parse_input(input_file)
        h_v_vent_map, d_vent_map = create_vent_maps(vent_lines)
        print("PART 1:", part1(h_v_vent_map))
        print("PART 2:", part2(h_v_vent_map, d_vent_map))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

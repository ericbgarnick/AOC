from sys import argv
from typing import Dict, Any, List


def parse_input(filename: str) -> Dict[str, Any]:
    """Return a tuple of (tree map, map width, map height)"""
    tree_map = []
    map_width = map_height = 0
    for line in open(filename, "r"):
        line = line.strip()
        map_width = len(line)
        tree_map += list(line)
        map_height += 1
    return {"tree_map": tree_map, "map_width": map_width, "map_height": map_height}


def alternate_paths(tree_map: List[str], map_width: int, map_height: int) -> int:
    total = 1
    for h, v in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        total *= count_trees(tree_map, map_width, map_height, h, v)
    return total


def count_trees(
        tree_map: List[str],
        map_width: int,
        map_height: int,
        h_dist: int = 3,
        v_dist: int = 1,
) -> int:
    cur_loc = trees_hit = 0
    while cur_loc < map_width * map_height:
        if map_width - cur_loc % map_width <= h_dist:
            # within h_dist of right edge - don't skip to next row
            increase = (v_dist - 1) * map_width + h_dist
        else:
            increase = v_dist * map_width + h_dist
        cur_loc += increase
        if cur_loc < len(tree_map) and tree_map[cur_loc] == "#":
            trees_hit += 1
    return trees_hit


if __name__ == "__main__":
    try:
        input_file = argv[1]
        map_info = parse_input(input_file)
        print("PART 1:", count_trees(**map_info))
        print("PART 2:", alternate_paths(**map_info))
    except IndexError:
        print("Enter path to data file!")

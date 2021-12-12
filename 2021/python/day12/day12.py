from sys import argv
from typing import Dict, Set


CaveMap = Dict[str, Set[str]]


def parse_input(filename: str) -> CaveMap:
    cave_map = {}
    for link in open(filename, "r"):
        cave1, cave2 = link.strip().split("-")
        add_caves(cave_map, cave1, cave2)
        add_caves(cave_map, cave2, cave1)
    return cave_map


def add_caves(cave_map: CaveMap, cave1: str, cave2: str):
    try:
        cave_map[cave1].add(cave2)
    except KeyError:
        cave_map[cave1] = {cave2}


def part1(cave_map: CaveMap) -> int:
    """
    Return the total number of paths possible through cave_map visiting
    lower-cased caves once and upper-cased caves unlimited times.
    """
    return visit_with_duplicate(cave_map, "start", set(), "")


def part2(cave_map: CaveMap) -> int:
    """
    Return the total number of paths possible through cave_map if all
    upper-cased caves and 1 lower-cased cave can be visited unlimited times,
    and the remaining lower-cased caves can be visited only once.
    """
    total_count = base_count = visit_with_duplicate(cave_map, "start", set(), "")
    for cave in cave_map.keys():
        if cave.islower():
            dup_count = visit_with_duplicate(cave_map, "start", {"start"}, cave)
            total_count += dup_count - base_count
    return total_count


def visit_with_duplicate(
        cave_map: CaveMap,
        cur_cave: str,
        visited: Set[str],
        duplicate: str,
) -> int:
    if cur_cave == "end":
        return 1
    if cur_cave.islower():
        if duplicate and cur_cave == duplicate:
            duplicate = ""
        else:
            visited.add(cur_cave)
    count = sum(
        visit_with_duplicate(cave_map, next_cave, visited, duplicate)
        for next_cave
        in cave_map[cur_cave] - visited
    )
    try:
        visited.remove(cur_cave)
    except KeyError:
        pass
    return count


def main():
    try:
        input_file = argv[1]
        cave_map = parse_input(input_file)
        print("PART 1:", part1(cave_map))
        print("PART 2:", part2(cave_map))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

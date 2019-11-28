from sys import argv
from typing import List, Tuple


def find_big_area(coord_list: List[str], part_num: int):
    coords = [parse_tuple(pair) for pair in coord_list]
    max_x = max(coords, key=lambda pair: pair[0])[0] + 1
    max_y = max(coords, key=lambda pair: pair[1])[1] + 1
    if part_num == 1:
        print("Part 1")
        create_voronoi(coords, max_x, max_y)
    elif part_num == 2:
        print("Part 2")
        find_within_dist(coords, max_x, max_y, 10000)


def parse_tuple(unparsed: str) -> Tuple:
    return tuple(int(val.strip()) for val in unparsed.split(','))


def create_voronoi(coords: List[Tuple[int, int]],
                   max_x: int, max_y: int) -> List[List[int]]:
    grid = [[-1 for _ in range(max_x)] for _ in range(max_y)]
    counts = [0 for _ in range(len(coords))]
    for x in range(max_x):
        for y in range(max_y):
            dists = []  # [(<dist>, <idx>), ...]
            for idx, pair in enumerate(coords):
                dist = find_dist((x, y), pair)
                dists.append((dist, idx))
            dists.sort()
            if dists[0][0] == dists[1][0]:
                pass
            else:
                idx = dists[0][1]
                grid[y][x] = idx
                counts[idx] += 1
    cleaned = clean_counts(counts, grid)
    max_count = max(cleaned)
    print("Max {} has total {}".format(cleaned.index(max_count), max_count))
    return grid


def find_within_dist(coords: List[Tuple[int, int]],
                     max_x: int, max_y: int, max_dist: int):
    grid = [[-1 for _ in range(max_x)] for _ in range(max_y)]
    kept = 0
    for x in range(max_x):
        for y in range(max_y):
            dists = []
            for idx, pair in enumerate(coords):
                dists.append(find_dist((x, y), pair))
            if sum(dists) < max_dist:
                kept += 1
    print("{} points within {} of vertices".format(kept, max_dist))
    return grid


def find_dist(pt_1: Tuple[int, int], pt_2: Tuple[int, int]) -> int:
    return abs(pt_1[0] - pt_2[0]) + abs(pt_1[1] - pt_2[1])


def clean_counts(counts: List[int], grid: List[List[int]]) -> List[int]:
    for top_spot in grid[0]:
        if top_spot != -1:
            counts[top_spot] = -1
    for bot_spot in grid[-1]:
        if bot_spot != -1:
            counts[bot_spot] = -1
    for row in grid:
        first = row[0]
        if first != -1:
            counts[first] = -1
        last = row[-1]
        if last != -1:
            counts[last] = -1
    return counts


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [l.strip() for l in open(data_file, 'r').readlines()]
    part = int(argv[2])

    find_big_area(data_lines, part)

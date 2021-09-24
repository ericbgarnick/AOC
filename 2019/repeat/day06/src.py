import argparse
from collections import deque
from typing import List, Dict


def solve(data: List[str], day_num: int) -> int:
    graph = create_graph([pair.split(")") for pair in data])
    if day_num == 1:
        return bfs_node_distance(graph, "COM")
    elif day_num == 2:
        return bfs_node_distance(graph, "YOU", "SAN")


def create_graph(orbits: List[List[str]]) -> Dict[str, Dict]:
    graph = {}

    for inner, outer in orbits:
        add_to_graph(graph, inner, outer)
        add_to_graph(graph, outer, inner)

    return graph


def add_to_graph(graph: Dict[str, Dict], key: str, val: str):
    try:
        graph[key]["orbits"].add(val)
    except KeyError:
        graph[key] = {"orbits": {val}, "distance": None}


def bfs_node_distance(graph: Dict[str, Dict], start: str, end: str = None) -> int:
    total_distance = 0
    graph[start]["distance"] = 0
    to_explore = deque([start])

    while to_explore:
        node = graph[to_explore.popleft()]
        distance = node["distance"]
        total_distance += distance
        for orbit_name in node["orbits"]:
            if end and orbit_name == end:
                return distance - 1  # Distance from start's orbited planet
            orbit = graph[orbit_name]
            if orbit["distance"] is None:
                orbit["distance"] = distance + 1
                to_explore.append(orbit_name)

    return total_distance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [line.strip() for line in f_in]

    print(f"PART 1: {solve(data, day_num=1)}")
    print(f"PART 2: {solve(data, day_num=2)}")


if __name__ == "__main__":
    main()

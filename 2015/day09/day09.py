from sys import argv
from typing import Dict, Tuple, Callable

TravelMap = Dict[str, Dict[str, int]]


def create_map(filename: str) -> TravelMap:
    """Return each location mapped to each other location
    and the distance between each such pair"""
    travel_map = {}
    for line in open(filename, "r"):
        loc1, loc2, dist = parse_line(line)
        add_locs(travel_map, loc1, loc2, dist)
        add_locs(travel_map, loc2, loc1, dist)
    return travel_map


def parse_line(line: str) -> Tuple[str, str, int]:
    locations, dist = line.strip().split(" = ")
    loc1, loc2 = locations.strip().split(" to ")
    return loc1, loc2, int(dist)


def add_locs(travel_map: TravelMap, loc1: str, loc2: str, dist: int):
    try:
        travel_map[loc1][loc2] = dist
    except KeyError:
        travel_map[loc1] = {loc2: dist}


def navigate(locations: TravelMap, comp_func: Callable) -> Tuple[int, Dict[str, int]]:
    """Return the distance traveled and best path
    given each possible starting location."""
    best_dist = comp_func(float("inf"), float("-inf")) * -1
    best_path = {}
    for loc in locations:
        new_dist, new_path = nav_helper(locations, loc, comp_func)
        if new_dist == comp_func(new_dist, best_dist):
            best_dist = new_dist
            best_path = new_path
    return best_dist, best_path


def nav_helper(
        locations: TravelMap, start_loc: str, comp_func: Callable
) -> Tuple[int, Dict[str, int]]:
    """Return the distance traveled and best path for the given start_loc"""
    cur_loc = start_loc
    path = {cur_loc: 0}  # location: visit order
    dist = 0
    while len(path) < len(locations):
        destinations = locations[cur_loc]
        available_dest_names = set(destinations.keys()) - set(path.keys())
        next_loc = comp_func(available_dest_names, key=lambda dest: destinations[dest])
        dist += destinations[next_loc]
        path[next_loc] = path[cur_loc] + 1
        cur_loc = next_loc
    return dist, path


def print_path(path: Dict[str, int]):
    print("->".join(sorted(path.keys(), key=lambda point: path[point])))


if __name__ == "__main__":
    locs = {
        "London": {"Dublin": 464, "Belfast": 518},
        "Dublin": {"London": 464, "Belfast": 141},
        "Belfast": {"Dublin": 141, "London": 518},
    }

    try:
        input_file = argv[1]
        print("PART 1:\n-------")
        shortest_distance, shortest_path = navigate(create_map(input_file), min)
        print_path(shortest_path)
        print(f"Total Distance: {shortest_distance}\n")

        print("PART 2:\n-------")
        longest_distance, longest_path = navigate(create_map(input_file), max)
        print_path(longest_path)
        print(f"Total Distance: {longest_distance}\n")
    except IndexError:
        print("Enter path to data file!")

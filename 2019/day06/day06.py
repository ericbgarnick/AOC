import sys
from queue import Queue
from typing import Dict, List


def day06_part1(puzzle_data: List[str]):
    orbits = create_orbits(puzzle_data)
    return calc_distances(orbits, 'COM', 0)


def day06_part2(puzzle_data: List[str]):
    origin = "YOU"
    destination = "SAN"
    orbits = create_orbits(puzzle_data)
    return dist_between_pts(orbits, origin, destination)


def create_orbits(orbit_data: List[str]) -> Dict:
    mapping = {}
    for orbit in orbit_data:
        inner, outer = orbit.split(')')
        add_to_mapping(mapping, inner, 'outer', outer)
        add_to_mapping(mapping, outer, 'inner', inner)
    return mapping


def add_to_mapping(mapping: Dict[str, Dict[str, List[str]]],
                   top_key: str, nested_key: str, value: str):
    try:
        mapping[top_key][nested_key].append(value)
    except KeyError:
        other_key = 'inner' if nested_key != 'inner' else 'outer'
        mapping[top_key] = {nested_key: [value], other_key: []}


def calc_distances(mapping: Dict, object_id: str, distance: int) -> int:
    """DFS to find all distances of all objects in mapping."""
    total_distance = distance
    for outer in mapping[object_id].get('outer', []):
        total_distance += calc_distances(mapping, outer, distance + 1)
    return total_distance


def dist_between_pts(mapping: Dict[str, Dict[str, List[str]]],
                     origin: str, destination: str) -> int:
    """BFS to find shortest distance between origin and destination."""
    origin_orbit = mapping[origin]['inner'][0]
    d_from_origin = {origin_orbit: 0}
    to_explore = Queue()
    to_explore.put(origin_orbit)
    while not to_explore.empty():
        orb = to_explore.get()
        d = d_from_origin[orb]
        for neighbor in mapping[orb]['inner'] + mapping[orb]['outer']:
            if neighbor == destination:
                return d
            elif neighbor not in d_from_origin:
                to_explore.put(neighbor)
                d_from_origin[neighbor] = d + 1


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, 'r').readlines()]
    print(f"PART 1: {day06_part1(data)}")
    print(f"PART 2: {day06_part2(data)}")

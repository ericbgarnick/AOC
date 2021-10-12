import argparse
import math
from collections import namedtuple
from typing import List, Tuple, Set, Dict

Asteroid = namedtuple("Asteroid", ["point", "angle", "distance"])
NUM_SHOTS = 200


def solve(data: List[str], day_num: int) -> int:
    asteroid_locs = parse_map(data)
    data_for_station = find_station(asteroid_locs)
    if day_num == 1:
        return data_for_station["most_seen_from_station"]
    else:
        asteroid_map = create_asteroid_map(data_for_station["asteroids_from_station"])
        last_shot = shoot_asteroids(asteroid_map, NUM_SHOTS)
        return last_shot.point[1] * 100 + last_shot.point[0]


def find_station(asteroid_locs: Set[Tuple[int, int]]) -> Dict:
    asteroids_from_station = []
    most_seen_from_station = 0
    for ast in asteroid_locs:
        asteroid_data = [
            Asteroid(other, calc_angle(ast, other), calc_dist(ast, other))
            for other in asteroid_locs - {ast}
        ]
        num_visible = len({a.angle for a in asteroid_data})
        if num_visible > most_seen_from_station:
            most_seen_from_station = num_visible
            asteroids_from_station = asteroid_data
    return {
        "asteroids_from_station": asteroids_from_station,
        "most_seen_from_station": most_seen_from_station,
    }


def parse_map(asteroid_map: List[str]) -> Set[Tuple[int, int]]:
    result = set()
    for r, row in enumerate(asteroid_map):
        for c, point in enumerate(row):
            if point == "#":
                result.add((r, c))
    return result


def calc_angle(source: Tuple[int, int], point: Tuple[int, int]) -> float:
    """Return the angle in radians of point from a vertical line through source."""
    if source[0] == point[0]:
        if source[1] < point[1]:
            angle = 3 * math.pi / 2
        else:
            angle = math.pi / 2
    elif source[1] == point[1]:
        if source[0] < point[0]:
            angle = math.pi
        else:
            angle = 2 * math.pi
    else:
        if (source[0] > point[0]) and (source[1] > point[1]):
            angle = math.atan(abs(source[1] - point[1]) / abs(source[0] - point[0]))
        elif (source[0] < point[0]) and (source[1] > point[1]):
            angle = math.atan(abs(source[0] - point[0]) / abs(source[1] - point[1])) + math.pi / 2
        elif (source[0] < point[0]) and (source[1] < point[1]):
            angle = math.atan(abs(source[1] - point[1]) / abs(source[0] - point[0])) + math.pi
        else:
            angle = math.atan(abs(source[0] - point[0]) / abs(source[1] - point[1])) + 3 * math.pi / 2
    return angle


def calc_dist(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def create_asteroid_map(asteroids: List[Asteroid]) -> Dict[float, List[Asteroid]]:
    asteroids.sort(key=lambda a: a.angle)
    return create_angle_map(asteroids)


def create_angle_map(asteroids: List[Asteroid]) -> Dict[float, List[Asteroid]]:
    """Return a dictionary of angles mapped to lists of Asteroids, sorted by distances."""
    asteroid_map = {a.angle: [] for a in asteroids}
    for a in asteroids:
        asteroid_map[a.angle].append(a)
    for angle, alist in asteroid_map.items():
        asteroid_map[angle] = sorted(alist, key=lambda a: a.distance)
    return asteroid_map


def shoot_asteroids(asteroid_map: Dict[float, List[Asteroid]], num_shots: int) -> Asteroid:
    """Return the Asteroid shot at the num_shots fire."""
    angles = sorted(asteroid_map.keys(), reverse=True)
    num_angles = len(angles)
    counter = angle_idx = 0
    tgt = None
    while counter < num_shots:
        angle = angles[angle_idx % num_angles]
        possible_tgts = asteroid_map[angle]
        while not possible_tgts:
            angle_idx += 1
            angle = angles[angle_idx % num_angles]
            possible_tgts = asteroid_map[angle]
        tgt = asteroid_map[angle][0]
        asteroid_map[angle] = asteroid_map[angle][1:]
        counter += 1
        angle_idx += 1
    return tgt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    data = [line.strip() for line in open(data_file, "r")]

    print(f"PART 1: {solve(data, day_num=1)}")
    print(f"PART 2: {solve(data, day_num=2)}")


if __name__ == "__main__":
    main()

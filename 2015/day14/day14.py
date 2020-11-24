import re
from sys import argv
from typing import Dict, Tuple

RACE_DURATION = 2503


def race(filename: str, part_num: int) -> Dict:
    """Return distance winner travels"""
    reindeer_data = parse_lines(filename)
    if part_num == 1:
        for name, reindeer in reindeer_data.items():
            calc_race_distance(reindeer)
        return max(reindeer_data.values(), key=lambda rd: rd["total_dist"])
    else:
        calc_lead_time(reindeer_data)
        return max(reindeer_data.values(), key=lambda rd: rd["lead_time"])


def parse_lines(filename: str) -> Dict[str, Dict[str, int]]:
    reindeer_data = {}
    for line in open(filename, "r"):
        name, speed, flight_time, rest_time = parse_line(line)
        reindeer_data[name] = {
            "speed": speed,
            "flight_time": flight_time,
            "rest_time": rest_time,
            "total_time": flight_time + rest_time,
            "total_dist": 0,
            "cur_dist": 0,
            "flight_left": flight_time,
            "rest_left": 0,
            "lead_time": 0,
        }
    return reindeer_data


def parse_line(line: str) -> Tuple[str, int, int, int]:
    name, stats = line.strip().split(maxsplit=1)
    speed, flight_time, rest_time = [int(num) for num in re.findall(r"\d+", stats)]
    return name, speed, flight_time, rest_time


def calc_race_distance(reindeer: Dict[str, int]):
    """Return the total distance this reindeer can travel in RACE_DURATION seconds"""
    multiple, remainder = divmod(RACE_DURATION, reindeer["total_time"])
    unit_dist = reindeer["speed"] * reindeer["flight_time"]
    base_dist = unit_dist * multiple
    partial_dist = (unit_dist if remainder >= reindeer["flight_time"] else
                    reindeer["speed"] * remainder)
    reindeer["total_dist"] = base_dist + partial_dist


def calc_lead_time(all_reindeer: Dict[str, Dict]):
    """Update all_reindeer['lead_time'] with the number of seconds they spend
    in the lead over the course of a race of RACE_DURATION seconds"""
    for sec in range(RACE_DURATION):
        for reindeer in all_reindeer.values():
            if reindeer["flight_left"]:
                update_action(reindeer, "flight")
                reindeer["cur_dist"] += reindeer["speed"]
            else:
                update_action(reindeer, "rest")
        cur_lead = max(all_reindeer.values(), key=lambda rd: rd["cur_dist"])
        for reindeer in all_reindeer.values():
            if reindeer["cur_dist"] == cur_lead["cur_dist"]:
                reindeer["lead_time"] += 1


def update_action(reindeer: Dict, cur_action: str):
    other_action = {"rest": "flight", "flight": "rest"}[cur_action]
    reindeer[f"{cur_action}_left"] -= 1
    if not reindeer[f"{cur_action}_left"]:
        reindeer[f"{other_action}_left"] = reindeer[f"{other_action}_time"]


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1:", race(input_file, 1)["total_dist"])
        print("PART 2:", race(input_file, 2)["lead_time"])
    except IndexError:
        print("Enter path to data file!")

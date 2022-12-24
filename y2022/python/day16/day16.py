"""
Part 1 answer:
Part 2 answer:
"""
import re
from collections import deque

from y2022.python.shared import get_data_file_path


TIME_LIMIT = 30  # minutes
VALVE_LABEL_PATTERN = re.compile(r"[A-Z]{2}")
START_VALVE_LABEL = "AA"


class Valve:
    def __init__(self, label: str, flow_rate: int, neighbors: set[str]):
        self.label = label
        self.flow_rate = flow_rate
        self.neighbors = neighbors

    def __str__(self) -> str:
        return f"{self.label} ({self.flow_rate}) -> {self.neighbors}"


def main():
    all_valves: dict[str, Valve] = {}
    with open(get_data_file_path(__file__.split("/")[-1], sample=True), "r") as f_in:
        for line in f_in:
            new_valve = parse_valve(line)
            all_valves[new_valve.label] = new_valve
    valve_distances = {v.label: {v.label: 0} for v in all_valves.values()}
    for valve in all_valves.values():
        # print(valve)
        find_distances(deque([valve]), valve, all_valves, valve_distances)
        # print(f"{valve.label}: {valve_distances[valve.label]}")


def parse_valve(valve_definition: str) -> Valve:
    valve_info, neighbors_info = valve_definition.strip().split(";")
    valve_label = VALVE_LABEL_PATTERN.search(valve_info).group()
    flow_rate = int(re.search(r"\d+", valve_info).group())
    neighbors = set(VALVE_LABEL_PATTERN.findall(neighbors_info))
    new_valve = Valve(valve_label, flow_rate, neighbors)
    return new_valve


def find_distances(
    to_visit: deque[Valve],
    start_valve: Valve,
    all_valves: dict[str, Valve],
    valve_distances: dict[str, dict[str, int]],
):
    if not to_visit or len(valve_distances[start_valve.label]) == len(all_valves):
        return
    cur_valve = to_visit.popleft()
    cur_dist = valve_distances[start_valve.label][cur_valve.label]
    for valve_name in cur_valve.neighbors:
        if valve_name not in valve_distances[start_valve.label]:
            next_valve = all_valves[valve_name]
            new_dist = cur_dist + 1
            valve_distances[start_valve.label][valve_name] = new_dist
            to_visit.append(next_valve)
    find_distances(to_visit, start_valve, all_valves, valve_distances)


if __name__ == "__main__":
    main()

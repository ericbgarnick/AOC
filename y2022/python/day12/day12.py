from collections import deque
from typing import List, Tuple, Optional

from y2022.python.shared import get_data_file_path

GOAL_REACHED = False


def main():
    topo_map = []
    start = None
    end = None
    with open(get_data_file_path(__file__, sample=False), "r") as f_in:
        for row_num, line in enumerate(f_in):
            line = list(line.strip())
            if "S" in line:
                start = (row_num, line.index("S"))
                line[start[1]] = "a"
            if "E" in line:
                end = (row_num, line.index("E"))
                line[end[1]] = "z"
            topo_map.append(line)
    part_1(start, end, topo_map)
    part_2(end, topo_map)


def part_1(start: Tuple[int, int], end: Tuple[int, int], topo_map: List[List[str]]):
    distances = [[-1 for _ in range(len(topo_map[0]))] for _ in range(len(topo_map))]
    distances[start[0]][start[1]] = 0
    navigate(topo_map, distances, deque([(start[0], start[1])]), direction="ascending")
    print("PART 1:", distances[end[0]][end[1]])


def part_2(start: Tuple[int, int], topo_map: List[List[str]]):
    distances = [[-1 for _ in range(len(topo_map[0]))] for _ in range(len(topo_map))]
    distances[start[0]][start[1]] = 0
    print("PART 2:")
    navigate(
        topo_map,
        distances,
        deque([(start[0], start[1])]),
        direction="descending",
        goal="a",
    )


def navigate(
    topo_map: List[List[str]],
    distances: List[List[int]],
    to_visit: Optional[deque],
    direction: str,
    goal: Optional[str] = None,
):
    goal = goal or ""
    while not GOAL_REACHED and len(to_visit):
        visit(topo_map, distances, to_visit, direction, goal)


def visit(
    topo_map: List[List[str]],
    distances: List[List[int]],
    to_visit: Optional[deque],
    direction: str, goal: str,
):
    global GOAL_REACHED
    cur = to_visit.popleft()
    for n in get_neighbors(cur, topo_map, direction):
        if distances[n[0]][n[1]] == -1:
            distances[n[0]][n[1]] = distances[cur[0]][cur[1]] + 1
            if goal and topo_map[n[0]][n[1]] == goal:
                goal_dist = distances[n[0]][n[1]]
                print(f"REACHED GOAL IN {goal_dist} STEPS")
                GOAL_REACHED = True
                return
            to_visit.append(n)


def get_neighbors(
    cur: Tuple[int, int], topo_map: List[List[str]], direction: str,
) -> List[Tuple[int, int]]:
    neighbors = []
    elevation = topo_map[cur[0]][cur[1]]
    if cur[0] > 0:
        up = topo_map[cur[0] - 1][cur[1]]
        if ((direction == "ascending" and ord(up) - ord(elevation) <= 1) or
                (direction == "descending" and ord(elevation) - ord(up) <= 1)):
            neighbors.append((cur[0] - 1, cur[1]))
    if cur[0] < len(topo_map) - 1:
        down = topo_map[cur[0] + 1][cur[1]]
        if ((direction == "ascending" and ord(down) - ord(elevation) <= 1) or
                (direction == "descending" and ord(elevation) - ord(down) <= 1)):
            neighbors.append((cur[0] + 1, cur[1]))
    if cur[1] > 0:
        left = topo_map[cur[0]][cur[1] - 1]
        if ((direction == "ascending" and ord(left) - ord(elevation) <= 1) or
                (direction == "descending" and ord(elevation) - ord(left) <= 1)):
            neighbors.append((cur[0], cur[1] - 1))
    if cur[1] < len(topo_map[0]) - 1:
        right = topo_map[cur[0]][cur[1] + 1]
        if ((direction == "ascending" and ord(right) - ord(elevation) <= 1) or
                (direction == "descending" and ord(elevation) - ord(right) <= 1)):
            neighbors.append((cur[0], cur[1] + 1))
    return neighbors


if __name__ == "__main__":
    main()

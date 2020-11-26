from sys import argv
from typing import List, Dict, Set


def build_grid(filename: str, broken: bool = False) -> List[Dict]:
    conversion = {".": 0, "#": 1}
    init_data = "".join([line.strip() for line in open(filename, "r")])
    grid_size = int(len(init_data) ** 0.5)
    grid = []
    for idx, symbol in enumerate(init_data):
        val = 1 if broken and is_corner(idx, grid_size) else conversion[symbol]
        point = {
            "cur_val": val,
            "next_val": 0,
            "neighbors": calc_neighbors(idx, grid_size)
        }
        grid.append(point)
    return grid


def calc_neighbors(idx: int, grid_size: int) -> Set[int]:
    neighbors = set()
    if idx >= grid_size:
        add_prev_row(idx, grid_size, neighbors)
    if idx < grid_size * grid_size - grid_size:
        add_next_row(idx, grid_size, neighbors)
    if idx % grid_size:
        neighbors.add(idx - 1)              # left
    if idx % grid_size != grid_size - 1:
        neighbors.add(idx + 1)              # right
    return neighbors


def add_prev_row(idx: int, grid_size: int, neighbors: Set[int]):
    if idx % grid_size:
        neighbors.add(idx - grid_size - 1)  # up-left
    neighbors.add(idx - grid_size)          # up
    if idx % grid_size != grid_size - 1:
        neighbors.add(idx - grid_size + 1)  # up-right


def add_next_row(idx: int, grid_size: int, neighbors: Set[int]):
    if idx % grid_size:
        neighbors.add(idx + grid_size - 1)  # down-left
    neighbors.add(idx + grid_size)          # down
    if idx % grid_size != grid_size - 1:
        neighbors.add(idx + grid_size + 1)  # down-right


def run(grid: List[Dict], num_ticks: int, broken: bool = False) -> int:
    for _ in range(num_ticks):
        tick(grid, broken)
    return sum(point["cur_val"] for point in grid)


def tick(grid: List[Dict], broken: bool):
    for idx, light in enumerate(grid):
        if broken and is_corner(idx, int(len(grid) ** 0.5)):
            light["next_val"] = 1
        else:
            set_next_val(grid, light)
    for light in grid:
        light["cur_val"] = light["next_val"]


def is_corner(idx: int, grid_size: int) -> bool:
    grid_area = grid_size * grid_size
    return idx in [0, grid_size - 1, grid_area - grid_size, grid_area - 1]


def set_next_val(grid: List[Dict], light: Dict):
    neighbors_on = sum(grid[n]["cur_val"] for n in light["neighbors"])
    if light["cur_val"]:
        light["next_val"] = int(neighbors_on in [2, 3])
    else:
        light["next_val"] = int(neighbors_on == 3)


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1:", run(build_grid(input_file), 100))
        print("PART 2:", run(build_grid(input_file, broken=True), 100, broken=True))
    except IndexError:
        print("Enter path to data file!")

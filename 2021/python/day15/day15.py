from sys import argv
from typing import List, Set

FULL_MAP_MULTIPLE = 5


class Node:
    def __init__(self, index: int, weight: int, dist: float = float("inf")):
        self.index = index
        self.weight = weight
        self.dist = dist
        self.neighbors: Set["Node"] = set()

    def __str__(self) -> str:
        return f"{self.index} x{self.weight} @{self.dist}"

    def __eq__(self, other: "Node") -> bool:
        return self.dist == other.dist

    def __lt__(self, other: "Node") -> bool:
        return self.dist < other.dist

    def __gt__(self, other: "Node") -> bool:
        return self.dist > other.dist

    def __hash__(self) -> int:
        return self.index


class WeightedGraph:
    def __init__(self, weights: List[int], width: int):
        self.nodes = [Node(i, w) for i, w in enumerate(weights)]
        self.nodes[0].dist = 0
        self.dist_assigned = {self.nodes[0]}
        self.width = width

    def __str__(self) -> str:
        output_rows = []
        row_end = self.width
        while row_end <= len(self.nodes):
            row_start = row_end - self.width
            output_rows.append("".join([str(n.weight) for n in self.nodes[row_start:row_end]]))
            row_end += self.width
        return "\n".join(output_rows)

    def neighbors(self, node: Node) -> Set[Node]:
        return {self.nodes[idx] for idx in self.neighbor_indexes(node.index)}

    def neighbor_indexes(self, index: int) -> Set[int]:
        neighbors = set()
        if index >= self.width:
            neighbors.add(index - self.width)
        if index + self.width < len(self.nodes):
            neighbors.add(index + self.width)
        if index % self.width != 0:
            neighbors.add(index - 1)
        if (index + 1) % self.width != 0:
            neighbors.add(index + 1)
        return neighbors


def parse_input(filename: str, full_map: bool) -> WeightedGraph:
    with open(filename, "r") as f_in:
        width = 0
        weights = []
        for line in f_in:
            line = line.strip()
            width = len(line)
            weights.extend([int(val) for val in line])
        if full_map:
            wg = build_full_map(weights, width)
        else:
            wg = WeightedGraph(weights, width)
    for node in wg.nodes:
        node.neighbors = wg.neighbors(node)
    return wg


def build_full_map(start_weights: List[int], original_width: int) -> WeightedGraph:
    full_map = extend_horizontally(start_weights, original_width)
    full_map = extend_vertically(full_map)
    return WeightedGraph(full_map, original_width * FULL_MAP_MULTIPLE)


def extend_horizontally(original_map: List[int], width: int) -> List[int]:
    extended = []
    num_rows = len(original_map) // width
    for r in range(num_rows):
        row_start = r * width
        row_end = row_start + width
        for increment in range(FULL_MAP_MULTIPLE):
            extended.extend([incremented(val, increment) for val in original_map[row_start:row_end]])
    return extended


def extend_vertically(original_map: List[int]) -> List[int]:
    extended = []
    for increment in range(FULL_MAP_MULTIPLE):
        extended.extend([incremented(val, increment) for val in original_map])
    return extended


def incremented(original_val: int, amount: int) -> int:
    new_val = original_val + amount
    if new_val <= 9:
        return new_val
    else:
        return new_val % 9


def part1(wg: WeightedGraph) -> int:
    """
    Return the length of the shortest path from the first node in wg to the last.
    """
    dijkstra(wg)
    return int(wg.nodes[-1].dist)


def part2(wg: WeightedGraph) -> int:
    """
    Return the length of the shortest path from the first node in wg to the last.
    """
    dijkstra(wg)
    return int(wg.nodes[-1].dist)


def dijkstra(wg: WeightedGraph):
    q = set(node for node in wg.nodes)
    seen = set()
    while q:
        shortest = min(wg.dist_assigned, key=lambda n: n.dist)
        q.remove(shortest)
        wg.dist_assigned.remove(shortest)
        seen.add(shortest)
        for nn in shortest.neighbors - seen:
            if shortest.dist + nn.weight < nn.dist:
                nn.dist = shortest.dist + nn.weight
                wg.dist_assigned.add(nn)


def main():
    try:
        input_file = argv[1]
        wg = parse_input(input_file, full_map=False)
        print(f"PART 1: {part1(wg)}")
        wg = parse_input(input_file, full_map=True)
        print(f"PART 2: {part2(wg)}")
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

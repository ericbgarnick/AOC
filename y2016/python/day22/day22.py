import re
from argparse import ArgumentParser
from bisect import insort


class Node:
    def __init__(self, x_pos: int, y_pos: int, size: int, used: int, avail: int, use_pct: int):
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.used = used
        self.avail = avail
        self.use_pct = use_pct

    def __str__(self) -> str:
        return f"{self.used} / {self.size} @ ({self.x}, {self.y})"


def create_cluster(input_datafile: str) -> list[list[Node]]:
    cluster = []
    with open(input_datafile, "r") as f_in:
        # Skip command entry
        f_in.readline()
        # Skip headers
        f_in.readline()
        for line in f_in:
            x, y = [int(coord) for coord in re.findall(r"-[xy](\d{1,2})", line)]
            size, used, avail = [int(val) for val in re.findall(r" (\d+)T ", line)]
            use_pct = re.search(r"(\d+)%", line).group(1)
            node = Node(x, y, size, used, avail, int(use_pct))
            if y >= len(cluster):
                cluster.append([node])
            else:
                cluster[y].append(node)
    return cluster


def count_viable_pairs(cluster: list[list[Node]]) -> int:
    total = 0
    increasing_availability = []
    for row in cluster:
        for node in row:
            insort(increasing_availability, node, key=lambda n: n.avail)
    for row in cluster:
        for node in row:
            if node.used == 0:
                continue
            node_idx = min_avail_match_index(increasing_availability, node)
            if node_idx != -1:
                total += len(increasing_availability) - node_idx
                if node.avail >= node.used:
                    # Node can't be a viable pair with itself
                    total -= 1
    return total


def min_avail_match_index(sorted_nodes: list[Node], query_node: Node) -> int:
    """
    Return the index of smallest available space
    that is larger than used space of query_node.
    """
    low = 0
    high = len(sorted_nodes) - 1
    guess = (low + high) // 2
    while True:
        if sorted_nodes[guess].avail == query_node.used:
            return guess

        avail_too_low = sorted_nodes[guess].avail < query_node.used
        if low == high:
            if avail_too_low:
                return -1
            else:
                return guess
        else:
            if avail_too_low:
                low = guess + 1
            else:
                high = guess
            guess = (low + high) // 2


def part_2():
    """
    * track target data coordinates
    * Best case: straight path across, all empty (len row - 1)
    * Worse cases:
    * * only nodes with enough space to hold target data are in a convoluted path
    * * many moves required to clear space for target data
    """
    pass


def main():
    parser = ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()

    if args.sample:
        datafile = "y2016/data/22_sample.txt"
    else:
        datafile = "y2016/data/22.txt"
    cluster = create_cluster(datafile)
    viable_pairs = count_viable_pairs(cluster)
    print("PART 1:", viable_pairs)



if __name__ == "__main__":
    main()

"""
Construct a graph, represented as an adjacency list,
where nodes are bag descriptions and each bag has
a list of 'parents' and a dictionary of 'children'
{<description>: <required count>}.
Ex.
{
    "light green": {
        "parents": [],
        "children": {"sparkly pink": 5}
    }
    "shiny red": {
        "parents": [],
        "children": {"dull gray": 2, "sparkly pink": 1}
    },
    "dull gray": {
        "parents": ["shiny red"],
        "children": {"faded yellow": 3}
    }
    "sparkly pink": {
        "parents": ["light green", "shiny red"],
        "children": {}
    }
    "faded yellow": {
        "parents": ["dull gray"],
        "children": {}
    }
}
"""
import re
from sys import argv
from typing import Dict, List, Any, Set


def construct_graph(filename: str) -> Dict[str, Any]:
    """Return adjacency list graph where nodes have
    'children' and 'parents' attributes"""
    bag_graph = {}
    for line in open(filename, "r"):
        parent, children = line.strip().split(" bags contain ")
        children = parse_children(children.split(", "))
        update_children(bag_graph, parent, children)
        update_parents(bag_graph, parent, children)
    return bag_graph


def parse_children(children: List[str]) -> Dict[str, int]:
    """Return the {description: number} for children"""
    children_specs = {}
    for child in children:
        if child[0].isdecimal():
            count = int(child[0])
            rest = child[2:].strip(".")
            description = re.sub(r" bags?", "", rest)
            children_specs[description] = count
    return children_specs


def update_children(bag_graph: Dict, parent: str, children: Dict):
    """Set 'children' for 'parent'"""
    try:
        bag_graph[parent]["children"] = children
    except KeyError:
        bag_graph[parent] = {"children": children, "parents": []}


def update_parents(bag_graph: Dict, parent: str, children: Dict):
    """Update 'parents' for each child in 'children'"""
    for child in children:
        try:
            bag_graph[child]["parents"].append(parent)
        except KeyError:
            bag_graph[child] = {"children": {}, "parents": [parent]}


def count_ancestors(bag_graph: Dict, node: str) -> int:
    """Return the total number of unique nodes nested under node"""
    return len(find_ancestors(bag_graph, node, set()))


def find_ancestors(bag_graph: Dict, start_node: str, ancestors: Set[str]) -> Set[str]:
    """Return the set of all unique ancestors of start_node"""
    try:
        parents = set(bag_graph[start_node]["parents"])
        for p in parents - ancestors:  # Skip ancestors already seen
            ancestors |= find_ancestors(bag_graph, p, ancestors)
        ancestors |= parents
    except KeyError:
        ancestors = set()  # no parents (a root node)
    return ancestors


def count_descendants(bag_graph: Dict, node: str) -> int:
    """Return the total number of nested nodes under node"""
    descendants = 0
    for child, count in bag_graph[node]["children"].items():
        descendants += count * (1 + count_descendants(bag_graph, child))
    return descendants


if __name__ == "__main__":
    input_file = argv[1]
    graph = construct_graph(input_file)
    print("PART 1:", count_ancestors(graph, "shiny gold"))
    print("PART 2:", count_descendants(graph, "shiny gold"))

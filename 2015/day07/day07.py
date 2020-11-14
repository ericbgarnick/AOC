import re
from os import path
from typing import List, Dict, Any

from operation import op_not, op_lshift, op_rshift, op_and, op_or
from topo_sort import topological_sort


################
# Create graph #
################
def construct_graph(raw_input: List[str]) -> Dict:
    graph = {}
    for line in raw_input:
        add_node(graph, line)
    return graph


def add_node(graph: Dict, line: str):
    """
    c - condition: Optional[str]
    d - descendants: List[str]
    v - value: Optional[int]
    f - finished: Optional[Bool]
    """
    condition, node_name = line.split(" -> ")
    predecessors = re.findall(r"[a-z]+", condition)
    try:
        graph[node_name]["c"] = condition
    except KeyError:
        graph[node_name] = new_node({"c": condition})
    for p in predecessors:
        try:
            graph[p]["d"].append(node_name)
        except KeyError:
            graph[p] = new_node({"d": [node_name]})


def new_node(start_values: Dict[str, Any]) -> Dict[str, Any]:
    n = {
        "c": None,
        "d": [],
        "v": None,
        "f": None,
    }
    n.update(**start_values)
    return n


####################
# Calculate values #
####################
def apply_conditions(graph: Dict[str, Dict], ordering: List[str]):
    for node_name in ordering:
        apply(graph, node_name)


def apply(graph: Dict[str, Dict], node_name: str):
    condition = graph[node_name]["c"]
    try:
        operation = re.search(r"[A-Z]+", condition).group()
    except AttributeError:
        operation = ""
    dependencies = re.findall(r"[a-z]+", condition)
    dep_vals = vals_for_keys(graph, dependencies)

    if operation == "NOT":
        value = op_not(dep_vals[0])
    elif operation.endswith("SHIFT"):
        offset = literal_vals(condition)[0]
        if operation[0] == "L":
            value = op_lshift(dep_vals[0], offset)
        else:  # RSHIFT
            value = op_rshift(dep_vals[0], offset)
    elif operation:  # AND / OR
        dep_vals += literal_vals(condition)
        if operation == "AND":
            value = op_and(*dep_vals)
        else:  # OR
            value = op_or(*dep_vals)
    else:
        dep_vals += literal_vals(condition)
        value = dep_vals[0]

    graph[node_name]["v"] = value


def vals_for_keys(graph: Dict[str, Any], keys: List[str]) -> List[int]:
    return [graph[key]["v"] for key in keys]


def literal_vals(condition: str) -> List[int]:
    return [int(d) for d in re.findall(r"\d+", condition)]


def reset_values(graph: Dict[str, Any]):
    for v in graph.values():
        v["v"] = None


if __name__ == "__main__":
    input_file = path.dirname(path.abspath(__file__)) + "/data07.txt"
    input_contents = [line.strip() for line in open(input_file, "r")]
    new_graph = construct_graph(input_contents)
    sorted_nodes = topological_sort(new_graph)

    # PART 1
    apply_conditions(new_graph, sorted_nodes)
    a_val = new_graph["a"]["v"]
    print("PART 1:", a_val)

    # PART 2
    new_graph["b"]["c"] = str(a_val)
    apply_conditions(new_graph, sorted_nodes)
    print("PART 2:", new_graph["a"]["v"])

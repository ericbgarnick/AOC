from typing import Dict, List


def topological_sort(graph: Dict) -> List[str]:
    """Return the names of graph nodes in topological-sort order"""
    node_stack = []
    for node_name in graph:
        if graph[node_name]["f"] is None:
            visit(graph, node_name, node_stack)

    return node_stack[-1::-1]


def visit(graph: Dict, node_name: str, node_stack: List[str]):
    graph[node_name]["f"] = False
    for d in graph[node_name]["d"]:
        if graph[d]["f"] is None:
            visit(graph, d, node_stack)

    graph[node_name]["f"] = True
    node_stack.append(node_name)

import pytest

from y2016.python.day22.day22 import Node, min_avail_match_index, count_viable_pairs


@pytest.fixture
def cluster() -> list[list[Node]]:
    return [
        [Node(0, 0, 10, 8, 2, 80), Node(1, 0, 9, 7, 2, 77), Node(2, 0, 10, 6, 4, 60)],
        [Node(0, 1, 11, 6, 5, 54), Node(1, 1, 8, 0, 8, 0), Node(2, 1, 9, 8, 1, 88)],
        [Node(0, 2, 32, 28, 4, 87), Node(1, 2, 11, 7, 4, 63), Node(2, 2, 9, 6, 3, 66)],
    ]


@pytest.fixture
def nodes() -> list[Node]:
    return [
        Node(0, 0, 0, 14, 10, 58),
        Node(0, 0, 0, 12, 13, 48),
        Node(0, 0, 0, 10, 15, 40),
    ]


@pytest.mark.parametrize(
    "query_node_idx, expected_node_idx",
    [
        (0, 2),
        (1, 1),
        (2, 0)
    ],
)
def test_min_avail_match_index(query_node_idx, expected_node_idx, nodes):
    idx = min_avail_match_index(nodes, nodes[query_node_idx])
    assert idx == expected_node_idx


def test_min_avail_match_index_extrema(nodes):
    query_node = Node(0, 0, 0, 1, 16, 10)
    sorted_nodes = [n for n in nodes] + [query_node]
    idx = min_avail_match_index(sorted_nodes, query_node)
    assert idx == 0


def test_count_viable_pairs(cluster):
    num_viable_pairs = count_viable_pairs(cluster)
    assert num_viable_pairs == 7

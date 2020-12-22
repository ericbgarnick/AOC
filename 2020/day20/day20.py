import re
from functools import reduce
from sys import argv
from typing import Dict, Set, Union, List

TileType = Dict[str, Union[str, int]]


def part_1(filename: str):
    all_tiles = read_tiles(filename)
    known_edges = {}
    for tile_id, tile_img in all_tiles.items():
        record_tile(tile_img, tile_id, known_edges)
    outer_tiles = get_outer_tiles(known_edges)
    corner_ids = [tid for tid, edges in outer_tiles.items() if len(edges) == 2]
    return reduce(int.__mul__, corner_ids)


def read_tiles(filename: str) -> Dict[int, List[str]]:
    tiles = {}
    raw_tiles = open(filename, "r").read().split("\n\n")
    for tile_def in raw_tiles:
        tile_split = tile_def.split("\n")
        tile_id = int(re.search(r"\d+", tile_split[0]).group())
        tiles[tile_id] = tile_split[1:]
    return tiles


def record_tile(
        tile_img: List[str],
        tile_id: int,
        known_edges: Dict[str, Set[int]],
):
    """Record all edges from tile_img in known_edges, associated with tile_id"""
    for edge in get_tile_edges(tile_img):
        if edge in known_edges:
            known_edges[edge].add(tile_id)
        elif edge[-1::-1] in known_edges:
            known_edges[edge[-1::-1]].add(tile_id)
        else:
            known_edges[edge] = {tile_id}


def get_tile_edges(tile_img: List[str]) -> List[str]:
    """Return a string representing each edge of tile_img"""
    return [
        tile_img[0],                            # top
        tile_img[-1],                           # bottom
        "".join([row[0] for row in tile_img]),  # left
        "".join([row[-1] for row in tile_img])  # right
    ]


def get_outer_tiles(known_edges: Dict[str, Set[int]]) -> Dict[int, Set[str]]:
    """Return a mapping of each perimeter tile id to a set of its outer edge(s)"""
    outer_tiles = {}
    for edge, ids in known_edges.items():
        if len(ids) == 1:
            tile_id = ids.pop()
            try:
                outer_tiles[tile_id].add(edge)
            except KeyError:
                outer_tiles[tile_id] = {edge}
    return outer_tiles


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", part_1(input_file))

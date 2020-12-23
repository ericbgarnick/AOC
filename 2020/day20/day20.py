import re
from functools import reduce
from sys import argv
from typing import Dict, Set, Union, List, Optional

TileType = Dict[str, Union[str, int]]


# == PART 1 == #
def part_1(filename: str) -> int:
    all_tiles = read_tiles(filename)
    matched_edges = {}
    for tile_id, tile_img in all_tiles.items():
        record_tile(tile_img, tile_id, matched_edges)
    corner_ids = get_corner_ids(matched_edges)
    return reduce(int.__mul__, corner_ids)


# == PART 2 == #
def part_2(filename: str) -> int:
    all_tiles = read_tiles(filename)
    matched_edges = {}
    for tile_id, tile_img in all_tiles.items():
        record_tile(tile_img, tile_id, matched_edges)
    corner_ids = get_corner_ids(matched_edges)
    arranged = arrange_tiles(all_tiles, matched_edges, corner_ids)
    # print_tiles(arranged)
    strip_edges(arranged)
    final_image = stitch_images(arranged)
    for row in final_image:
        print(row)
    return 1


def arrange_tiles(
        all_tiles: Dict[int, List[str]],
        matched_edges: Dict[str, Set[int]],
        corner_ids: List[int],
) -> List[List[Dict]]:
    arranged = []
    first_corner = {"id": corner_ids[0], "img": all_tiles[corner_ids[0]]}
    first_corner = orient_first_corner(first_corner, matched_edges)
    next_row_start = first_corner
    while next_row_start:
        arranged.append([next_row_start])
        next_tile = next_row_start
        while next_tile:
            next_tile = get_next_tile(all_tiles, matched_edges, next_tile)
            if next_tile:
                arranged[-1].append(next_tile)
        next_row_start = get_next_row_start(all_tiles, matched_edges, next_row_start)
    return arranged


def strip_edges(tiles: List[List[Dict]]):
    for tile_row in tiles:
        for tile in tile_row:
            tile["img"] = [img_row[1:-1] for img_row in tile["img"][1:-1]]


def stitch_images(tiles: List[List[Dict]]) -> List[str]:
    tile_width = len(tiles[0][0]["img"])
    stitched = []
    for tile_row_idx, tile_row in enumerate(tiles):
        for _ in range(tile_width):
            stitched.append([])
        for tile in tile_row:
            for img_row_idx, img_row in enumerate(tile["img"]):
                stitched_row_idx = tile_row_idx * tile_width + img_row_idx
                stitched[stitched_row_idx].append(img_row)
    return ["".join(stitched_row) for stitched_row in stitched]


def orient_first_corner(
        first_corner: Dict,
        matched_edges: Dict[str, Set[int]],
) -> Dict:
    """There must be one unmatched edge already on top or bottom
    and one on left or right of first_corner tile,
    so either leave as is, flip once, or flip twice"""
    n, s, w, e = get_tile_edges(first_corner["img"])

    # orient tile so unmatched edges are on top and left
    if (len(matched_edges.get(s, set())) == 1) or (len(matched_edges.get(s[-1::-1], set())) == 1):
        # flip img so s edge becomes top
        first_corner["img"] = flip_on_x(first_corner["img"])

    if (len(matched_edges.get(e, set())) == 1) or (len(matched_edges.get(e[-1::-1], set())) == 1):
        # flip img so e edge becomes left
        first_corner["img"] = flip_on_y(first_corner["img"])

    # Remove this tile from matched_edges
    for edge in [n, s, w, e]:
        try:
            matched_edges[edge] -= {first_corner["id"]}
        except KeyError:
            matched_edges[edge[-1::-1]] -= {first_corner["id"]}

    return first_corner


def get_next_tile(
        all_tiles: Dict[int, List[str]],
        matched_edges: Dict[str, Set[int]],
        prev_tile: Dict,
) -> Optional[Dict]:
    """
    - Find tile whose edge matches the eastern edge of prev_tile
    - Orient the next tile to match prev_tile orientation
    - Remove next tile edges from matched_edges
    """
    _, _, _, prev_e = get_tile_edges(prev_tile["img"])
    try:
        next_tile_id = matched_edges.get(prev_e).pop()
    except KeyError:
        # End of the row, no next tile
        return None
    except AttributeError:
        try:
            next_tile_id = matched_edges.get(prev_e[-1::-1]).pop()
        except KeyError:
            # End of the row, no next tile
            return None

    next_tile_img = all_tiles[next_tile_id]
    next_n, next_s, next_w, next_e = get_tile_edges(next_tile_img)

    # Orient next tile image to match with prev_tile
    if next_w == prev_e:
        pass
    elif next_w[-1::-1] == prev_e:
        next_tile_img = flip_on_x(next_tile_img)
    elif next_e == prev_e:
        next_tile_img = flip_on_y(next_tile_img)
    elif next_e[-1::-1] == prev_e:
        next_tile_img = flip_on_x(flip_on_y(next_tile_img))
    elif next_n == prev_e:
        next_tile_img = flip_on_neg_1(next_tile_img)
    elif next_n[-1::-1] == prev_e:
        next_tile_img = flip_on_neg_1(flip_on_y(next_tile_img))
    elif next_s == prev_e:
        next_tile_img = flip_on_1(flip_on_y(next_tile_img))
    elif next_s[-1::-1] == prev_e:
        next_tile_img = flip_on_1(next_tile_img)

    # Remove this tile from matched_edges
    for edge in [next_n, next_s, next_w, next_e]:
        try:
            matched_edges[edge] -= {next_tile_id}
        except KeyError:
            matched_edges[edge[-1::-1]] -= {next_tile_id}

    return {"id": next_tile_id, "img": next_tile_img}


def get_next_row_start(
        all_tiles: Dict[int, List[str]],
        matched_edges: Dict[str, Set[int]],
        prev_tile: Dict,
) -> Optional[Dict]:
    """Do stuff"""
    _, prev_s, _, _ = get_tile_edges(prev_tile["img"])
    try:
        next_tile_id = matched_edges.get(prev_s).pop()
    except KeyError:
        # End last row, no next tile
        return None
    except AttributeError:
        try:
            next_tile_id = matched_edges.get(prev_s[-1::-1]).pop()
        except KeyError:
            # End last row, no next tile
            return None

    next_tile_img = all_tiles[next_tile_id]
    next_n, next_s, next_w, next_e = get_tile_edges(next_tile_img)

    # Orient next tile image to match with prev_tile
    if next_n == prev_s:
        pass
    elif next_n[-1::-1] == prev_s:
        next_tile_img = flip_on_y(next_tile_img)
    elif next_s == prev_s:
        next_tile_img = flip_on_x(next_tile_img)
    elif next_s[-1::-1] == prev_s:
        next_tile_img = flip_on_x(flip_on_y(next_tile_img))
    elif next_w == prev_s:
        next_tile_img = flip_on_neg_1(next_tile_img)
    elif next_w[-1::-1] == prev_s:
        next_tile_img = flip_on_neg_1(flip_on_x(next_tile_img))
    elif next_e == prev_s:
        next_tile_img = flip_on_1(flip_on_x(next_tile_img))
    elif next_e[-1::-1] == prev_s:
        next_tile_img = flip_on_1(next_tile_img)

    # Remove this tile from matched_edges
    for edge in [next_n, next_s, next_w, next_e]:
        try:
            matched_edges[edge] -= {next_tile_id}
        except KeyError:
            matched_edges[edge[-1::-1]] -= {next_tile_id}

    return {"id": next_tile_id, "img": next_tile_img}


def print_tiles(tiles: List[List[Dict]], images: bool = False):
    if images:
        pass
    else:
        for row in tiles:
            for tile in row:
                print(tile["id"], end=" ")
            print("\n", end="")


# == SHARED == #
def read_tiles(filename: str) -> Dict[int, List[str]]:
    """Return each tile id mapped to the tile in its original orientation"""
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
        matched_edges: Dict[str, Set[int]],
):
    """Record all edges from tile_img in matched_edges, associated with tile_id"""
    for edge in get_tile_edges(tile_img):
        if edge in matched_edges:
            matched_edges[edge].add(tile_id)
        elif edge[-1::-1] in matched_edges:
            matched_edges[edge[-1::-1]].add(tile_id)
        else:
            matched_edges[edge] = {tile_id}


def get_tile_edges(tile_img: List[str]) -> List[str]:
    """Return a string representing each edge of tile_img"""
    return [
        tile_img[0],                            # North
        tile_img[-1],                           # South
        "".join([row[0] for row in tile_img]),  # West
        "".join([row[-1] for row in tile_img])  # East
    ]


def get_corner_ids(matched_edges: Dict[str, Set[int]]) -> List[int]:
    """Return a list of tile ids for the corner tiles"""
    outer_tiles = {}
    for edge, ids in matched_edges.items():
        if len(ids) == 1:
            tile_id = min(ids)  # Hack to retrieve value without removing from set
            try:
                outer_tiles[tile_id].add(edge)
            except KeyError:
                outer_tiles[tile_id] = {edge}
    return [tid for tid, edges in outer_tiles.items() if len(edges) == 2]


def flip_on_y(image: List[str]) -> List[str]:
    return [row[-1::-1] for row in image]


def flip_on_x(image: List[str]) -> List[str]:
    return image[-1::-1]


def flip_on_neg_1(image: List[str]) -> List[str]:
    n = len(image)
    flipped = [["" for _ in range(n)] for _ in range(n)]
    for row in range(n):
        for col in range(row, n):
            flipped[row][col], flipped[col][row] = image[col][row], image[row][col]
    return ["".join(row) for row in flipped]


def flip_on_1(image: List[str]) -> List[str]:
    n = len(image)
    last = n - 1
    flipped = [["" for _ in range(n)] for _ in range(n)]
    for row in range(last, -1, -1):
        for col in range(last - row, n):
            flipped[row][col], flipped[last - col][last - row] = image[last - col][last - row], image[row][col]
    return ["".join(row) for row in flipped]


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", part_1(input_file))
    part_2(input_file)

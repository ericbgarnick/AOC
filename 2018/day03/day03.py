from sys import argv
from typing import List, Dict


def overlapping_spots(claim_list: List[str], puzzle_part: int):
    fabric = [[0 for _ in range(1000)] for _ in range(1000)]
    claims = []
    for claim in claim_list:
        claim_id, rest = [x.strip() for x in claim.split('@')]
        pos, area = [x.strip() for x in rest.split(':')]
        hor, vert = [int(x.strip()) for x in pos.split(',')]
        width, height = [int(x.strip()) for x in area.split('x')]

        claims.append({'id': claim_id, 'hor': hor, 'vert': vert,
                       'width': width, 'height': height})

        for w in range(width):
            for h in range(height):
                fabric[vert + h][hor + w] += 1

    if puzzle_part == 1:
        overlaps = count_overlaps(fabric)
        print("{} overlaps".format(overlaps))

    elif puzzle_part == 2:
        claim_id = lone_claim(claims, fabric)
        print("Lone claim {}".format(claim_id))


def count_overlaps(fabric: List[List[int]]) -> int:
    overlaps = 0
    for row in fabric:
        for spot in row:
            if spot > 1:
                overlaps += 1
    return overlaps


def lone_claim(claims: List[Dict], fabric: List[List[int]]):
    for claim in claims:
        if is_lone_claim(claim, fabric):
            return claim['id']


def is_lone_claim(claim: Dict, fabric: List[List[int]]) -> bool:
    vert = claim['vert']
    hor = claim['hor']
    width = claim['width']
    height = claim['height']
    if fabric[vert][hor] == 1:
        for w in range(width):
            for h in range(height):
                if fabric[vert + h][hor + w] != 1:
                    return False
        return True
    else:
        return False


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [l.strip() for l in open(data_file, 'r').readlines()]
    part = int(argv[2])

    print("Running part", part)

    overlapping_spots(data_lines, part)

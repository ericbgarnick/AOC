from collections import defaultdict
from sys import argv
from typing import List, Dict


def part1(box_ids: List[str]) -> int:
    doubles = 0
    triples = 0
    for box_id in box_ids:
        d_found = t_found = False
        for letter in set(box_id):
            l_count = box_id.count(letter)
            if l_count == 2:
                d_found = True
            elif l_count == 3:
                t_found = True
        if d_found:
            doubles += 1
        if t_found:
            triples += 1
    return doubles * triples


def part2(box_ids: List[str]) -> str:
    """Solution has O(N x M) runtime, where N is the number of box ids,
    and M is the length of a box id.

    A record is created of which box ids have which letters at each index in
    the id. Each box id is compared to each previously seen box_id having the
    same letters at the same indices. A match has been found when a prior
    box id has 1 match fewer than the length of the id."""
    record = {}  # {<letter_idx>: {<letter>: {id_idx, ...}, ...}, ...}
    for id_idx, box_id in enumerate(box_ids):
        matches = defaultdict(int)  # {<id_idx>: <match count>}

        match = match_letters(record, matches, box_ids, box_id, id_idx)
        if match:
            return match

    return ""


def match_letters(record: Dict, matches: Dict, box_ids: List[str],
                  box_id: str, id_idx: int):
    for letter_idx, letter in enumerate(box_id):
        for match in record.get(letter_idx, {}).get(letter, set()):
            new_match_count = matches[match] + 1
            matches[match] = new_match_count

            if new_match_count + 1 == len(box_id):
                orig = box_ids[match]
                return ''.join([orig[i] for i, l in
                                enumerate(orig) if box_id[i] == l])

        populate_record(record, letter_idx, letter, id_idx)

    return ""


def populate_record(record: Dict, letter_idx: int, letter: str, id_idx: int):
    if letter_idx in record:
        try:
            record[letter_idx][letter].add(id_idx)
        except KeyError:
            record[letter_idx][letter] = {id_idx}
    else:
        record[letter_idx] = {letter: {id_idx}}


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [l.strip() for l in open(data_file, 'r').readlines()]
    part = int(argv[2])

    if part == 1:
        print("Checksum: {}".format(part1(data_lines)))
    elif part == 2:
        print("Common letters: {}".format(part2(data_lines)))

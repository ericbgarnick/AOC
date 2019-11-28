import hashlib
import time
from collections import defaultdict
from sys import argv

from acre import Acre
from lumber_collection import LumberCollection


COLLECTION_RECORD = defaultdict(list)


def run_simulation(lumber_collection: LumberCollection, cycles: int):
    i = loop = 0
    while i < cycles:
        update_collection(lumber_collection)

        cur_values = [a.type for a in lumber_collection.collection_area]
        area_total = sum(cur_values)
        hash_key = hashlib.md5(str(area_total).encode('utf-8')).hexdigest()
        if not loop and hash_key in COLLECTION_RECORD:
            for idx, values in COLLECTION_RECORD[hash_key]:
                if cur_values == values:
                    # Loop found!
                    loop = i - idx
                    while i < cycles - loop:
                        i += loop
                    break
        elif not loop:
            COLLECTION_RECORD[hash_key].append((i, cur_values))
        i += 1


def update_collection(lumber_collection: LumberCollection):
    for acre in lumber_collection.collection_area:
        acre.calc_next_type()
    for acre in lumber_collection.collection_area:
        acre.update_type()


def calc_result(lumber_collection: LumberCollection) -> int:
    open_acres = 0
    lumber_yards = 0
    wooded_acres = 0
    for acre in lumber_collection.collection_area:
        if acre.type == Acre.OPEN:
            open_acres += 1
        elif acre.type == Acre.LUMBER:
            lumber_yards += 1
        else:
            wooded_acres += 1
    return wooded_acres * lumber_yards


if __name__ == '__main__':
    data_file, num_cycles = argv[1:3]
    data = [line.strip() for line in open(data_file, 'r').readlines()]
    collection = LumberCollection(data)

    start = time.perf_counter()
    run_simulation(collection, int(num_cycles))
    print("SECONDS ELAPSED:", time.perf_counter() - start)

    result = calc_result(collection)
    print("Total:", result)

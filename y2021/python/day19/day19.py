import re
from sys import argv
from typing import List

from scanner import Scanner


def parse_input(filename: str) -> List[Scanner]:
    curr_scanner_beacons = []
    scanners = []
    for line in open(filename, "r"):
        if not line.strip():
            continue
        if line.startswith("---"):
            if curr_scanner_beacons:
                scanners.append(Scanner(curr_scanner_beacons))
            curr_scanner_beacons = []
        else:
            x, y, z = re.findall(r"-?\d+", line.strip())
            curr_scanner_beacons.append((int(x), int(y), int(z)))
    scanners.append(Scanner(curr_scanner_beacons))
    return scanners


def part1(scanners: List[Scanner]) -> Scanner:
    """
    """
    return assemble_beacon_map(scanners)


def assemble_beacon_map(scanners: List[Scanner]) -> Scanner:
    next_scanners = []
    while len(scanners) > 1:
        for i, scanner1 in enumerate(scanners[:-1]):
            for j in range(i + 1, len(scanners)):
                scanner2 = scanners[j]
                if scanner2.overlaps(scanner1):
                    scanner1.merge(scanner2)
                    next_scanners = [scanner for k, scanner in enumerate(scanners) if k != j]
                    break
            if next_scanners:
                break
        scanners = next_scanners
        next_scanners = []
        print([len(s.beacons) for s in scanners])
    return scanners[0]


def part2(scanners: List[Scanner]) -> int:
    """
    """
    print([s.origin for s in scanners])
    print("")
    unmerged = [s for s in scanners[1:] if s.origin == (0, 0, 0)]
    for i in range(len(unmerged)):
        can_merge = unmerged[i].overlaps(scanners[0], debug=True)
        print("CAN MERGE:", can_merge, end="\n\n")
    max_dist = 0
    for i, s1 in enumerate(scanners[:-1]):
        for j in range(i + 1, len(scanners)):
            s2 = scanners[j]
            o1 = s1.origin
            o2 = s2.origin
            max_dist = max(abs(o2[0] - o1[0]) + abs(o2[1] - o1[1]) + abs(o2[2] - o1[2]), max_dist)
    return max_dist


def main():
    try:
        input_file = argv[1]
    except IndexError:
        print("Enter path to data file!")
        return
    scanners = parse_input(input_file)
    joined = part1(scanners)
    print("PART 1:", len(joined.beacons))
    print("PART 2:", part2(scanners))


if __name__ == "__main__":
    main()

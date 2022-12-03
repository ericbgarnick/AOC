from typing import Tuple, List, Optional

Beacon = Tuple[int, int, int]


class Scanner:
    def __init__(self, beacon_coords: List[Beacon], origin: Tuple[int, int, int] = (0, 0, 0)):
        self.beacons = beacon_coords
        self.origin = origin

    @property
    def x(self) -> List[int]:
        return [beacon[0] for beacon in self.beacons]

    @property
    def y(self) -> List[int]:
        return [beacon[1] for beacon in self.beacons]

    @property
    def z(self) -> List[int]:
        return [beacon[2] for beacon in self.beacons]

    def overlaps(self, other: "Scanner", debug: bool = False) -> bool:
        """
        Return True if >= 12 of the beacons other scanner
        detects overlap with self.beacons.

        Reorients self while looking for overlaps.
        """
        if debug:
            print("ORIGINAL:", self.beacons)
        one_d_overlaps = find_overlaps(other, self, "x", debug=debug)
        if debug:
            print("1D OVERLAPS:", one_d_overlaps)
        for axis1, offset1 in one_d_overlaps:
            applied_one_d = apply_offset(self, axis1, offset1, 1)
            if debug:
                print("APPLIED 1D:", applied_one_d.beacons)
            hold_axis = axis1.strip("-")
            two_d_overlaps = find_overlaps(other, applied_one_d, "y", "x", debug=debug)
            if debug:
                print("2D OVERLAPS:", two_d_overlaps)
            for axis2, offset2 in two_d_overlaps:
                applied_two_d = apply_offset(applied_one_d, axis2, offset2, 2, hold_axis=axis1.strip("-"))
                if debug:
                    print("APPLIED 2D:", applied_two_d.beacons)
                hold_axes = axis1.strip("-") + axis2.strip("-")
                three_d_overlaps = find_overlaps(other, applied_two_d, "z", "xy", debug=debug)
                if debug:
                    print("3D OVERLAPS:", three_d_overlaps)
                for axis3, offset3 in three_d_overlaps:
                    applied_three_d = apply_offset(applied_two_d, axis3, offset3, 3)
                    if debug:
                        print("APPLIED 3D:", applied_three_d.beacons)
                    if overlap_success(other, applied_three_d):
                        self.beacons = applied_three_d.beacons
                        self.origin = applied_three_d.origin
                        if debug:
                            print(f"\nUSING OFFSETS {offset1}, {offset2}, {offset3}\n")

                        return True
        return False

    def merge(self, other: "Scanner"):
        """Add all beacons from other to self.beacons. Other must already be oriented with self."""
        for beacon in other.beacons:
            if beacon not in self.beacons:
                self.beacons.append(beacon)


def find_overlaps(
        ref_scanner: Scanner,
        new_scanner: Scanner,
        ref_axis: str,
        hold_axes: Optional[str] = "",
        debug: bool = False,
) -> List[Tuple[str, int]]:
    """
    Return a list of pairs of axis label with offset value for axis+offsets
    that result in at least 12 overlaps between ref_scanner and new_scanner.
    """
    axes = "xyz"
    ref_axis_idx = axes.index(ref_axis)
    ref_scanner_vals = [triple[ref_axis_idx] for triple in ref_scanner.beacons]

    overlaps = []

    for i, axis in enumerate(axes):
        if axis in hold_axes:
            continue
        new_scanner_vals = [triple[i] for triple in new_scanner.beacons]
        offsets = get_offsets(ref_scanner_vals, new_scanner_vals, debug=debug)
        overlaps += [(axis, offset) for offset in offsets]
        offsets = get_offsets(ref_scanner_vals, [-1 * v for v in new_scanner_vals], debug=debug)
        overlaps += [(f"-{axis}", offset) for offset in offsets]
    return overlaps


def get_offsets(
        ref_values: List[int],
        new_values: List[int],
        debug: bool = False,
) -> List[int]:
    """
    Compare ref_values with new_values by shifting new_values
    so that its first value aligns with each value in ref_values.
    Return the alignment shifts that produce the overlaps >= 12.
    """
    offsets = []
    ref_val_set = set(ref_values)
    sorted_ref_values = sorted(ref_values)
    sorted_new_values = sorted(new_values)
    offset_ends = [
        sorted_new_values[-1] - sorted_ref_values[0],
        sorted_new_values[0] - sorted_ref_values[-1],
    ]
    for offset in range(min(offset_ends), max(offset_ends) + 1):
        offset_new_values = {v - offset for v in sorted_new_values}
        alignment_count = len(ref_val_set & offset_new_values)
        if alignment_count >= 12:
            offsets.append(offset)
        elif debug and alignment_count > 9:
            print("ALIGNMENT COUNT:", alignment_count)

    return offsets


def apply_offset(
        scanner: Scanner,
        offset_axis: str,
        offset: int,
        alignment_num: int,
        hold_axis: Optional[str] = None,
) -> Scanner:
    if offset_axis == "x":
        if alignment_num == 1:
            scanner = Scanner([(x - offset, y, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x - offset, y, z)
        elif alignment_num == 2:
            scanner = Scanner([(y, -1 * x - offset, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (y, -1 * x - offset, z)
        elif alignment_num == 3:
            scanner = Scanner([(x - offset, y, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x - offset, y, z)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    elif offset_axis == "-x":
        if alignment_num == 1:
            scanner = Scanner([(-1 * x - offset, -1 * y, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (-1 * x - offset, -1 * y, z)
        elif alignment_num == 2:
            scanner = Scanner([(-1 * y, x - offset, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (-1 * y, x - offset, z)
        elif alignment_num == 3:
            scanner = Scanner([(-1 * x - offset, y, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (-1 * x - offset, y, z)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    elif offset_axis == "y":
        if alignment_num == 1:
            scanner = Scanner([(y - offset, -1 * x, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (y - offset, -1 * x, z)
        elif alignment_num == 2:
            scanner = Scanner([(x, y - offset, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, y - offset, z)
        elif alignment_num == 3:
            scanner = Scanner([(x, y - offset, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, y - offset, z)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    elif offset_axis == "-y":
        if alignment_num == 1:
            scanner = Scanner([(-1 * y - offset, x, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (-1 * y - offset, x, z)
        elif alignment_num == 2:
            if hold_axis == "z":
                scanner = Scanner([(-1 * x, -1 * y - offset, z) for x, y, z in scanner.beacons], scanner.origin)
                x, y, z = scanner.origin
                scanner.origin = (-1 * x, -1 * y - offset, z)
            elif hold_axis == "x":
                print("HOLD AXIS:", hold_axis)
                scanner = Scanner([(x, -1 * y - offset, -1 * z) for x, y, z in scanner.beacons], scanner.origin)
                x, y, z = scanner.origin
                scanner.origin = (x, -1 * y - offset, -1 * z)
            else:
                scanner = Scanner([(x, y - offset, z) for x, y, z in scanner.beacons], scanner.origin)
                x, y, z = scanner.origin
                scanner.origin = (x, y - offset, z)
                print(f"GOT {hold_axis} HOLD AXIS FOR -Y OFFSET AXIS!")
        elif alignment_num == 3:
            scanner = Scanner([(x, -1 * y - offset, z) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, -1 * y - offset, z)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    elif offset_axis == "z":
        if alignment_num == 1:
            scanner = Scanner([(z - offset, y, -1 * x) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (z - offset, y, -1 * x)
        elif alignment_num == 2:
            scanner = Scanner([(x, z - offset, -1 * y) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, z - offset, -1 * y)
        elif alignment_num == 3:
            scanner = Scanner([(x, y, z - offset) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, y, z - offset)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    elif offset_axis == "-z":
        if alignment_num == 1:
            scanner = Scanner([(-1 * z - offset, y, x) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (-1 * z - offset, y, x)
        elif alignment_num == 2:
            scanner = Scanner([(x, -1 * z - offset, y) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, -1 * z - offset, y)
        elif alignment_num == 3:
            scanner = Scanner([(x, y, -1 * z - offset) for x, y, z in scanner.beacons], scanner.origin)
            x, y, z = scanner.origin
            scanner.origin = (x, y, -1 * z - offset)
        else:
            raise ValueError(f"Unknown alignment number {alignment_num}")
    else:
        raise ValueError(f"Unknown axis {offset_axis}")
    return scanner


def overlap_success(ref_scanner: Scanner, new_scanner: Scanner) -> bool:
    return len(set(ref_scanner.beacons) & set(new_scanner.beacons)) >= 12

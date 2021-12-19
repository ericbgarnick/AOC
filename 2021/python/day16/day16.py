import re
from sys import argv
from typing import Optional, Callable


class Packet:
    VERSION_BITS = 3
    TYPE_ID_BITS = 3

    TYPE_0_LENGTH = 15
    TYPE_1_LENGTH = 11

    def __init__(self, as_hex: Optional[str] = None, as_bin: Optional[str] = None):
        assert as_hex or as_bin
        self.hex_packet = as_hex
        self.bin_packet = as_bin
        self.set_bin()
        self.version: Optional[int] = None
        self.type_id: Optional[int] = None
        self.length: Optional[int] = None
        self.subpackets = []
        self.value = self.parse()

    def set_bin(self):
        """
        Set self.bin_packet, converting self.hex_packet to binary.

        Ensure leading zeroes are included correctly.
        """
        if self.bin_packet:
            return
        naive_bin = format(int(self.hex_packet, 16), "b")
        padding_len = (4 - len(naive_bin) % 4) % 4
        leading_hex_zeroes = re.match(r"0+", self.hex_packet)
        if leading_hex_zeroes is not None:
            num_leading_zeroes = len(leading_hex_zeroes.group())
            leading_bin_zeroes = "".join(["0000" for _ in range(num_leading_zeroes)])
        else:
            leading_bin_zeroes = ""
        leading_bin_zeroes += "".join(["0" for _ in range(padding_len)])
        self.bin_packet = leading_bin_zeroes + naive_bin

    def parse(self) -> int:
        """
        Return total value for this Packet,
        as determined by the combination of all subpackets.
        """
        self.parse_header()
        if self.type_id == 4:
            return self.parse_literal()
        else:
            self.parse_operator()
            if self.type_id == 0:
                return sum(sp.value for sp in self.subpackets)
            elif self.type_id == 1:
                value = 1
                for sp in self.subpackets:
                    value *= sp.value
                return value
            elif self.type_id == 2:
                return min(sp.value for sp in self.subpackets)
            elif self.type_id == 3:
                return max(sp.value for sp in self.subpackets)
            elif self.type_id == 5:
                return self.subpacket_comparison_value(int.__gt__)
            elif self.type_id == 6:
                return self.subpacket_comparison_value(int.__lt__)
            elif self.type_id == 7:
                return self.subpacket_comparison_value(int.__eq__)
            else:
                raise ValueError(self.type_id)

    def subpacket_comparison_value(self, comparison: Callable) -> int:
        if comparison(self.subpackets[0].value, self.subpackets[1].value):
            return 1
        else:
            return 0

    def parse_header(self):
        self.version: Optional[int] = int(
            self.bin_packet[:self.VERSION_BITS], 2
        )
        self.type_id: Optional[int] = int(
            self.bin_packet[self.VERSION_BITS:self.VERSION_BITS + self.TYPE_ID_BITS], 2
        )

    def parse_literal(self) -> int:
        """Return the value for a literal packet."""
        bits = []
        section_length = 4
        prefix_idx = self.VERSION_BITS + self.TYPE_ID_BITS
        value_start_idx = prefix_idx + 1
        while self.bin_packet[prefix_idx] == "1":
            bits += list(self.bin_packet[value_start_idx: value_start_idx + section_length])
            prefix_idx = value_start_idx + section_length
            value_start_idx = prefix_idx + 1
        value_end_idx = value_start_idx + section_length
        bits += list(self.bin_packet[value_start_idx: value_end_idx])
        self.length = value_end_idx
        return int("".join(bits), 2)

    def parse_operator(self):
        length_type_id_idx = self.VERSION_BITS + self.TYPE_ID_BITS
        length_type_id = self.bin_packet[length_type_id_idx]
        length_start_idx = length_type_id_idx + 1
        if length_type_id == "0":
            length_end_idx = length_start_idx + self.TYPE_0_LENGTH
            subpackets_length = int(self.bin_packet[length_start_idx:length_end_idx], 2)
            subpackets_raw = self.bin_packet[length_end_idx:length_end_idx + subpackets_length]
            while sum(sp.length for sp in self.subpackets) < subpackets_length:
                new_subpacket = Packet(as_bin=subpackets_raw)
                subpackets_raw = subpackets_raw[new_subpacket.length:]
                self.subpackets.append(new_subpacket)
            self.length = length_end_idx + subpackets_length
        else:
            length_end_idx = length_start_idx + self.TYPE_1_LENGTH
            num_subpackets = int(self.bin_packet[length_start_idx:length_end_idx], 2)
            subpackets_raw = self.bin_packet[length_end_idx:]
            while len(self.subpackets) < num_subpackets:
                new_subpacket = Packet(as_bin=subpackets_raw)
                subpackets_raw = subpackets_raw[new_subpacket.length:]
                self.subpackets.append(new_subpacket)
            prefix_len = self.VERSION_BITS + self.TYPE_ID_BITS + 1 + self.TYPE_1_LENGTH
            self.length = prefix_len + sum(sp.length for sp in self.subpackets)


def parse_input(filename: str) -> Packet:
    return Packet(as_hex=open(filename, "r").read().strip())


def part1(packet: Packet) -> int:
    """Return the sum of version numbers for packet + all nested subpackets."""
    return sum_versions(packet)


def sum_versions(packet: Packet, total: int = 0) -> int:
    total += sum(sum_versions(sp, total) for sp in packet.subpackets)
    total += packet.version
    return total


def part2(packet: Packet) -> int:
    """Return the value for packet, calculated from all nested subpackets."""
    return packet.value


def main():
    try:
        input_file = argv[1]
        cave_map = parse_input(input_file)
        print("PART 1:", part1(cave_map))
        print("PART 2:", part2(cave_map))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

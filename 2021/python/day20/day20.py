import re
from sys import argv
from typing import List


class ScannerImage:
    SYMBOL_VALUES = {".": "0", "#": "1"}
    SWAP = {".": "#", "#": "."}

    def __init__(self, image: List[str], image_width: int, algorithm: List[str]):
        self.image = image
        self.width = image_width
        self.algorithm = algorithm
        self.void_value = "."

    def __str__(self) -> str:
        rows = []
        for row_num in range(len(self.image) // self.width):
            row_start_idx = row_num * self.width
            rows.append(self.image[row_start_idx:row_start_idx + self.width])
        return "\n".join("".join(row) for row in rows)

    def enhance(self):
        self.image = self.create_new_image_base()
        self.width += 2
        temp_image = self.image[:]
        for idx in range(len(self.image)):
            alg_idx = self.get_block_value(idx)
            temp_image[idx] = self.algorithm[alg_idx]
        self.image = temp_image
        is_off_turns_on = self.void_value == "." and self.algorithm[0] == "#"
        is_on_turns_off = self.void_value == "#" and self.algorithm[-1] == "."
        if is_off_turns_on or is_on_turns_off:
            self.void_value = ScannerImage.SWAP[self.void_value]

    def create_new_image_base(self) -> List[str]:
        new_width = self.width + 2
        new_image = [self.void_value for _ in range(new_width)]
        for chunk_start_row in range(len(self.image) // self.width):
            chunk_start_idx = chunk_start_row * self.width
            new_image += (
                    [self.void_value]
                    + self.image[chunk_start_idx:chunk_start_idx + self.width]
                    + [self.void_value]
            )
        new_image += [self.void_value for _ in range(new_width)]
        return new_image

    def get_block_value(self, center_idx: int) -> int:
        top_row = self.get_top_row(center_idx)
        middle_row = self.get_middle_row(center_idx)
        bottom_row = self.get_bottom_row(center_idx)
        pixels = top_row + middle_row + bottom_row
        bin_value = "".join([ScannerImage.SYMBOL_VALUES[val] for val in pixels])
        return int(bin_value, 2)

    def get_top_row(self, center_idx: int) -> List[str]:
        row = [self.void_value, self.void_value, self.void_value]
        if center_idx >= self.width:
            row[1] = self.image[center_idx - self.width]
            if center_idx % self.width == 0:
                row[2] = self.image[center_idx - self.width + 1]
            elif (center_idx + 1) % self.width == 0:
                row[0] = self.image[center_idx - self.width - 1]
            else:
                row[0] = self.image[center_idx - self.width - 1]
                row[2] = self.image[center_idx - self.width + 1]
        return row

    def get_middle_row(self, center_idx: int) -> List[str]:
        row = [self.void_value, self.image[center_idx], self.void_value]
        if center_idx % self.width != 0:
            row[0] = self.image[center_idx - 1]
        if (center_idx + 1) % self.width != 0:
            row[2] = self.image[center_idx + 1]
        return row

    def get_bottom_row(self, center_idx: int) -> List[str]:
        row = [self.void_value, self.void_value, self.void_value]
        if center_idx < len(self.image) - self.width:
            row[1] = self.image[center_idx + self.width]
            if center_idx % self.width == 0:
                row[2] = self.image[center_idx + self.width + 1]
            elif (center_idx + 1) % self.width == 0:
                row[0] = self.image[center_idx + self.width - 1]
            else:
                row[0] = self.image[center_idx + self.width - 1]
                row[2] = self.image[center_idx + self.width + 1]
        return row

    @property
    def light_count(self) -> int:
        return sum(int(ScannerImage.SYMBOL_VALUES[pixel]) for pixel in self.image)


def parse_input(filename: str) -> ScannerImage:
    with open(filename, "r") as f_in:
        algorithm = list(next(f_in).strip())
        _ = next(f_in)
        first_row = next(f_in).strip()
        image = list(first_row) + list(re.sub(r"\n", "", f_in.read()))
    return ScannerImage(image, len(first_row), algorithm)


def part1(scanner_image: ScannerImage) -> int:
    """Return the number of lighted points after enhancing scanner_image twice."""
    enhance_n_times(scanner_image, 2)
    return scanner_image.light_count


def part2(scanner_image: ScannerImage) -> int:
    """Return the number of lighted points after enhancing scanner_image 50 times."""
    enhance_n_times(scanner_image, 50)
    return scanner_image.light_count


def enhance_n_times(scanner_image: ScannerImage, n: int):
    for _ in range(n):
        scanner_image.enhance()


def main():
    try:
        input_file = argv[1]
    except IndexError:
        print("Enter path to data file!")
        return
    scanner_image = parse_input(input_file)
    print("PART 1:", part1(scanner_image))
    scanner_image = parse_input(input_file)
    print("PART 2:", part2(scanner_image))


if __name__ == "__main__":
    main()

import re
from sys import argv
from typing import List, Tuple

Transparency = List[int]


class InstructionManual:
    """
    A class to represent and fold a transparency sheet with
    dots in a grid pattern, and instructions on how to fold
    the transparency sheet.
    """
    BLANK = "0"
    DOT = "1"
    PALETTE = {BLANK: " ", DOT: "#"}

    def __init__(
            self,
            transparency_sheet: Transparency,
            fold_instructions: List[Tuple[str, int]],
            width: int,
    ):
        self.transparency_sheet = transparency_sheet
        self.fold_instructions = fold_instructions
        self.width = width

    def __str__(self) -> str:
        bin_sheet = [
            format(row, f"0{self.width}b")
            for row in self.transparency_sheet
        ]
        pixel_sheet = [
            [self.PALETTE[bit] for bit in row]
            for row in bin_sheet
        ]
        return "\n".join(["".join(row) for row in pixel_sheet])

    def fold(self, axis: str, value: int):
        """Apply vertical or horizontal fold to self.transparency_sheet."""
        if axis == "y":
            self._fold_up(value)
        else:
            self._fold_back(value)

    def _fold_up(self, fold_row: int):
        """Apply a vertical fold at row index fold_row."""
        for offset in range(1, len(self.transparency_sheet)):
            if offset <= fold_row:
                copy_row = self.transparency_sheet[fold_row + offset]
                self.transparency_sheet[fold_row - offset] |= copy_row
            else:
                overhang = self.transparency_sheet[-1:fold_row + offset - 1:-1]
                self.transparency_sheet = overhang + self.transparency_sheet[:fold_row]
                break
        self.transparency_sheet = self.transparency_sheet[:fold_row]

    def _fold_back(self, fold_col: int):
        """
        Apply a horizontal fold at col index fold_col.

        Side effect: update self.width.
        """
        new_width = self.width
        for r, row in enumerate(self.transparency_sheet):
            bin_row = list(format(row, f"0{self.width}b"))
            left = bin_row[:fold_col]
            right = bin_row[fold_col + 1:]
            while len(left) < len(right):
                left.insert(0, self.BLANK)
            while len(right) < len(left):
                right.append(self.BLANK)
            right.reverse()
            new_width = len(right)
            new_val = int("".join(left), 2) | int("".join(right), 2)
            self.transparency_sheet[r] = new_val
        self.width = new_width


def parse_input(filename: str) -> InstructionManual:
    max_x = max_y = 0
    points = []
    instructions = []
    for line in open(filename, "r"):
        if re.match(r"\d+,\d+", line) is not None:
            x, y = [int(val) for val in line.strip().split(",")]
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            points.append((x, y))
        elif line.startswith("fold"):
            axis, value = line.strip().split()[-1].split("=")
            instructions.append((axis, int(value)))
    return InstructionManual(create_sheet(points, max_x, max_y), instructions, max_x + 1)


def create_sheet(
        points: List[Tuple[int, int]], max_x: int, max_y: int
) -> Transparency:
    """Return a Transparency sheet for the given points."""
    sheet = [
        [InstructionManual.BLANK for _ in range(max_x + 1)]
        for _ in range(max_y + 1)
    ]
    for col, row in points:
        sheet[row][col] = InstructionManual.DOT
    return [int("".join(row), 2) for row in sheet]


def part1(instruction_manual: InstructionManual) -> int:
    """
    Return the number of dots visible in the instruction manual
    transparency sheet after applying the first fold.
    """
    instruction_manual.fold(*instruction_manual.fold_instructions[0])
    return sum(sum_bits(val) for val in instruction_manual.transparency_sheet)


def sum_bits(num: int) -> int:
    """Return the sum of bits in the binary representation of num."""
    return sum(int(bit) for bit in format(num, "b"))


def part2(instruction_manual: InstructionManual) -> str:
    """
    Return the image produced by applying all the folds
    to the instruction manual transparency sheet.
    """
    for axis, value in instruction_manual.fold_instructions:
        instruction_manual.fold(axis, value)
    return str(instruction_manual)


def main():
    try:
        input_file = argv[1]
        manual = parse_input(input_file)
        print(f"PART 1: {part1(manual)}")
        print(f"PART 2:\n{part2(manual)}")
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

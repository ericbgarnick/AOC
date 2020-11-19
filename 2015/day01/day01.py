from sys import argv


def part1(filename: str) -> int:
    with open(filename, "r") as f_in:
        parens = f_in.read().strip()
        return parens.count("(") - parens.count(")")


def part2(filename: str) -> int:
    conversion = {"(": 1, ")": -1}
    with open(filename, "r") as f_in:
        parens = f_in.read().strip()
        floor = 0
        for i, symbol in enumerate(parens):
            floor += conversion[symbol]
            if floor == -1:
                return i + 1


if __name__ == "__main__":
    try:
        file = argv[1]
        print("PART 1:", part1(file))
        print("PART 2:", part2(file))
    except IndexError:
        print("Must enter path to input data file!")

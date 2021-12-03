from typing import List
from sys import argv


def parse_input(filename: str) -> List[str]:
    return [line.strip() for line in open(filename, "r")]


def part1(diagnostics: List[str]) -> int:
    gamma_count = [0 for _ in range(len(diagnostics[0]))]
    for number in diagnostics:
        for i, bit in enumerate(number):
            if bit == "1":
                gamma_count[i] += 1
            else:
                gamma_count[i] -= 1
    gamma = []
    epsilon = []
    for c in gamma_count:
        if c > 0:
            gamma.append("1")
            epsilon.append("0")
        elif c < 0:
            gamma.append("0")
            epsilon.append("1")

    gamma = "".join(gamma)
    epsilon = "".join(epsilon)
    return int(gamma, 2) * int(epsilon, 2)


def part2(diagnostics: List[str]) -> int:
    o_gen_rating = find_rating(diagnostics, "o-gen")
    co2_scrub_rating = find_rating(diagnostics, "co2-scrub")
    return int(o_gen_rating, 2) * int(co2_scrub_rating, 2)


def find_rating(diagnostics: List[str], rating_type: str) -> str:
    if rating_type == "o-gen":
        comparison = int.__ge__
    elif rating_type == "co2-scrub":
        comparison = int.__lt__
    else:
        raise ValueError(f"Unknown rating_type: {rating_type}")
    diagnostics = [num for num in diagnostics]
    for i in range(len(diagnostics[0])):
        ones = []
        zeroes = []
        for number in diagnostics:
            if number[i] == "1":
                ones.append(number)
            else:
                zeroes.append(number)
        if comparison(len(ones), len(zeroes)):
            diagnostics = ones
        else:
            diagnostics = zeroes
        if len(diagnostics) == 1:
            return diagnostics[0]


def main():
    try:
        input_file = argv[1]
        depths = parse_input(input_file)
        print("PART 1:", part1(depths))
        print("PART 2:", part2(depths))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

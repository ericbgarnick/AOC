"""
Part 1 answer: 72070
Part 2 answer: 211805
"""
from y2022.python.shared import get_data_file_path


def main():
    tallies = tally_calories()
    print("PART 1:", tallies[-1])
    print("PART 2:", sum(tallies[-3:]))


def tally_calories() -> list[int]:
    tallies = []
    elf_total = 0
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        for line in f_in:
            line = line.strip()
            if line:
                elf_total += int(line)
            else:
                tallies.append(elf_total)
                elf_total = 0
    tallies.append(elf_total)
    return sorted(tallies)


if __name__ == "__main__":
    main()

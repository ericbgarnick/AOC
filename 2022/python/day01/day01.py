import os
from typing import List

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = "/".join(DIR_PATH.split("/")[:-2] + ["data"])


def main():
    tallies = tally_calories()
    print("PART 1:", tallies[-1])
    print("PART 2:", sum(tallies[-3:]))


def tally_calories() -> List[int]:
    tallies = []
    elf_total = 0
    input_data_file = DATA_DIR + "/01.txt"
    with open(input_data_file, "r") as f_in:
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

import re
from sys import argv


def polymer_length(polymer: str, part_num: int):
    if part_num == 1:
        print("Part 1")
        print("Reduced length:", reduce_polymer(polymer))
    elif part_num == 2:
        print("Part 2")
        print("Shortest polymer length:", shortest_polymer(polymer))


def reduce_polymer(polymer: str) -> int:
    original = list(polymer)
    reduced = []
    while len(original) != len(reduced):
        i = 0
        while i < len(original) - 1:
            if opposites(original[i], original[i + 1]):
                i += 2
            else:
                reduced.append(original[i])
                i += 1
            if i == len(original) - 1:
                reduced.append(original[i])
        if len(original) != len(reduced):
            original = [x for x in reduced]
            reduced = []
    return len(original)


def opposites(a: str, b: str) -> bool:
    return a != b and a.lower() == b.lower()


def shortest_polymer(polymer: str) -> int:
    alphabet = {chr(c): 0 for c in range(65, 91)}

    for letter in alphabet:
        subbed = re.sub(letter, '', polymer, flags=re.I)
        alphabet[letter] = reduce_polymer(subbed)

    return min(alphabet.values())


if __name__ == '__main__':
    data_file = argv[1]
    data_line = open(data_file, 'r').read().strip()
    part = int(argv[2])

    polymer_length(data_line, part)


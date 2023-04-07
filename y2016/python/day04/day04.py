"""
Part 1 answer: 278221
Part 2 answer:
"""
import re
from collections import Counter, defaultdict

from y2016.python.shared import get_data_file_path


def load_rooms() -> list[str]:
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        return [line.strip() for line in f_in]



def is_valid_room(room: str) -> bool:
    room_name, checksum = re.split(r"\d+", room)
    letters_to_counts = Counter(re.findall(r"[a-z]", room_name))
    counts_to_letters: dict[int, list[str]] = defaultdict(list)
    for letter, count in letters_to_counts.items():
        counts_to_letters[count].append(letter)

    for letter in checksum.strip("[]"):
        try:
            count = letters_to_counts.pop(letter)
        except KeyError:
            return False
        if count != max(counts_to_letters.keys()):
            return False
        tied_letters = counts_to_letters.pop(count)
        if letter != sorted(tied_letters)[0]:
            return False
        if len(tied_letters) > 1:
            counts_to_letters[count] = sorted(tied_letters)[1:]
    return True


def main():
    rooms = load_rooms()
    valid_room_count = sum(
        int(re.search(r"\d+", room).group())
        for room in rooms if is_valid_room(room)
    )
    print("PART 1:", valid_room_count)


if __name__ == "__main__":
    main()

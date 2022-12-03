import re
from sys import argv
from typing import List, Dict, Tuple


def parse_input(filename: str) -> Dict[str, Dict[str, int]]:
    preferences = {}
    for line in open(filename, "r"):
        subject, preference = line.strip().split(" would ")
        neighbor, score = parse_preference(preference)
        try:
            preferences[subject][neighbor] = score
        except KeyError:
            preferences[subject] = {neighbor: score}
    return preferences


def parse_preference(preference: str) -> Tuple[str, int]:
    neighbor = preference.strip(".").rsplit(maxsplit=1)[-1]
    score = int(re.search(r"\d+", preference).group())
    if preference.startswith("lose"):
        score *= -1
    return neighbor, score


def add_self(all_preferences: Dict[str, Dict[str, int]]):
    attendees = [name for name in all_preferences.keys()]
    for preferences in all_preferences.values():
        preferences["Host"] = 0
    all_preferences["Host"] = {attendee: 0 for attendee in attendees}


def score_arrangements(
        preferences: Dict[str, Dict[str, int]],
        cur_arrangement: List[str],
        results: Dict[int, List[str]]
) -> Dict[int, List[str]]:
    if len(cur_arrangement) == len(preferences):
        results[calc_happiness(preferences, cur_arrangement)] = [name for name in cur_arrangement]
    else:
        remaining = list(set(preferences.keys()) - set(cur_arrangement))
        for name in remaining:
            score_arrangements(preferences, cur_arrangement + [name], results)
    return results


def calc_happiness(preferences: Dict[str, Dict[str, int]], seating: List[str]) -> int:
    total_happiness = 0
    for pos, name in enumerate(seating):
        num_people = len(seating)
        # Add prior person
        prior_name = seating[pos - 1]
        total_happiness += preferences[name][prior_name]
        # Add next person
        next_name = seating[(pos + 1) % num_people]
        total_happiness += preferences[name][next_name]
    return total_happiness


if __name__ == "__main__":
    test_preferences = {
        "Alice": {"Bob": 54, "Carol": 79, "David": -2},
        "Bob": {"Alice": 83, "Carol": -7, "David": -63},
        "Carol": {"Alice": -62, "Bob": 60, "David": 55},
        "David": {"Alice": 46, "Bob": -7, "Carol": 41},
    }
    try:
        input_file = argv[1]
        seating_preferences = parse_input(input_file)
        print("PART 1", max(score_arrangements(seating_preferences, [], {}).keys()))
        add_self(seating_preferences)
        print("PART 2", max(score_arrangements(seating_preferences, [], {}).keys()))
    except IndexError:
        print("Enter path to data file!")

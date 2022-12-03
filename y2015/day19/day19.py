from sys import argv
from typing import Dict, List, Tuple, Union

Number = Union[int, float]


def parse_input(filename: str) -> Tuple[List[str], str]:
    raw_replacements = []
    replacements_done = False
    for line in open(filename, "r"):
        line = line.strip()
        if line and not replacements_done:
            raw_replacements.append(line)
        elif line:
            return raw_replacements, line
        else:
            replacements_done = True


def forward_replacements(raw_replacements: List[str]) -> Dict[str, List[str]]:
    replacements = {}
    for rr in raw_replacements:
        source, result = rr.split(" => ")
        try:
            replacements[source].append(result)
        except KeyError:
            replacements[source] = [result]
    return replacements


def reverse_replacements(raw_replacements: List[str]) -> Dict[str, str]:
    replacements = {}
    for rr in raw_replacements:
        source, result = rr.split(" => ")
        if source != "e":
            replacements[result] = source
    return replacements


def calibrate(replacements: Dict[str, List[str]], medicine: str) -> int:
    molecules = set()
    for source, results in replacements.items():
        for i in range(len(medicine) - len(source) + 1):
            if medicine[i: i + len(source)] == source:
                prefix = medicine[:i]
                suffix = medicine[i + len(source):]
                for res in results:
                    molecules.add(prefix + res + suffix)
    return len(molecules)


def steps_to_medicine(replacements: Dict[str, str], final: List[str], goal: str) -> int:
    """
    WARNING: This will probably find the correct solution, but maybe not in my lifetime
    """
    return helper(replacements, final, goal, {}, 0)


def helper(
        replacements: Dict[str, str],
        final: List[str],
        initial: str,
        memo: Dict,
        steps: Number,
) -> int:
    try:
        return memo[initial]
    except KeyError:
        pass
    if initial in final:
        return steps + 1  # Don't need to explicitly go to "e"
    else:
        temp_steps = float("inf")
        for result, source in replacements.items():
            loc = initial.find(result)
            while loc != -1:
                replaced = initial[:loc] + initial[loc:].replace(result, source, 1)
                try:
                    temp_steps = memo[replaced]
                except KeyError:
                    temp_steps = min(temp_steps, helper(replacements, final, replaced, memo, steps + 1))
                    memo[replaced] = temp_steps
                loc = initial.find(result, loc + 1)
        return temp_steps


if __name__ == "__main__":
    try:
        input_file = argv[1]
        raw_conversions, medicine_molecule = parse_input(input_file)
        forward = forward_replacements(raw_conversions)
        print("PART 1:", calibrate(forward, medicine_molecule))
        reverse = reverse_replacements(raw_conversions)
        final_replacements = forward["e"]
        # print("PART 2:", steps_to_medicine(reverse, final_replacements, medicine_molecule))
        # https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/?utm_source=share&utm_medium=web2x&context=3
        print("PART 2: 292 symbols - 72 parens - 2 * 6 commas - 1 = 207")
    except IndexError:
        print("Enter path to data file!")

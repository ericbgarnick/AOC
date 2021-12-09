from collections import defaultdict, namedtuple
from typing import List, Dict, Set
from sys import argv


NUMBER_CONFIGS = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}

NUM_CONFIG_LENGTHS = {
    num: len(config) for num, config in NUMBER_CONFIGS.items()
}


Signal = namedtuple("Signal", ["inputs", "outputs"])


def parse_input(filename: str) -> List[Signal]:
    signals = []
    for line in open(filename, "r"):
        inputs, outputs = [section.strip().split() for section in line.strip().split("|")]
        signals.append(Signal(inputs, outputs))
    return signals


def part1(signals: List[Signal]) -> int:
    """
    Return the total number of unique-length configurations are in all signal outputs.
    """
    config_length_counts = defaultdict(int)
    for length in NUM_CONFIG_LENGTHS.values():
        config_length_counts[length] += 1
    unique_config_lengths = {
        length for length in NUM_CONFIG_LENGTHS.values()
        if config_length_counts[length] == 1
    }
    count = 0
    for inputs, outputs in signals:
        for o in outputs:
            if len(o) in unique_config_lengths:
                count += 1
    return count


def part2(signals: List[Signal]) -> int:
    """Return the sum of all signal output values."""
    total = 0
    for inputs, outputs in signals:
        mapping = determine_signal_mapping(inputs)
        total += int("".join([signal_to_int(o, mapping) for o in outputs]))
    return total


def determine_signal_mapping(signals: List[str]) -> Dict:
    """Return a mapping of scrambled values to the original values in the display."""
    scrambled_configs = {}  # number to config
    forward_mapping = {}  # scrambled value to standard value
    reverse_mapping = {}  # standard value to scrambled value
    find_unique_configs(signals, scrambled_configs)

    map_pos_a(scrambled_configs, forward_mapping, reverse_mapping)

    find_5(signals, scrambled_configs)

    map_pos_g(scrambled_configs, forward_mapping, reverse_mapping)
    map_pos_f(scrambled_configs, forward_mapping, reverse_mapping)
    map_pos_c(scrambled_configs, forward_mapping, reverse_mapping)

    find_2_3(signals, scrambled_configs, reverse_mapping)

    map_pos(scrambled_configs, forward_mapping, reverse_mapping, "d", 3)
    map_pos(scrambled_configs, forward_mapping, reverse_mapping, "e", 2)
    map_pos(scrambled_configs, forward_mapping, reverse_mapping, "b", 5)
    return forward_mapping


def find_unique_configs(signals: List[str], configs: Dict[int, Set[str]]):
    """
    Populate scrambled configs for 1, 4, 7, 8.

    These numbers have unique config lengths.
    """
    unique_nums = (1, 4, 7, 8)
    for s in signals:
        for num in unique_nums:
            if len(s) == NUM_CONFIG_LENGTHS[num]:
                configs[num] = set(s)
                break
        if len(configs) == len(unique_nums):
            return


def map_pos_a(
        configs: Dict[int, Set[str]],
        f_mapping: Dict[str, str],
        r_mapping: Dict[str, str],
):
    top = (configs[7] - configs[1]).pop()
    f_mapping[top] = "a"
    r_mapping["a"] = top


def find_5(signals: List[str], configs: Dict[int, Set[str]]):
    """
    Add the scrambled config for 5 to configs.

    5 is the only config of 2, 3, 5 (length 5)
    that overlaps with the extras from 4.
    """
    extras_from_4 = configs[4] - configs[1]
    two_three_five = [set(s) for s in signals if len(s) == NUM_CONFIG_LENGTHS[2]]
    for config in two_three_five:
        if config & extras_from_4 == extras_from_4:
            configs[5] = config
            return


def map_pos_g(
        configs: Dict[int, Set[str]],
        f_mapping: Dict[str, str],
        r_mapping: Dict[str, str],
):
    four_seven_config = configs[4] | configs[7]
    bottom = (configs[5] - four_seven_config).pop()
    f_mapping[bottom] = "g"
    r_mapping["g"] = bottom


def map_pos_f(
        configs: Dict[int, Set[str]],
        f_mapping: Dict[str, str],
        r_mapping: Dict[str, str],
):
    bottom_right = (configs[5] & configs[1]).pop()
    f_mapping[bottom_right] = "f"
    r_mapping["f"] = bottom_right


def map_pos_c(
        configs: Dict[int, Set[str]],
        f_mapping: Dict[str, str],
        r_mapping: Dict[str, str],
):
    top_right = (configs[1] - configs[5]).pop()
    f_mapping[top_right] = "c"
    r_mapping["c"] = top_right


def find_2_3(
        signals: List[str],
        configs: Dict[int, Set[str]],
        r_mapping: Dict[str, str],
):
    """
    Add the scrambled config for 2 and 3 to configs.

    3 is the config from 2, 3 that has the "f" value.
    """
    two_three = [
        set(s) for s in signals
        if len(s) == NUM_CONFIG_LENGTHS[2] and set(s) != configs[5]
    ]
    for config in two_three:
        if r_mapping["f"] in config:
            configs[3] = config
        else:
            configs[2] = config


def map_pos(
        configs: Dict[int, Set[str]],
        f_mapping: Dict[str, str],
        r_mapping: Dict[str, str],
        letter: str,
        number: int,
):
    config_position = (configs[number] - set(f_mapping.keys())).pop()
    f_mapping[config_position] = letter
    r_mapping[letter] = config_position


def signal_to_int(output_signal: str, mapping: Dict[str, str]) -> str:
    """
    Return the integer represented by output_signal, unscrambled using mapping.

    output signals can have values in any order, so value is translated
    as an unordered set for comparison with NUMBER_CONFIGS items.
    """
    translated = {mapping[letter] for letter in output_signal}
    return next(str(num) for num, config in NUMBER_CONFIGS.items() if config == translated)


def main():
    try:
        input_file = argv[1]
        signals = parse_input(input_file)
        print("PART 1:", part1(signals))
        print("PART 2:", part2(signals))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()

import sys
from typing import List

PATTERN = [0, 1, 0, -1]
NUM_CYCLES = 100
DIGITS_TO_RETURN = 8
INPUT_MULTIPLE = 10000
MESSAGE_OFFSET_LEN = 7


def day16_part1(puzzle_data: List[int]) -> str:
    input_signal = puzzle_data
    for _ in range(NUM_CYCLES):
        input_signal = _calc_whole_fft_phase(input_signal)
    return ''.join(str(d) for d in input_signal[:DIGITS_TO_RETURN])


def day16_part2(puzzle_data: List[int], digits_to_compute: int) -> str:
    input_signal = _create_input_signal(puzzle_data, digits_to_compute)
    for _ in range(NUM_CYCLES):
        input_signal = _calc_part_fft_phase(input_signal)
    return ''.join(str(d) for d in input_signal[:DIGITS_TO_RETURN])


# - Part 1 helpers - #
def _calc_whole_fft_phase(input_signal: List[int]) -> List[int]:
    result = []
    for pos in range(1, len(input_signal) + 1):
        pattern_for_el = _construct_pattern_for_pos(pos)
        pattern_len = len(pattern_for_el)
        new_val = 0
        for i, el in enumerate(input_signal):
            # Skip the first idx the first time looping through pattern
            idx = i + 1
            factor = pattern_for_el[idx % pattern_len]
            new_val += el * factor
        result.append(abs(new_val) % 10)
    return result


def _construct_pattern_for_pos(pos: int) -> List[int]:
    pattern_for_el = []
    for p in PATTERN:
        pattern_for_el += [p for _ in range(pos)]
    return pattern_for_el


# - Part 2 helpers - #
def _calc_part_fft_phase(input_signal: List[int]) -> List[int]:
    result = []
    total = sum(input_signal)
    for i in range(len(input_signal)):
        if i:
            # No reduction for first digit (use the whole input signal)
            total -= input_signal[i - 1]
        result.append(total % 10)
    return result


def _create_input_signal(signal_segment: List[int],
                         relevant_signal_length: int) -> List[int]:
    """Create the section of input signal we care about for part 2 result"""
    multiple, remainder = divmod(relevant_signal_length, len(signal_segment))
    result = signal_segment[-1 * remainder:]
    for _ in range(multiple):
        result += signal_segment
    return result


if __name__ == '__main__':
    data_file = sys.argv[1]
    data_str = open(data_file, 'r').read().strip()
    data = [int(x) for x in data_str]
    message_offset = int(''.join([str(d) for d in data[:MESSAGE_OFFSET_LEN]]))
    digits = len(data) * INPUT_MULTIPLE - message_offset

    print(f"PART 1:\n{day16_part1(data)}")
    print(f"PART 2:\n{day16_part2(data, digits)}")

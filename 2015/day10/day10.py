import re
from sys import argv


def look_and_say(start_seq: str, iterations: int) -> str:
    cur_seq = start_seq
    while iterations:
        cur_seq = convert_fast(cur_seq)
        iterations -= 1
    return cur_seq


def convert_slow(seq: str) -> str:
    next_seq = ""
    while len(seq):
        prefix = re.search(r"^(\d)\1*", seq).group()
        prefix_len = len(prefix)
        seq, next_seq = seq[prefix_len:], next_seq + str(prefix_len) + prefix[0]
    return next_seq


def convert_fast(seq: str) -> str:
    """Convert number sequences to single-letter symbols,
    then convert symbols to new number sequences"""
    letter_to_next = {
        r"a": "11",
        r"b": "21",
        r"c": "31",
        r"d": "12",
        r"e": "22",
        r"f": "32",
        r"g": "13",
        r"h": "23",
        r"i": "33",
    }
    next_seq_ones = re.sub(r"1", "a", re.sub(r"11", "b", re.sub(r"111", "c", seq)))
    next_seq_twos = re.sub(r"2", "d", re.sub(r"22", "e", re.sub(r"222", "f", next_seq_ones)))
    next_seq = re.sub(r"3", "g", re.sub(r"33", "h", re.sub(r"333", "i", next_seq_twos)))
    for regex, code in letter_to_next.items():
        next_seq = re.sub(regex, code, next_seq)
    return next_seq


if __name__ == "__main__":
    try:
        num_iterations = int(argv[1])
        new_val = len(look_and_say("3113322113", num_iterations))
        print("SEQUENCE LENGTH:", new_val)
    except IndexError:
        print("Enter number of iterations!")

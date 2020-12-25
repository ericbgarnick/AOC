
# Real pub keys
PUB_KEY_1 = 2084668
PUB_KEY_2 = 3704642
# Sample pub keys
# PUB_KEY_1 = 5764801
# PUB_KEY_2 = 17807724

SUBJECT_NUMBER = 7
TRANSFORM_VALUE = 20201227


def find_loop_size(orig_pub_key: int) -> int:
    new_pub_key = 1
    loop_size = 0
    while new_pub_key != orig_pub_key:
        new_pub_key *= SUBJECT_NUMBER
        new_pub_key %= TRANSFORM_VALUE
        loop_size += 1
    return loop_size


def transform(pub_key: int, loop_size: int) -> int:
    encryption_key = 1
    for _ in range(loop_size):
        encryption_key *= pub_key
        encryption_key %= TRANSFORM_VALUE
    return encryption_key


if __name__ == "__main__":
    loop_size_1 = find_loop_size(PUB_KEY_1)
    print("PART 1:", transform(PUB_KEY_2, loop_size_1))

from hashlib import md5


def find_key(num_zeroes: int) -> int:
    secret = "iwrupvqb"
    digits = 0
    while True:
        hash_result = md5(f"{secret}{digits}".encode("utf8")).hexdigest()
        if hash_result.startswith("0" * num_zeroes):
            return digits
        else:
            digits += 1


if __name__ == "__main__":
    print("PART 1:", find_key(5))
    print("PART 2:", find_key(6))

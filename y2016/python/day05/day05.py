"""
Part 1 answer: d4cd2ee1
Part 2 answer: f2c730e5
"""
import hashlib


ROOM_ID = "ugkcyxxp".encode("utf-8")


def find_codes() -> tuple[str, str]:
    simple_code = []
    complex_code = ["" for _ in range(8)]
    index = 0
    while len(simple_code) < 8 or "" in complex_code:
        b_idx = str(index).encode("utf-8")
        hashed = hashlib.md5(ROOM_ID + b_idx).hexdigest()
        if hashed[:5] == "00000":
            if len(simple_code) < 8:
                code_char = hashed[5]
                print("NEXT SIMPLE CODE CHAR:", code_char)
                simple_code.append(code_char)
            if hashed[5].isdecimal() and int(hashed[5]) < len(complex_code):
                code_char_idx = int(hashed[5])
                if complex_code[code_char_idx] == "":
                    print(f"COMPLEX CODE CHAR AT IDX {code_char_idx}: {hashed[6]}")
                    complex_code[code_char_idx] = hashed[6]
        index += 1
    return "".join(simple_code), "".join(complex_code)


def main():
    simple_code, complex_code = find_codes()
    print("PART 1:", simple_code)
    print("PART 2:", complex_code)


if __name__ == "__main__":
    main()

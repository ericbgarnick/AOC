import re
from sys import argv
from typing import Dict

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL_FIELDS = {"cid"}


# == VALIDATORS == #
def valid_year(year: str, min_year: int, max_year: int) -> bool:
    return re.match(r"^\d{4}$", year) and min_year <= int(year) <= max_year


def valid_height(height: str) -> bool:
    min_cm, max_cm = 150, 193
    min_in, max_in = 59, 76
    if re.match(r"^\d{2,3}(cm|in)", height):
        height_val = int(height[:-2])
        if height.endswith("cm"):
            return min_cm <= height_val <= max_cm
        else:
            return min_in <= height_val <= max_in


def valid_hair(color: str) -> bool:
    return re.match(r"^#[0-9a-f]{6}$", color) is not None


def valid_eye(color: str) -> bool:
    return color in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def valid_pid(pid: str) -> bool:
    return re.match(r"^\d{9}$", pid) is not None


# == SOLUTION == #
def count_passports(filename: str, part_num: int) -> int:
    input_text = open(filename, "r").read()
    num_valid = 0
    for passport in input_text.split("\n\n"):
        fields = dict(field.split(":") for field in passport.split())
        if part_num == 1:
            num_valid += int(valid_field_names(fields))
        else:
            num_valid += int(valid_field_values(fields))

    return num_valid


def valid_field_names(fields: Dict[str, str]) -> bool:
    return not REQUIRED_FIELDS - set(fields.keys())


def valid_field_values(fields: Dict[str, str]) -> bool:
    year_ranges = {"byr": [1920, 2002], "iyr": [2010, 2020], "eyr": [2020, 2030]}
    validators = {
        "byr": valid_year,
        "iyr": valid_year,
        "eyr": valid_year,
        "hgt": valid_height,
        "hcl": valid_hair,
        "ecl": valid_eye,
        "pid": valid_pid,
    }
    for field_name, validator_fn in validators.items():
        try:
            value = fields[field_name]
            if field_name.endswith("yr"):
                yr_min, yr_max = year_ranges[field_name]
                valid = validator_fn(value, yr_min, yr_max)
            else:
                valid = validator_fn(value)
        except KeyError:
            valid = False
        if not valid:
            return False
    return True


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1:", count_passports(input_file, 1))
        print("PART 2:", count_passports(input_file, 2))
    except IndexError:
        print("Enter path to data file!")

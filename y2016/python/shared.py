import os
import re

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = "/".join(DIR_PATH.split("/")[:-1] + ["data"])


def get_data_file_path(filename: str, sample: bool = False) -> str:
    day_number = int(re.search(r"\d+", filename).group())
    if sample:
        return DATA_DIR + f"/{day_number:02}_sample.txt"
    else:
        return DATA_DIR + f"/{day_number:02}.txt"

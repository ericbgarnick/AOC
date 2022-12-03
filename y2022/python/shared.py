import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = "/".join(DIR_PATH.split("/")[:-1] + ["data"])


def get_data_file_path(day_number: int) -> str:
    return DATA_DIR + f"/{day_number:02}.txt"

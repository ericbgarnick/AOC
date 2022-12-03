from typing import List, Optional

from dance import Dance


class DanceMaster:
    def __init__(self, dancers: Optional[str]=None):
        start_code = 97
        alph_len = 16
        data = [chr(code_pt) for code_pt in
                range(start_code, start_code + alph_len)]
        dancers = dancers or data
        self.dance = Dance(dancers)

        self.current = None     # type: List[str]
        self.repeat = 0
        self.conversion = None  # type: List[int]
        self.conversion_factor = 0

    def find_repeat(self, instructions: str):

        count = 0

        while not count or self.dance.dancers != self.dance.original_list:
            self.dance.call_dance(instructions)
            count += 1
            if not count % 1000:
                print("{} Cycles".format(count))

        print("Repeat at {}".format(count))

    def find_conversion(self):
        result = [el for el in self.dance.dancers]
        self.conversion = [result.index(el) for el in
                           self.dance.original]

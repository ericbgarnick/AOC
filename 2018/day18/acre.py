

class Acre:
    OPEN = 1
    LUMBER = 10
    WOODED = 100

    TYPE_FOR_SYMBOL = {'.': OPEN, '#': LUMBER, '|': WOODED}
    NEXT_TYPE = {OPEN: WOODED, WOODED: LUMBER, LUMBER: OPEN}

    ALL_OUTCOMES = {OPEN: {}, LUMBER: {}, WOODED: {}}

    def __init__(self, acre_type: int):
        self.calc_all_outcomes()
        self.type = acre_type
        self.neighbors = set()
        self.next_type = None

    @classmethod
    def calc_all_outcomes(cls):
        corner_neighbors = 3
        edge_neighbors = 5
        mid_neighbors = 8
        for num_neighbors in [corner_neighbors, edge_neighbors, mid_neighbors]:
            cls.outcome_for_position(num_neighbors)

    @classmethod
    def outcome_for_position(cls, num_neighbors: int):
        for hundreds in range(num_neighbors + 1):
            for tens in range(num_neighbors + 1):
                for units in range(num_neighbors + 1):
                    if hundreds + tens + units == num_neighbors:
                        env = hundreds * 100 + tens * 10 + units
                        for acre_type in cls.ALL_OUTCOMES.keys():
                            cls.ALL_OUTCOMES[acre_type][env] = cls._convert(acre_type, env)

    @staticmethod
    def _open_conversion(environment: int) -> bool:
        return environment >= 300

    @staticmethod
    def _lumber_conversion(environment: int) -> bool:
        return environment % 100 < 10 or environment // 100 == 0

    @staticmethod
    def _wooded_conversion(environment: int) -> bool:
        return environment % 100 >= 30

    @classmethod
    def _convert(cls, acre_type: int, environment: int) -> int:
        conversion_func = {cls.OPEN: cls._open_conversion,
                           cls.LUMBER: cls._lumber_conversion,
                           cls.WOODED: cls._wooded_conversion}
        should_convert = conversion_func[acre_type](environment)
        return cls.NEXT_TYPE[acre_type] if should_convert else acre_type

    def calc_next_type(self):
        environment = sum(n.type for n in self.neighbors)
        self.next_type = self.ALL_OUTCOMES[self.type][environment]
        # self.next_type = self._convert(self.type, environment)

    def update_type(self):
        self.type = self.next_type

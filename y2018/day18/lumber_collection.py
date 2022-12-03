from typing import List

from acre import Acre


class LumberCollection:
    def __init__(self, area_map: List[str]):
        row_len = len(area_map[0])
        num_rows = len(area_map)
        self.collection_area = []  # type: List[Acre]
        self.populate_area(area_map)
        self.link_acres(row_len, num_rows)
        
    def populate_area(self, area_map: List[str]):
        for row in area_map:
            for acre in row:
                acre_type = Acre.TYPE_FOR_SYMBOL[acre]
                self.collection_area.append(Acre(acre_type))
                
    def link_acres(self, row_len: int, num_rows: int):
        for i, acre in enumerate(self.collection_area):
            if i % row_len:
                # W
                acre.neighbors.add(self.collection_area[i - 1])
                if i >= row_len:
                    # NW
                    acre.neighbors.add(self.collection_area[i - row_len - 1])
                    # N
                    acre.neighbors.add(self.collection_area[i - row_len])
                if i < row_len * (num_rows - 1):
                    # SW
                    acre.neighbors.add(self.collection_area[i + row_len - 1])
                    # S
                    acre.neighbors.add(self.collection_area[i + row_len])
            if i % row_len != row_len - 1:
                # E
                acre.neighbors.add(self.collection_area[i + 1])
                if i >= row_len:
                    # NE
                    acre.neighbors.add(self.collection_area[i - row_len + 1])
                    # N
                    acre.neighbors.add(self.collection_area[i - row_len])
                if i < row_len * (num_rows - 1):
                    # SE
                    acre.neighbors.add(self.collection_area[i + row_len + 1])
                    # S
                    acre.neighbors.add(self.collection_area[i + row_len])



import sys

from clay_map import ClayMap
from seepage import Seepage

if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, "r").readlines()]
    cm = ClayMap(data)
    seepage = Seepage(cm)
    seepage.run()
    print(f"Water seeps to {seepage.water_volume} spaces")

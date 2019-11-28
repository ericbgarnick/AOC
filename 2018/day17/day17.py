from sys import argv

from water_tracer import WaterTracer

if __name__ == '__main__':

    file_name = argv[1]
    data = open(file_name, 'r').readlines()
    water_tracer = WaterTracer(data)
    print("MOST LEFT:", water_tracer.clay_map.most_left)
    with open('clay_map.out', 'w') as clay_out:
        clay_out.write(str(water_tracer.clay_map))

    print("TOTAL VOLUME", water_tracer.trace())

    with open('water_map.out', 'w') as water_out:
        water_out.write(str(water_tracer))

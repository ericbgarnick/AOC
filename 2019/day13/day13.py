import sys

from arcade_cabinet import ArcadeCabinet

if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]

    cabinet = ArcadeCabinet()
    cabinet.run(data)
    block_type = ArcadeCabinet.BLOCK
    block_count = cabinet.tile_type_count(block_type)

    print(f"PART 1:\n{block_count} block-type tiles")


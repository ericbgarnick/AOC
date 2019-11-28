from cave import CaveSpot, Cave


class TestCave:
    SIMPLE_CAVE = ["####",
                   "#..#",
                   "####"]

    def test_link_spots(self):
        # Set up cave
        cave_width = len(self.SIMPLE_CAVE[0])
        cave = Cave(cave_width)
        for row in self.SIMPLE_CAVE:
            spots = [CaveSpot(point) for point in row]
            cave.add_row(spots)
        cave.link_spots()
        # Test created cave
        for i, spot in enumerate(cave.cave_map):
            if i < cave_width:
                assert spot.u is None
            else:
                assert spot.u is cave.cave_map[i - cave_width]
            if i >= cave_width * 2:
                assert spot.d is None
            else:
                assert spot.d is cave.cave_map[i + cave_width]
            if i % cave_width == 0:
                assert spot.l is None
            else:
                assert spot.l is cave.cave_map[i - 1]
            if (i + 1) % cave_width == 0:
                assert spot.r is None
            else:
                assert spot.r is cave.cave_map[i + 1]

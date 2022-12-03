from clay_map import ClayMap


class TestClayMap:
    def test_create_map(self):
        data = ["x=1, y=1",
                "y=2, x=2",
                "x=3, y=3..5",
                "y=6..8, x=4",
                "x=5..7, y=9",
                "y=10, x=8..10"]
        expected_clay = [(1, 1), (2, 2), (3, 3), (3, 4), (3, 5),
                         (4, 6), (4, 7), (4, 8), (5, 9), (6, 9),
                         (7, 9), (8, 10), (9, 10), (10, 10)]
        expected_sand = [(1, 2), (4, 4), 5, 8]
        expected_highest = 1
        expected_lowest = 10
        cm = ClayMap(data)

        for c in expected_clay:
            assert cm.is_clay(c) is True

        for s in expected_sand:
            assert cm.is_clay(s) is False

        assert cm.highest_point == expected_highest
        assert cm.lowest_point == expected_lowest


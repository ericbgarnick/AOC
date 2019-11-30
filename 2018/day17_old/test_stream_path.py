from clay_map import ClayMap
from stream_path_old import StreamPath, Direction, RowEndType


class TestStreamPath:
    @staticmethod
    def get_clay_map() -> ClayMap:
        data = ["x=1, y=1",
                "y=9, x=9",
                "x=3, y=3..5",
                "y=6..8, x=4",
                "x=5..7, y=9",
                "y=10, x=8..10"]
        return ClayMap(data)

    def test_init(self):
        cm = self.get_clay_map()
        sp = StreamPath(cm, Direction.LEFT)

        assert sp.direction == Direction.LEFT
        assert sp.row_end_pos is None
        assert sp.row_end_type is None
        assert sp.path_history == set()

    def test_open_end(self):
        cm = self.get_clay_map()
        sp = StreamPath(cm, Direction.LEFT)
        assert sp.open_end() is False

        sp.row_end_type = RowEndType.CLOSED
        assert sp.open_end() is False

        sp.row_end_type = RowEndType.OPEN
        assert sp.open_end() is True

    def test_fill_row_on_clay_no_surface(self):
        """Landed on a single square of clay"""
        cm = self.get_clay_map()
        start = (3, 2)
        sp = StreamPath(cm, Direction.LEFT)

        sp.fill_row(start)
        assert sp.head_pos == start
        assert sp.row_end_pos == start
        assert sp.open_end() is True
        assert sp.path_history == {start}

    def test_fill_row_on_clay_immediate_wall(self):
        """Landed next to a wall of clay"""
        cm = self.get_clay_map()
        start = (4, 5)
        sp = StreamPath(cm, Direction.LEFT)

        sp.fill_row(start)
        assert sp.head_pos == start
        assert sp.row_end_pos == start
        assert sp.open_end() is False
        assert sp.path_history == {start}

    def test_fill_row_on_clay_run_to_drop(self):
        """Landed on a platform of clay"""
        cm = self.get_clay_map()
        start = (5, 8)
        sp = StreamPath(cm, Direction.RIGHT)

        sp.fill_row(start)
        assert sp.head_pos == (7, 8)
        assert sp.row_end_pos == (7, 8)
        assert sp.open_end() is True
        assert sp.path_history == {(5, 8), (6, 8), (7, 8)}

    def test_fill_row_on_clay_run_to_wall(self):
        """Landed in a bowl of clay"""
        cm = self.get_clay_map()
        start = (7, 8)
        sp = StreamPath(cm, Direction.LEFT)

        sp.fill_row(start)
        assert sp.head_pos == (5, 8)
        assert sp.row_end_pos == (5, 8)
        assert sp.open_end() is False
        assert sp.path_history == {(7, 8), (6, 8), (5, 8)}

    def test_fill_row_on_water_run_to_drop(self):
        """Start one level above the platform of clay"""
        cm = self.get_clay_map()
        start = (5, 7)
        sp = StreamPath(cm, Direction.RIGHT)
        sp.path_history = {(5, 8), (6, 8), (7, 8)}

        sp.fill_row(start)
        assert sp.head_pos == (7, 7)
        assert sp.row_end_pos == (7, 7)
        assert sp.open_end() is True
        assert sp.path_history == {(5, 8), (6, 8), (7, 8),
                                   (5, 7), (6, 7), (7, 7)}

    def test_fill_row_on_water_run_to_wall(self):
        """Start one level above the platform of clay, run to a wall"""
        cm = self.get_clay_map()
        start = (7, 7)
        sp = StreamPath(cm, Direction.LEFT)
        sp.path_history = {(7, 8), (6, 8), (5, 8)}

        sp.fill_row(start)
        assert sp.head_pos == (5, 7)
        assert sp.row_end_pos == (5, 7)
        assert sp.open_end() is False
        assert sp.path_history == {(7, 8), (6, 8), (5, 8),
                                   (7, 7), (6, 7), (5, 7)}

from clay_map import ClayMap, Point
from water_tracer import WaterTracer


class TestWaterTracer:
    def test_drop(self):
        data = ["x=1, y=1",
                "y=6..8, x=500",
                "y=2, x=500",
                "x=3, y=650..655",
                "y=12, x=499..502"
                "y=6..8, x=500"]
        expected_bottom = (500, 1)
        wt = WaterTracer(data)

        # Drop from surface down 1
        start = ClayMap.SOURCE_SPRING
        bottom = wt.drop(start)
        assert bottom == expected_bottom

        # Drop from sand down several
        start = (499, 2)
        expected_bottom = (499, 11)
        bottom = wt.drop(start)
        assert bottom == expected_bottom

    @staticmethod
    def drop_history_helper(start: Point):
        data = ["x=5, y=2..9"]
        wt = WaterTracer(data)
        stop = (5, 9)
        expected_history = {(5, 2), (5, 3), (5, 4), (5, 5),
                            (5, 6), (5, 7), (5, 8), (5, 9)}
        history = wt.drop_history(start, stop)
        assert history == expected_history

    def test_drop_history_within_clay_range(self):
        self.drop_history_helper((5, 2))

    def test_drop_history_outside_clay_range(self):
        self.drop_history_helper((5, 0))

    ################
    # - TEST RUN - #
    ################
    def test_run_no_drop_1_clay_no_pool(self):
        """
          +
         |#|
        """
        data = ["x=500, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 2

    def test_run_1_drop_1_clay_no_pool(self):
        """
            +
        #  |||
           |#|
        """
        data = ["x=500, y=2",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 5

    def test_run_1_drop_1_clay_1_pool(self):
        """
            +
        #  ||||
           |##|
        """
        data = ["x=500..501, y=2",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 6

    def test_run_1_drop_1_clay_2_pool(self):
        """
            +
        # |||||
          |###|
        """
        data = ["x=499..501, y=2",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 7

    def test_run_1_drop_1_clay_dip_pool(self):
        """
            +
        # |||||
          |#~#|
          |###|
        """
        data = ["x=499..501, y=3",
                "x=499, y=2",
                "x=501, y=2",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 10

    def test_run_1_drop_1_clay_dip_pool_skip_top_row(self):
        """
            +
          ||||| (skip this row)
          |#~#|
          |###|
        """
        data = ["x=499..501, y=3",
                "x=499, y=2",
                "x=501, y=2"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 5

    def test_run_fancier_shapes_1(self):
        """
            +
        # |||||||
          |#~###|
          |#~~# |
          |#### |
        """
        data = ["x=499..502, y=4",
                "x=499, y=2..3",
                "x=502, y=3",
                "x=501..503, y=2",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 16

    def test_run_fancier_shapes_1_skip_top_row(self):
        """
            +
          ||||||| (skip this row)
          |#~###|
          |#~~# |
          |#### |
        """
        data = ["x=499..502, y=4",
                "x=499, y=2..3",
                "x=502, y=3",
                "x=501..503, y=2"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 9

    def test_run_fancier_shapes_2(self):
        """
            +
        # |||||
          |#~#|
          |###|
          | |||#
          | |#~#
          | |###
        """
        data = ["x=499..501, y=3",
                "x=499, y=2",
                "x=501, y=2",
                "x=501..503, y=6",
                "x=501, y=5",
                "x=503, y=4..5",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 19

    def test_run_fancier_shapes_3(self):
        """
            +
        # |||||
          |#~#|
          |###|
         #|||||#
         #~#|#~#
         ###|###
        """
        data = ["x=499..501, y=3",
                "x=499, y=2",
                "x=501, y=2",
                "x=501..503, y=6",
                "x=501, y=5",
                "x=503, y=4..5",
                "x=497, y=4..6",
                "x=498, y=6",
                "x=499, y=5..6",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 19

    def test_run_fancier_shapes_4(self):
        """
            +
        #   |
        |||||||||
        |#~~~~~#|
        |#~###~#|
        |#~~#~~#|
        |#######|
        """
        data = ["x=497, y=3..6",
                "x=503, y=3..6",
                "x=499..501, y=4",
                "x=498..502, y=6",
                "x=500, y=5",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        assert vol == 29

    def test_run_fancier_shapes_5(self):
        """
             +
        #    |
        |||||||||||
        |#~~~~~~~#|
        |#~~###~~#|
        |#~~~~~~~#|
        |#########|
        """
        data = ["x=496, y=3..6",
                "x=504, y=3..6",
                "x=499..501, y=4",
                "x=497..503, y=6",
                "x=1, y=1"]
        wt = WaterTracer(data)

        vol = wt.trace()

        with open('test.out', 'w') as test_out:
            test_out.write(str(wt))

        assert vol == 38

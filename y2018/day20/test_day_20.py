from unittest import TestCase

from day20 import Explorer, Position


class TestExplorer(TestCase):
    def test_explore_one_path(self):
        directions = '(NE)'
        expected_journal = {
            Position(0, 0): 0,
            Position(-1, 0): 1,
            Position(-1, 1): 2,
        }
        e = Explorer()
        e.explore_cave(directions)

        self.assertDictEqual(expected_journal, e.journal)

    def test_explore_three_paths(self):
        directions = '(NE|EE|W)'
        expected_journal = {
            Position(0, 0): 0,
            Position(-1, 0): 1,
            Position(-1, 1): 2,
            Position(0, 1): 1,
            Position(0, 2): 2,
            Position(0, -1): 1
        }
        e = Explorer()
        e.explore_cave(directions)

        self.assertDictEqual(expected_journal, e.journal)

    def test_explore_three_paths_with_prefix(self):
        directions = 'N(NE|EE|W)'
        expected_journal = {
            Position(0, 0): 0,
            Position(-1, 0): 1,
            Position(-2, 0): 2,
            Position(-2, 1): 3,
            Position(-1, 1): 2,
            Position(-1, 2): 3,
            Position(-1, -1): 2
        }
        e = Explorer()
        e.explore_cave(directions)

        self.assertDictEqual(expected_journal, e.journal)

    def test_explore_paths_with_prefix_and_nesting(self):
        directions = 'N(NE|EE(SS|NE)))'
        expected_journal = {
            Position(0, 0): 0,
            Position(-1, 0): 1,
            Position(-2, 0): 2,
            Position(-2, 1): 3,
            Position(-1, 1): 2,
            Position(-1, 2): 3,
            Position(0, 2): 4,
            Position(1, 2): 5,
            Position(-2, 2): 4,
            Position(-2, 3): 5
        }
        e = Explorer()
        e.explore_cave(directions)

        self.assertDictEqual(expected_journal, e.journal)

    def max_distance_check(self, directions: str, expected_distance: int):
        e = Explorer()
        e.explore_cave(directions)

        self.assertEqual(expected_distance, e.max_distance)

    def test_find_max_distance_simple(self):
        directions = '^WNE$'
        expected_distance = 3
        self.max_distance_check(directions, expected_distance)

    def test_find_max_distance_nesting(self):
        directions = '^ENWWW(NEEE|SSE(EE|N))$'
        expected_distance = 10
        self.max_distance_check(directions, expected_distance)

    def test_find_max_distance_dead_ends(self):
        directions = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
        expected_distance = 18
        self.max_distance_check(directions, expected_distance)

    def test_find_max_distance_nesting_dead_ends(self):
        directions = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
        expected_distance = 23
        self.max_distance_check(directions, expected_distance)

    def test_find_max_distance_long_nesting(self):
        directions = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
        expected_distance = 31
        self.max_distance_check(directions, expected_distance)

    def rooms_for_dist_check(self, directions: str, target_distance: int,
                             expected_num_rooms: int):
        e = Explorer()
        e.explore_cave(directions)

        self.assertEqual(expected_num_rooms, e.rooms_for_dist(target_distance))

    def test_rooms_for_dist1(self):
        directions = '^WNE$'
        target_distance = 2
        expected_num_rooms = 2
        self.rooms_for_dist_check(directions, target_distance,
                                  expected_num_rooms)

    def test_rooms_for_dist2(self):
        directions = '^N(E|NE|W)$'
        target_distance = 2
        expected_num_rooms = 4
        self.rooms_for_dist_check(directions, target_distance,
                                  expected_num_rooms)

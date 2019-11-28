from typing import Tuple, List

import pytest

from battle import Battle
from cave import CaveSpot
from team_unit import TeamUnit


@pytest.fixture
def defaults():
    first_spot = CaveSpot(CaveSpot.FLOOR)
    second_spot = CaveSpot(CaveSpot.FLOOR)
    third_spot = CaveSpot(CaveSpot.FLOOR)
    fourth_spot = CaveSpot(CaveSpot.FLOOR)
    fifth_spot = CaveSpot(CaveSpot.FLOOR)
    # Keep 6th as unconnected spot
    sixth_spot = CaveSpot(CaveSpot.FLOOR)
    default_team = TeamUnit.GOBLIN
    default_unit = TeamUnit(default_team, first_spot)
    setattr(TestTeamUnit, 'FIRST_SPOT', first_spot)
    setattr(TestTeamUnit, 'SECOND_SPOT', second_spot)
    setattr(TestTeamUnit, 'THIRD_SPOT', third_spot)
    setattr(TestTeamUnit, 'FOURTH_SPOT', fourth_spot)
    setattr(TestTeamUnit, 'FIFTH_SPOT', fifth_spot)
    setattr(TestTeamUnit, 'SIXTH_SPOT', sixth_spot)
    setattr(TestTeamUnit, 'DEFAULT_TEAM', default_team)
    setattr(TestTeamUnit, 'DEFAULT_UNIT', default_unit)


@pytest.mark.usefixtures("defaults")
class TestTeamUnit:
    ###############
    # - HELPERS - #
    ###############
    def link_first_second_spots(self):
        self.FIRST_SPOT.set_u(self.SECOND_SPOT)
        self.SECOND_SPOT.set_d(self.FIRST_SPOT)

    def split_first_second_spots(self):
        self.FIRST_SPOT.set_u(None)
        self.SECOND_SPOT.set_d(None)

    def link_first_third_spots(self):
        self.FIRST_SPOT.set_l(self.THIRD_SPOT)
        self.THIRD_SPOT.set_r(self.FIRST_SPOT)

    def split_first_third_spots(self):
        self.FIRST_SPOT.set_l(None)
        self.THIRD_SPOT.set_r(None)

    def link_first_fourth_spots(self):
        self.FIRST_SPOT.set_r(self.FOURTH_SPOT)
        self.FOURTH_SPOT.set_l(self.FIRST_SPOT)

    def split_first_fourth_spots(self):
        self.FIRST_SPOT.set_r(None)
        self.FOURTH_SPOT.set_l(None)

    def link_first_fifth_spots(self):
        self.FIRST_SPOT.set_d(self.FIFTH_SPOT)
        self.FIFTH_SPOT.set_u(self.FIRST_SPOT)

    def split_first_fifth_spots(self):
        self.FIRST_SPOT.set_d(None)
        self.FIFTH_SPOT.set_u(None)

    def create_elf_goblin(self) -> Tuple[TeamUnit, TeamUnit]:
        unit_elf = TeamUnit(TeamUnit.ELF, self.FIRST_SPOT)
        unit_goblin = TeamUnit(TeamUnit.GOBLIN, self.SECOND_SPOT)
        return unit_elf, unit_goblin

    ################################
    # - TEST BASIC FUNCTIONALITY - #
    ################################
    def test_create_unit(self):
        assert self.DEFAULT_UNIT.team == self.DEFAULT_TEAM
        assert self.DEFAULT_UNIT.occupies(self.FIRST_SPOT)
        assert self.DEFAULT_UNIT.health == TeamUnit.MAX_HEALTH_G

    def test_enemies(self):
        unit_elf, unit_goblin = self.create_elf_goblin()

        assert unit_elf.is_against(unit_goblin)
        assert unit_goblin.is_against(unit_elf)

    def test_occupies(self):
        assert self.DEFAULT_UNIT.occupies(self.FIRST_SPOT)
        assert not self.DEFAULT_UNIT.occupies(self.SIXTH_SPOT)

    def test_take_damage(self):
        initial_health = self.DEFAULT_UNIT.health
        damage = 1
        self.DEFAULT_UNIT.take_damage(damage)

        assert self.DEFAULT_UNIT.health == initial_health - damage

    def test_is_dead(self):
        damage = self.DEFAULT_UNIT.health
        self.DEFAULT_UNIT.take_damage(damage)

        assert self.DEFAULT_UNIT.is_dead

    def test_attack(self):
        unit_elf, unit_goblin = self.create_elf_goblin()

        initial_health = unit_goblin.health
        unit_elf.attack(unit_goblin)

        assert unit_goblin.health == initial_health - unit_elf.attack_power

    ###########################
    # - TEST ADJACENT SPOTS - #
    ###########################
    @staticmethod
    def adjacent_spots_checker(battle_map: List[str],
                               directions: str,
                               skip_occupied: bool = False,
                               start_up: bool = False):
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        start_spot = unit.spot.u if start_up else unit.spot
        adjacent_spots = unit.adjacent_spots(start=start_spot,
                                             skip_occupied=skip_occupied)

        assert len(adjacent_spots) == len(directions)
        for i, direction in enumerate(directions):
            dir_attr = getattr(start_spot, direction)
            assert adjacent_spots[i] is dir_attr

    def test_adjacent_spots_from_unit_all_free(self):
        battle_map = ["#######",
                      "#.....#",
                      "#..E..#",
                      "#.....#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'ulrd')

    def test_adjacent_spots_from_unit_one_wall(self):
        battle_map = ["#######",
                      "#..#..#",
                      "#..E..#",
                      "#.....#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'lrd')

    def test_adjacent_spots_from_unit_all_walls(self):
        battle_map = ["#######",
                      "#..#..#",
                      "#.#E#.#",
                      "#..#..#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, '')

    def test_adjacent_spots_from_unit_skip_occupied(self):
        battle_map = ["#######",
                      "#.....#",
                      "#..E..#",
                      "#..E..#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'ulr',
                                    skip_occupied=True)

    def test_adjacent_spots_from_other_point_all_free(self):
        battle_map = ["#######",
                      "#.....#",
                      "#.....#",
                      "#..E..#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'ulrd',
                                    start_up=True)

    def test_adjacent_spots_from_other_point_one_wall(self):
        battle_map = ["#######",
                      "#..#..#",
                      "#.....#",
                      "#..E..#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'lrd',
                                    start_up=True)

    def test_adjacent_spots_from_other_point_one_wall_one_unit(self):
        battle_map = ["#######",
                      "#..#..#",
                      "#.....#",
                      "#..E..#",
                      "#######"]
        self.adjacent_spots_checker(battle_map, 'lr',
                                    skip_occupied=True,
                                    start_up=True)

    ##########################
    # - TEST CHOOSE TARGET - #
    ##########################
    def test_choose_target_out_of_range(self):
        unit_elf = TeamUnit(TeamUnit.ELF, self.FIRST_SPOT)
        unit_goblin = TeamUnit(TeamUnit.GOBLIN, self.SIXTH_SPOT)

        assert unit_elf.choose_target([unit_goblin]) is None

    def test_choose_target_1_in_range(self):
        self.link_first_second_spots()

        unit_elf, unit_goblin = self.create_elf_goblin()

        assert unit_elf.choose_target([unit_goblin]) is unit_goblin

        self.split_first_second_spots()

    def setup_2_in_range(self) -> Tuple[TeamUnit, TeamUnit, TeamUnit]:
        self.link_first_second_spots()
        self.link_first_third_spots()

        unit_elf, unit_goblin1 = self.create_elf_goblin()
        unit_goblin2 = TeamUnit(TeamUnit.GOBLIN, self.THIRD_SPOT)
        return unit_elf, unit_goblin1, unit_goblin2

    def test_choose_target_2_in_range_same_health(self):
        unit_elf, unit_goblin1, unit_goblin2 = self.setup_2_in_range()

        chosen = unit_elf.choose_target([unit_goblin1, unit_goblin2])

        assert chosen is unit_goblin1

        self.split_first_second_spots()
        self.split_first_third_spots()

    def test_choose_target_2_in_range_diff_health(self):
        unit_elf, unit_goblin1, unit_goblin2 = self.setup_2_in_range()
        unit_goblin2.take_damage(1)

        chosen = unit_elf.choose_target([unit_goblin1, unit_goblin2])

        assert chosen is unit_goblin2

        self.split_first_second_spots()
        self.split_first_third_spots()

    def test_choose_targets_1_in_range_1_out_of_range(self):
        self.link_first_second_spots()

        unit_elf, unit_goblin1 = self.create_elf_goblin()
        unit_goblin2 = TeamUnit(TeamUnit.GOBLIN, self.SIXTH_SPOT)

        chosen = unit_elf.choose_target([unit_goblin1, unit_goblin2])

        assert chosen is unit_goblin1

        self.split_first_second_spots()

    #####################
    # - TEST MOVEMENT - #
    #####################
    def test_move(self):
        self.link_first_second_spots()

        self.DEFAULT_UNIT.move(self.SECOND_SPOT)

        assert self.DEFAULT_UNIT.occupies(self.SECOND_SPOT) is True

        self.split_first_second_spots()

    def test_make_best_move_1_option(self):
        self.link_first_fifth_spots()

        possible_destinations = [self.FIFTH_SPOT]
        self.DEFAULT_UNIT.make_best_move(possible_destinations)

        assert self.DEFAULT_UNIT.occupies(possible_destinations[0]) is True

        self.DEFAULT_UNIT.move(self.FIRST_SPOT)

        self.split_first_fifth_spots()

    def test_make_best_move_2_options(self):
        self.link_first_fourth_spots()
        self.link_first_fifth_spots()

        possible_destinations = [self.FOURTH_SPOT, self.FIFTH_SPOT]
        self.DEFAULT_UNIT.make_best_move(possible_destinations)

        assert self.DEFAULT_UNIT.occupies(possible_destinations[0]) is True

        self.DEFAULT_UNIT.move(self.FIRST_SPOT)

        self.split_first_fourth_spots()
        self.split_first_fifth_spots()

    def test_make_best_move_3_options(self):
        self.link_first_third_spots()
        self.link_first_fourth_spots()
        self.link_first_fifth_spots()

        possible_destinations = [self.THIRD_SPOT, self.FOURTH_SPOT,
                                 self.FIFTH_SPOT]
        self.DEFAULT_UNIT.make_best_move(possible_destinations)

        assert self.DEFAULT_UNIT.occupies(possible_destinations[0]) is True

        self.DEFAULT_UNIT.move(self.FIRST_SPOT)

        self.split_first_third_spots()
        self.split_first_fourth_spots()
        self.split_first_fifth_spots()

    def test_make_best_move_4_options(self):
        self.link_first_second_spots()
        self.link_first_third_spots()
        self.link_first_fourth_spots()
        self.link_first_fifth_spots()

        possible_destinations = [self.SECOND_SPOT, self.THIRD_SPOT,
                                 self.FOURTH_SPOT, self.FIFTH_SPOT]
        self.DEFAULT_UNIT.make_best_move(possible_destinations)

        assert self.DEFAULT_UNIT.occupies(possible_destinations[0]) is True

        self.DEFAULT_UNIT.move(self.FIRST_SPOT)

        self.split_first_second_spots()
        self.split_first_third_spots()
        self.split_first_fourth_spots()
        self.split_first_fifth_spots()

    #############################
    # - TEST DISTANCE TO SPOT - #
    #############################
    @staticmethod
    def distance_to_spot_checker(battle_map: List[str],
                                 expected_dist: int,
                                 spot_index: int,
                                 start_left: bool = False):
        battle = Battle(battle_map)
        unit = battle.all_units[0]

        spot = battle.cave.cave_map[spot_index]
        args = [[spot], unit.spot.l] if start_left else [[spot]]
        distance = unit.distance_to_spot(*args)[0][1]
        assert distance == expected_dist

    def test_distance_to_spot_disconnected(self):
        distance = self.DEFAULT_UNIT.distance_to_spot([self.SECOND_SPOT])[0][1]
        assert distance == -1

    def test_distance_to_spot_0_away(self):
        battle_map = ["E"]
        self.distance_to_spot_checker(battle_map, 0, 0)

    def test_distance_to_spot_1_away(self):
        battle_map = [".",
                      "E"]
        self.distance_to_spot_checker(battle_map, 1, 0)

    def test_distance_to_spot_2_away(self):
        battle_map = ["..",
                      "E."]
        self.distance_to_spot_checker(battle_map, 2, 1)

    def test_distance_to_spot_blocked_by_wall(self):
        battle_map = ["E#."]
        self.distance_to_spot_checker(battle_map, -1, 2)

    def test_distance_to_spot_blocked_by_unit(self):
        battle_map = ["EE."]
        self.distance_to_spot_checker(battle_map, -1, 2)

    def test_distance_to_spot_occupied_by_unit(self):
        battle_map = ["E.E"]
        self.distance_to_spot_checker(battle_map, -1, 2)

    def test_distance_to_spot_start_left(self):
        battle_map = ["..E"]
        self.distance_to_spot_checker(battle_map, 1, 0, start_left=True)

    def test_distance_to_spot_start_left_blocked(self):
        battle_map = [".#.E"]
        self.distance_to_spot_checker(battle_map, -1, 0, start_left=True)

    ###############################
    # - TEST CHOOSE DESTINATION - #
    ###############################
    def test_choose_destination_1_target_adjacent(self):
        battle_map = ["EG"]
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        possible_targets = [battle.all_units[1]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is unit.spot

    def test_choose_destination_1_target_1_away(self):
        battle_map = ["E.G"]
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        possible_targets = [battle.all_units[1]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[1]

    def test_choose_destination_1_target_1_away_wall_blocks_closest(self):
        battle_map = ["...",
                      "E#G",
                      "..."]
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        possible_targets = [battle.all_units[1]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[2]

    def test_choose_destination_1_target_1_away_wall_blocks_read_order(self):
        battle_map = ["..#",
                      "E#G",
                      "..."]
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        possible_targets = [battle.all_units[1]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[8]

    def test_choose_destination_2_targets_diff_distances(self):
        battle_map = ["..G",
                      "..."
                      "E..",
                      "..G"]
        battle = Battle(battle_map)
        unit = battle.all_units[1]
        possible_targets = [battle.all_units[0], battle.all_units[2]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[8]

    def test_choose_destination_2_targets_equidistant(self):
        battle_map = ["..G",
                      "E.#",
                      "..G"]
        battle = Battle(battle_map)
        unit = battle.all_units[1]
        possible_targets = [battle.all_units[0], battle.all_units[2]]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[1]

    def test_choose_destination_several_targets(self):
        battle_map = ["#######",
                      "#E..G.#",
                      "#...#.#",
                      "#.G.#G#",
                      "#######"]
        battle = Battle(battle_map)
        unit = battle.all_units[0]
        possible_targets = battle.all_units[1:]

        destination = unit.choose_destination(possible_targets, 0, 0)

        assert destination is battle.cave.cave_map[10]

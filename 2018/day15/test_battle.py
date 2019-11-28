from typing import Dict

import pytest

from battle import Battle
from cave import CaveSpot
from team_unit import TeamUnit
# unit_health referenced as fixture
from test_helpers import using_health, unit_health


class TestBattle:
    SIMPLE_MAP = ["#####",
                  "#...#",
                  "#.E.#",
                  "#...#",
                  "#####"]

    BATTLE_MAP = ["#########",
                  "#.......#",
                  "#.......#",
                  "#...E...#",
                  "#...GE..#",
                  "#.......#",
                  "#.......#",
                  "#########"]

    CAVE_MAP = ["#########",
                "#.......#",
                "#.......#",
                "#.......#",
                "#.......#",
                "#.......#",
                "#.......#",
                "#########"]

    UNITS = [TeamUnit(TeamUnit.ELF, CaveSpot(CaveSpot.FLOOR)),
             TeamUnit(TeamUnit.GOBLIN, CaveSpot(CaveSpot.FLOOR)),
             TeamUnit(TeamUnit.ELF, CaveSpot(CaveSpot.FLOOR))]

    ##################
    # - TEST SETUP - #
    ##################
    @staticmethod
    def test_create_print_battle(capsys):

        new_battle = Battle(TestBattle.BATTLE_MAP)

        for u in new_battle.all_units:
            assert u.battle == new_battle

        new_battle.print_cave()
        out, err = capsys.readouterr()
        assert out == "MAP:\n{}\n".format('\n'.join(TestBattle.CAVE_MAP))

        new_battle.print_units()
        out, err = capsys.readouterr()
        units_str = '\n'.join([str(u) for u in TestBattle.UNITS])
        assert out == "UNITS:\n{}\n".format(units_str)

        new_battle.print_battle()
        out, err = capsys.readouterr()
        assert out == "BATTLE:\n{}\n".format('\n'.join(TestBattle.BATTLE_MAP))

    ##################
    # - TEST UTILS - #
    ##################
    def test_is_spot_occupied_wall(self):
        new_battle = Battle(TestBattle.SIMPLE_MAP)
        spot = new_battle.cave.cave_map[0]

        assert new_battle.is_spot_occupied(spot) is False

    def test_is_spot_occupied_empty(self):
        new_battle = Battle(TestBattle.SIMPLE_MAP)
        spot = new_battle.cave.cave_map[6]

        assert new_battle.is_spot_occupied(spot) is False

    def test_is_spot_occupied_live_unit(self):
        new_battle = Battle(TestBattle.SIMPLE_MAP)
        spot = new_battle.cave.cave_map[12]

        assert new_battle.is_spot_occupied(spot) is True

    def test_is_spot_occupied_dead_unit(self):
        new_battle = Battle(TestBattle.SIMPLE_MAP)
        unit = new_battle.all_units[0]
        unit.take_damage(unit.health)
        spot = new_battle.cave.cave_map[12]

        assert new_battle.is_spot_occupied(spot) is False

    ###########################
    # - TEST RUN SIMULATION - #
    ###########################
    @staticmethod
    def battle_check(outcome: int, winners: str = TeamUnit.ELF,
                     damage_info: Dict[str, int] = None):
        new_battle = Battle(TestBattle.BATTLE_MAP)

        if damage_info is not None:
            tgt_index = damage_info['index']
            damage_amt = damage_info['amount']
            new_battle.all_units[tgt_index].take_damage(damage_amt)

        new_battle.run()

        assert new_battle.winners == winners
        assert new_battle.outcome == outcome

    @using_health(health_e=3, health_g=3)
    @pytest.mark.usefixtures("unit_health")
    def test_run_battle_no_rounds(self):
        """Goblin dies before round 1 finishes"""
        self.battle_check(0)

    @using_health(health_e=4, health_g=4)
    @pytest.mark.usefixtures("unit_health")
    def test_run_battle_one_round_strong_elves(self):
        """Goblin takes 2 hits, both elves alive at end of round 1"""
        self.battle_check(5)

    @using_health(health_e=3, health_g=4)
    @pytest.mark.usefixtures("unit_health")
    def test_run_battle_one_round_weak_elves(self):
        """Goblin takes 2 hits, kills 1 elf before round ends"""
        self.battle_check(3, winners=TeamUnit.ELF)

    @using_health(health_e=13, health_g=13)
    @pytest.mark.usefixtures("unit_health")
    def test_run_battle_two_rounds(self):
        """Goblin takes 5 hits, damages one elf during 2 rounds"""
        self.battle_check(40)

    @using_health(health_e=4, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_run_battle_target_lowest_health(self):
        """Elf in later read order has lower health, so goblin attacks
        and kills that one before being killed at end of round 1"""
        damage_info = {"index": 2, "amount": 2}
        self.battle_check(4, winners=TeamUnit.ELF,
                          damage_info=damage_info)

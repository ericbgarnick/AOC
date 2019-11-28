import pytest

from battle import Battle
from team_unit import TeamUnit
# Need unit_health for fixture
from test_helpers import using_health, unit_health


class TestSimulation:
    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_1_on_1_no_move(self):
        battle_map = ["#########",
                      "#.......#",
                      "#.......#",
                      "#...E...#",
                      "#...G...#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 1
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_2_on_1_no_move(self):
        battle_map = ["#########",
                      "#.......#",
                      "#.......#",
                      "#...E...#",
                      "#..EG...#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 0
        expected_remaining_health = 10

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_2_on_2_no_move(self):
        battle_map = ["#########",
                      "#.......#",
                      "#.......#",
                      "#..GE...#",
                      "#..EG...#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        # 2 attackers
        expected_num_rounds = 2
        # One elf hurt, one untouched
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_1_on_1_one_move(self):
        battle_map = ["#########",
                      "#...G...#",
                      "#.......#",
                      "#...E...#",
                      "#.......#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 1
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_1_on_1_one_move_each(self):
        battle_map = ["#########",
                      "#...E...#",
                      "#.......#",
                      "#.......#",
                      "#...G...#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 2
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_1_on_1_two_moves_each(self):
        battle_map = ["#########",
                      "#..E....#",
                      "#.......#",
                      "#.......#",
                      "#....G..#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 3
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=5, health_g=5)
    @pytest.mark.usefixtures("unit_health")
    def test_1_on_1_move_around_obstacle(self):
        battle_map = ["#########",
                      "#...G...#",
                      "#...#...#",
                      "#.......#",
                      "#...E...#",
                      "#.......#",
                      "#.......#",
                      "#########"]
        battle = Battle(battle_map)
        battle.run()

        expected_num_rounds = 3
        expected_remaining_health = 2

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == expected_num_rounds * expected_remaining_health

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_1(self):
        battle_map = ["#######",
                      "#.G...#",
                      "#...EG#",
                      "#.#.#G#",
                      "#..G#E#",
                      "#.....#",
                      "#######"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == 27730

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_2(self):
        battle_map = ["#######",
                      "#G..#E#",
                      "#E#E.E#",
                      "#G.##.#",
                      "#...#E#",
                      "#...E.#",
                      "#######"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == 36334

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_3(self):
        battle_map = ["#######",
                      "#E..EG#",
                      "#.#G.E#",
                      "#E.##E#",
                      "#G..#.#",
                      "#..E#.#",
                      "#######"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.ELF
        assert battle.outcome == 39514

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_4(self):
        battle_map = ["#######",
                      "#E.G#.#",
                      "#.#G..#",
                      "#G.#.G#",
                      "#G..#.#",
                      "#...E.#",
                      "#######"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == 27755

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_5(self):
        battle_map = ["#######",
                      "#.E...#",
                      "#.#..G#",
                      "#.###.#",
                      "#E#G#G#",
                      "#...#G#",
                      "#######"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == 28944
        # assert True is False

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_sample_6(self):
        battle_map = ["#########",
                      "#G......#",
                      "#.E.#...#",
                      "#..##..G#",
                      "#...##..#",
                      "#...#...#",
                      "#.G...G.#",
                      "#.....G.#",
                      "#########"]

        battle = Battle(battle_map)
        battle.run()

        battle.print_battle()

        assert battle.winners == TeamUnit.GOBLIN
        assert battle.outcome == 18740

    @using_health(health_e=200, health_g=200)
    @pytest.mark.usefixtures("unit_health")
    def test_big_map(self):
        battle_map = ["##################################################",
                      "#........................#.......................#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#.............#..........#.........#.............#",
                      "#...G......G..#..........#.........#....E.....E..#",
                      "#.G.....G.....#..........#.........#.....E...E...#",
                      "#...G......G..#..........#.........#..E.....E....#",
                      "#....G...G....#..........#.........#....E.....E..#",
                      "#...G...G.....#....................#...E..E......#",
                      "##################################################"]

        battle = Battle(battle_map)
        battle.run(max_rounds=1)

        battle.print_battle()
        battle.print_metrics()

        # Uncomment below to see metrics
        # assert False is True

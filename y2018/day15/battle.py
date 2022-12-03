from collections import defaultdict
from typing import List, Iterable, Optional, Tuple, Dict

from cave import Cave, CaveSpot
from metric import Metric
from team_unit import TeamUnit


METRIC_NAMES = ("load_battle", "find_possible_targets", "choose_destination",
                "approach_destination", "try_attack", "sorted_destinations",
                "calc_distances_to_adjacent_spots", "determine_unoccupied",
                "closest_spots", "collect_adjacent_spots", "record_spot",
                "in_adjacent_spots", "add_spot_with_dist")


class Battle:
    def __init__(self, battle_map: Iterable[str],
                 metric_names: Tuple[str] = METRIC_NAMES):
        self.metrics = {n: Metric(n) for n in metric_names}

        self._battle_over = False
        self._round_num = 0
        self._teams = defaultdict(int)
        # units kept in order of next turn
        self._units = []            # type: List[TeamUnit]
        self._cave = None           # type: Optional[Cave]
        self._spots_for_units = {}  # type: Dict[CaveSpot, TeamUnit]
        self._time_since_movement = 0
        self._time_since_death = 0
        self.metrics["load_battle"].start()
        self._load_battle(battle_map)
        self.metrics["load_battle"].stop()
        self._battle_outcome = 0
        self._winning_team = None   # type: Optional[str]

    @property
    def all_units(self) -> List[TeamUnit]:
        return self._units

    @property
    def ordered_units(self) -> List[TeamUnit]:
        return sorted(self._units,
                      key=lambda u: self._cave.cave_map.index(u.spot))

    @property
    def cave(self) -> Cave:
        return self._cave

    @property
    def outcome(self) -> int:
        return self._battle_outcome

    @property
    def winners(self) -> str:
        return self._winning_team

    def print_cave(self):
        print("MAP:")
        print(self._cave)

    def print_units(self):
        print("UNITS:")
        for u in self._units:
            print(u)

    def print_battle(self):
        print("BATTLE:")
        battle_map = []
        for spot in self._cave.cave_map:
            battle_map.append(spot.spot_type)
            if spot.spot_type == CaveSpot.FLOOR:
                for unit in self._units:
                    if unit.occupies(spot):
                        unit_loc = self.ordered_units.index(unit)
                        battle_map[-1] = unit.team
                        break
        print(self._cave.cave_string(battle_map, self._cave.width))

    def print_metrics(self):
        print("METRICS:")
        print('\n\n'.join(str(metric) for metric in
                          sorted(self.metrics.values(),
                                 key=lambda m: m.total_time)))

    #############
    # - SETUP - #
    #############
    def _load_battle(self, battle_map: Iterable[str]):
        for row in battle_map:
            row = row.strip()
            if not self._cave:
                self._cave = Cave(len(row))
            map_row = []
            for point in row.strip():
                spot = CaveSpot(point)
                map_row.append(spot)
                self._create_unit(point, spot)
            self._cave.add_row(map_row)
        self._cave.link_spots()

    def _create_unit(self, point: str, cave_spot: CaveSpot):
        """Create a TeamUnit and add to self._units if specified by point"""
        if point in TeamUnit.POSSIBLE_UNITS:
            unit = TeamUnit(point, cave_spot, self)
            self._spots_for_units[cave_spot] = unit
            self._units.append(unit)
            self._teams[point] += 1

    #############
    # - UTILS - #
    #############
    def update_spot_for_unit(self, unit: TeamUnit, new_spot: CaveSpot):
        self._spots_for_units.pop(unit.spot)
        self._spots_for_units[new_spot] = unit
        self._time_since_movement = 0

    def is_spot_occupied(self, spot: CaveSpot) -> bool:
        at_spot = self._spots_for_units.get(spot)
        try:
            # TeamUnit at spot
            return not at_spot.is_dead
        except AttributeError:
            # Nothing at spot
            return False

    ######################
    # - RUN SIMULATION - #
    ######################
    def run(self, max_rounds: int = -1):
        while self._num_teams_remaining() > 1:
            if 0 < max_rounds <= self._round_num:
                return
            for unit_num, unit in enumerate(self.ordered_units):
                self._time_since_movement += 1
                self._time_since_death += 1
                if not unit.is_dead:
                    self.metrics["find_possible_targets"].start()
                    possible_targets = [t for t in self._units if
                                        not t.is_dead and t.is_against(unit)]
                    self.metrics["find_possible_targets"].stop()
                    if possible_targets:
                        self.metrics["choose_destination"].start()
                        destination = unit.choose_destination(
                            possible_targets,
                            self._time_since_movement,
                            self._time_since_death)
                        self.metrics["choose_destination"].stop()
                        if not unit.occupies(destination):
                            self.metrics["approach_destination"].start()
                            unit.approach_destination(destination)
                            self.metrics["approach_destination"].stop()
                        if unit.occupies(destination):
                            # Approach may have moved unit into range
                            self.metrics["try_attack"].start()
                            self._try_attack(unit, unit_num, possible_targets)
                            self.metrics["try_attack"].stop()
                    else:
                        self._battle_over = True
                        break
            if not self._battle_over:
                self._round_num += 1
        self._determine_winning_team()
        self._calculate_outcome()

    def _try_attack(self, unit: TeamUnit, unit_num: int,
                    possible_targets: List[TeamUnit]):
        target = unit.choose_target(possible_targets)
        if target:
            unit.attack(target)
            if target.is_dead:
                self._time_since_death = 0
                self._teams[target.team] -= 1
                if unit_num + 1 < len(self._units):
                    # Let this round complete if the last unit killed someone
                    self._battle_over = self._num_teams_remaining() < 2

    def _num_teams_remaining(self) -> int:
        return len([team_size for team_size in self._teams.values()
                    if team_size])

    def _determine_winning_team(self):
        self._winning_team = next(unit.team for unit in self._units
                                  if not unit.is_dead)

    def _calculate_outcome(self):
        for u in self._units:
            print(u)
        remaining_health = sum(u.health for u in self._units if not u.is_dead)
        print("TOTAL HEALTH:", remaining_health)
        print("ROUND NUM:", self._round_num)
        self._battle_outcome = self._round_num * remaining_health

from queue import Queue
from typing import List, Optional, Tuple

from cave import CaveSpot


class TeamUnit:

    ELF = "E"
    GOBLIN = "G"
    POSSIBLE_UNITS = {ELF, GOBLIN}

    # 13 Attack power for all elves to survive
    ATTACK_POWER_E = 3
    ATTACK_POWER_G = 3
    MAX_HEALTH_E = 200
    MAX_HEALTH_G = 200

    def __init__(self, team: str, cave_spot: CaveSpot, battle=None):
        self._hitpoints = (self.MAX_HEALTH_E if team == self.ELF
                           else self.MAX_HEALTH_G)
        self._attack_power = (self.ATTACK_POWER_E if team == self.ELF
                              else self.ATTACK_POWER_G)

        self._team = team
        self._spot = cave_spot
        self._battle = battle
        self._latest_destination = None     # type: CaveSpot

    def __str__(self):
        return "{}: {}".format(self._team, self._hitpoints)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'TeamUnit'):
        return (self._hitpoints == other._hitpoints and
                self._team == other._team and
                self._spot == other._spot)

    @property
    def team(self) -> str:
        return self._team

    @property
    def spot(self) -> CaveSpot:
        return self._spot

    @property
    def battle(self):
        return self._battle

    @property
    def is_dead(self) -> bool:
        return self._hitpoints <= 0

    @property
    def health(self) -> int:
        return self._hitpoints

    @property
    def attack_power(self) -> int:
        return self._attack_power

    def is_against(self, other: 'TeamUnit') -> bool:
        return self._team != other.team

    def choose_destination(self, targets: List['TeamUnit'],
                           time_since_movement: int,
                           time_since_death: int) -> Optional[CaveSpot]:
        """Return the CaveSpot this TeamUnit should move towards.
        Return None if there is nowhere to go"""
        if (time_since_movement > len(self.battle.all_units) and
                time_since_death > len(self.battle.all_units)):
            return self._latest_destination
        self.battle.metrics["sorted_destinations"].start()
        sorted_destinations = self._sorted_destinations(targets)
        self.battle.metrics["sorted_destinations"].stop()

        self.battle.metrics["closest_spots"].start()
        closest_spots = self._closest_spots(sorted_destinations)
        self.battle.metrics["closest_spots"].stop()

        if not len(closest_spots):
            # No spots reachable
            self._latest_destination = None
        elif len(closest_spots) == 1:
            # One distinctly closest
            self._latest_destination = closest_spots[0]
        else:
            # Multiple tied for closest
            self._latest_destination = self._first_read_order_spot(closest_spots)
        return self._latest_destination

    def choose_target(self, targets: List['TeamUnit']) -> Optional['TeamUnit']:
        """Returns the target to attack this turn if any"""
        # Return None when there are no targets in range
        ordered_targets = [None]
        best_target_health = float('inf')
        for spot in self.adjacent_spots():
            for t in targets:
                if t.occupies(spot):
                    if t.health < best_target_health:
                        best_target_health = t.health
                        ordered_targets.append(t)
        return ordered_targets[-1]

    # TODO: test!
    def approach_destination(self, destination: CaveSpot):
        """Update self._spot to a CaveSpot 1 step closer to destination.
        If more than 1 adjacent spot moves closer, choose the spot of
        earlier read-order"""

        if destination is None:
            return

        adj_spots = self.adjacent_spots(skip_occupied=True)
        distances = self.distance_to_spot(adj_spots, destination)

        closer_spot = None
        closer_dist = float('inf')
        for spot in adj_spots:
            dist = next(p[1] for p in distances if p[0] is spot)
            if 0 <= dist < closer_dist:
                closer_dist = dist
                closer_spot = spot
        if closer_spot is None:
            # Unit is boxed in
            pass
        else:
            self.move(closer_spot)

    def _sorted_destinations(self, targets: List['TeamUnit']) -> \
            List[Tuple[CaveSpot, int]]:
        """Return a list of FLOOR-type CaveSpots adjacent to
        targets in increasing order of distance from self"""
        self.battle.metrics["collect_adjacent_spots"].start()
        nested_adjs = [self.adjacent_spots(t.spot) for t in targets]
        flattened_spots = [s for adjs in nested_adjs for s in adjs]
        self.battle.metrics["collect_adjacent_spots"].stop()

        self.battle.metrics["calc_distances_to_adjacent_spots"].start()
        all_spot_dists = self.distance_to_spot(flattened_spots)
        self.battle.metrics["calc_distances_to_adjacent_spots"].stop()

        return sorted([pair for pair in all_spot_dists if pair[1] >= 0],
                      key=lambda pair: pair[1])

    @staticmethod
    def _closest_spots(sorted_destinations: List[Tuple[CaveSpot, int]]) -> \
            List[CaveSpot]:
        closest_spots = []
        if len(sorted_destinations):
            min_dist = sorted_destinations[0][1]
            for pair in sorted_destinations:
                if pair[1] == min_dist:
                    closest_spots.append(pair[0])
                else:
                    # No more spots as close as the closest
                    break
        return closest_spots

    def _first_read_order_spot(self, candidate_spots: List[CaveSpot]) -> CaveSpot:
        """Return the CaveSpot from candidate_spots first in read-order."""
        cave_spots = self._battle.cave.cave_map  # type: List[CaveSpot]
        earliest_order = cave_spots.index(candidate_spots[0])
        earliest_spot = candidate_spots[0]
        for spot in candidate_spots[1:]:
            order = cave_spots.index(spot)
            if order < earliest_order:
                earliest_order = order
                earliest_spot = spot
        return earliest_spot

    def occupies(self, spot: CaveSpot) -> bool:
        return not self.is_dead and self._spot == spot

    def attack(self, other: 'TeamUnit'):
        other.take_damage(self._attack_power)

    def take_damage(self, damage: int):
        new_hp = max(0, self._hitpoints - damage)
        self._hitpoints = new_hp
        
    def make_best_move(self, possible_destinations: List[CaveSpot]):
        """Update self._spot to the read-order-first
        CaveSpot in possible_destinations."""
        for spot in self.adjacent_spots():
            for dest in possible_destinations:
                if spot == dest:
                    self.move(dest)
                    return

    def move(self, destination: CaveSpot):
        try:
            self.battle.update_spot_for_unit(self, destination)
        except AttributeError:
            # Unit is not in a Battle
            pass
        self._spot = destination

    def adjacent_spots(self, start: CaveSpot = None,
                       skip_occupied: bool = False) -> List[CaveSpot]:
        """Return a list of CaveSpots (row, col)
        adjacent to self, ordered by read order."""
        if self.battle:
            self.battle.metrics["in_adjacent_spots"].start()
        start = start or self._spot
        all_adjacent = (start.u, start.l, start.r, start.d)
        non_wall = [spot for spot in all_adjacent
                    if spot and spot.spot_type != CaveSpot.WALL]
        if skip_occupied:
            result = [spot for spot in non_wall
                      if not self._battle.is_spot_occupied(spot)]
        else:
            result = non_wall
        if self.battle:
            self.battle.metrics["in_adjacent_spots"].stop()
        return result

    def distance_to_spot(self, destinations: List[CaveSpot],
                         start: CaveSpot = None) -> List[Tuple[CaveSpot, int]]:
        """Return the number of moves required to reach destination.
        Return -1 if no path found to destination"""
        start = start or self._spot

        seen_spots = {start}
        spot_q = Queue()
        distances = {start: 0}

        spot_q.put(start)

        while not spot_q.empty():
            current_spot = spot_q.get()
            cur_dist = distances[current_spot]
            for adjacent in self.adjacent_spots(current_spot):
                unseen = adjacent not in seen_spots
                self.battle.metrics["determine_unoccupied"].start()
                unoccupied = not self._battle.is_spot_occupied(adjacent)
                self.battle.metrics["determine_unoccupied"].stop()
                if unseen and unoccupied:
                    self.battle.metrics["record_spot"].start()
                    distances[adjacent] = cur_dist + 1
                    seen_spots.add(adjacent)
                    spot_q.put(adjacent)
                    self.battle.metrics["record_spot"].stop()
        return [(dest, distances.get(dest, -1)) for dest in destinations]

from enum import Enum
from sys import argv
from typing import Dict, List, Any

Chart = List[Dict[str, Any]]


class SeatingChart:
    EMPTY_SEAT = "L"
    FULL_SEAT = "#"
    FLOOR = "."

    class DecisionCriteria(Enum):
        """Number of surrounding full seats that cause a full seat to become empty"""
        ADJACENCY = 4
        VISIBILITY = 5

    def __init__(self, chart_file: str, decision_criteria: DecisionCriteria):
        self.decision_criteria = decision_criteria
        self.any_changes = True
        self.row_width = 0
        self.col_length = 0
        self.chart = []  # type: Chart
        self._parse_input(chart_file)

    def __str__(self) -> str:
        output = []
        last_row_start = self.row_width * self.col_length - self.row_width + 1
        for row_start in range(0, last_row_start + 1, self.row_width):
            row_end = row_start + self.row_width
            output.append("".join(
                [space["cur"] for space in
                 self.chart[row_start:row_end]])
            )
        return "\n".join(output)

    def update_seats(self):
        self._set_next_space_values()
        self._update_cur_space_values()

    def _set_next_space_values(self):
        for seat in self.chart:
            num_full_surrounding = sum(
                1 for space in seat["surrounding"] if
                self.chart[space]["cur"] == self.FULL_SEAT
            )
            if seat["cur"] == self.EMPTY_SEAT and num_full_surrounding == 0:
                seat["next"] = self.FULL_SEAT
            elif seat["cur"] == self.FULL_SEAT and num_full_surrounding >= self.decision_criteria.value:
                seat["next"] = self.EMPTY_SEAT

    def _update_cur_space_values(self):
        change = False

        for seat in self.chart:
            if seat["cur"] != seat["next"]:
                change = True
            seat["cur"] = seat["next"]

        self.any_changes = change

    @property
    def total_spaces(self) -> int:
        return self.row_width * self.col_length

    @property
    def num_full_seats(self) -> int:
        return sum(1 for seat in self.chart if seat["cur"] == self.FULL_SEAT)

    def _parse_input(self, filename: str):
        for row in open(filename, "r"):
            row = row.strip()
            if not self.row_width:
                self.row_width = len(row)
            self.chart += [{"cur": val, "next": val, "surrounding": []} for val in row]
            self.col_length += 1
        self._build_chart()

    def _build_chart(self):
        for i, seat in enumerate(self.chart):
            if seat["cur"] == self.EMPTY_SEAT:
                self._set_surrounding_seats(i)

    def _set_surrounding_seats(self, idx: int):
        can_set_left = bool(idx % self.row_width)
        can_set_right = bool((idx + 1) % self.row_width)

        if idx >= self.row_width:                 # not first row
            self._set_next_seat(idx, -1, 0)       # N
            if can_set_left:
                self._set_next_seat(idx, -1, -1)  # NW
            if can_set_right:
                self._set_next_seat(idx, -1, 1)   # NE

        if idx < self.total_spaces - self.row_width:   # not last row
            self._set_next_seat(idx, 1, 0)        # S
            if can_set_left:
                self._set_next_seat(idx, 1, -1)   # SW
            if can_set_right:
                self._set_next_seat(idx, 1, 1)    # SE

        if can_set_left:                          # not first col
            self._set_next_seat(idx, 0, -1)       # W

        if can_set_right:                         # not last col
            self._set_next_seat(idx, 0, 1)        # E

    def _set_next_seat(self, start_idx: int, row_change: int, col_change: int):
        next_idx = start_idx + self.row_width * row_change + col_change

        while not self._stop_looking(next_idx, row_change, col_change):
            next_idx += self.row_width * row_change + col_change

        if self.chart[next_idx]["cur"] != self.FLOOR:
            self.chart[start_idx]["surrounding"].append(next_idx)

    def _stop_looking(self, idx: int, row_change: int, col_change: int) -> bool:
        # For adjacency criteria, only ever look at the immediately adjacent seat
        if self.decision_criteria == self.DecisionCriteria.ADJACENCY:
            return True

        if self.chart[idx]["cur"] != self.FLOOR:
            return True

        at_edge_col = idx % self.row_width == 0 or (idx + 1) % self.row_width == 0
        at_edge_row = idx < self.row_width or idx >= self.total_spaces - self.row_width

        if not row_change:
            # Searching horizontally
            return at_edge_col

        if not col_change:
            # Searching vertically
            return at_edge_row

        else:
            # Searching diagonally
            return at_edge_col or at_edge_row


def simulate(seating_chart: SeatingChart) -> int:
    while seating_chart.any_changes:
        seating_chart.update_seats()
    return seating_chart.num_full_seats


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", simulate(SeatingChart(input_file, SeatingChart.DecisionCriteria.ADJACENCY)))
    print("PART 2:", simulate(SeatingChart(input_file, SeatingChart.DecisionCriteria.VISIBILITY)))

"""
Part 1 answer: 93226
Part 2 answer:
"""
import re
from enum import Enum
from typing import Optional

from y2022.python.shared import get_data_file_path


class Board:
    NULL = " "
    OPEN = "."
    WALL = "#"
    def __init__(self, raw_board: list[str]):
        board_width = max(len(row) for row in raw_board)
        self.board = [[Board.NULL] * board_width for _ in range(len(raw_board))]
        self.fill_board(raw_board)

    def fill_board(self, raw_board: list[str]):
        for r, row in enumerate(raw_board):
            for c, symbol in enumerate(row):
                self.board[r][c] = symbol


class CubeFace:
    def __init__(self, raw_face: list[str]):
        size = len(raw_face)
        self.face = [[Cube.OPEN] * size for _ in range(size)]
        self.fill_face(raw_face)
        self.u: Optional["CubeFace"] = None  # face before row 0
        self.d: Optional["CubeFace"] = None  # face after last row
        self.l: Optional["CubeFace"] = None  # face before col 0
        self.r: Optional["CubeFace"] = None  # face after last col

    def fill_face(self, raw_face: list[str]):
        for r, row in enumerate(raw_face):
            for c, symbol in enumerate(row):
                self.face[r][c] = symbol


class Cube:
    NULL = " "
    OPEN = "."
    WALL = "#"
    def __init__(self, raw_cube: list[str]):
        self.size = gcd(len(raw_cube), len(raw_cube[0].strip()))
        self.faces: list[list[Optional[CubeFace]]] = []
        self._create_faces(raw_cube)
        self._connect_faces()


    def _create_faces(self, raw_cube: list[str]):
        for start_row in range(0, len(raw_cube), self.size):
            self.faces.append([])
            for start_col in range(0, len(raw_cube[start_row]), self.size):
                if raw_cube[start_row][start_col] == Cube.NULL:
                    self.faces[start_row].append(None)
                else:
                    end_row = start_row + self.size
                    end_col = start_col + self.size
                    raw_face = [row[start_col: end_col] for row in raw_cube[start_row: end_row]]
                    self.faces[start_row].append(CubeFace(raw_face))

    def _connect_faces(self):
        for r, row in enumerate(self.faces):
            for c, face in enumerate(row):
                if face is not None:
                    try:
                        if self.faces[r][c + 1] is not None:
                            face.r = self.faces[r][c + 1]
                            self.faces[r][c + 1].l = face
                    except IndexError:
                        pass
                    try:
                        if c != 0 and self.faces[r][c - 1] is not None:
                            face.l = self.faces[r][c - 1]
                            self.faces[r][c - 1].r = face
                    except IndexError:
                        pass
                    try:
                        if self.faces[r + 1][c] is not None:
                            face.d = self.faces[r + 1][c]
                            self.faces[r + 1][c].u = face
                    except IndexError:
                        pass
                    try:
                        if r != 0 and self.faces[r - 1][c] is not None:
                            face.u = self.faces[r - 1][c]
                            self.faces[r - 1][c].d = face
                    except IndexError:
                        pass

    def _connect_faces_helper(self, face: CubeFace):
        self._connect_up_helper(face)
        self._connect_down_helper(face)

    @staticmethod
    def _connect_up_helper(face: CubeFace):
        target = None
        try:
            target = face.d.d.d
        except AttributeError:
            pass
        if target is None:
            left = face.l
            while left is not None and left.u is None:
                left = left.l
            if left is not None and left.u is not None:
                target = left.u
        if target is None:
            right = face.r
            while right is not None and right.u is None:
                right = right.r
            if right is not None and right.u is not None:
                target = right.u
        if target is not None:
            face.u = target
            target.d = face

    @staticmethod
    def _connect_down_helper(face: CubeFace):
        target = None
        try:
            target = face.u.u.u
        except AttributeError:
            pass
        if target is None:
            left = face.l
            while left is not None and left.d is None:
                left = left.l
            if left is not None and left.d is not None:
                target = left.d
        if target is None:
            right = face.r
            while right is not None and right.d is None:
                right = right.r
            if right is not None and right.d is not None:
                target = right.d
        if target is not None:
            face.d = target
            target.u = face

    @staticmethod
    def _connect_left_helper(face: CubeFace):
        target = None
        try:
            target = face.r.r.r
        except AttributeError:
            pass
        if target is None:
            up = face.u
            while up is not None and up.l is None:
                up = up.u
            if up is not None and up.l is not None:
                target = up.l
        if target is None:
            down = face.d
            while down is not None and down.l is None:
                down = down.d
            if down is not None and down.l is not None:
                target = down.l
        if target is not None:
            face.l = target
            target.r = face


def gcd(a: int, b: int) -> int:
    factor = 2
    candidate = 1
    while factor <= min(a, b) // 2:
        if a % factor == b % factor == 0:
            candidate = factor
        factor += 1
    return candidate


class Pawn:
    class Direction(Enum):
        U = "U"
        D = "D"
        L = "L"
        R = "R"
    TURN = {
        Direction.U: {"L": Direction.L, "R": Direction.R},
        Direction.D: {"L": Direction.R, "R": Direction.L},
        Direction.L: {"L": Direction.D, "R": Direction.U},
        Direction.R: {"L": Direction.U, "R": Direction.D},
    }
    def __init__(self, board: Board):
        self.board = board
        self.position = self.find_start()
        self.direction = self.Direction.R

    def find_start(self) -> tuple[int, int]:
        """Return (row, col) of starting position (for open space in the first row)"""
        return 0, self.board.board[0].index(Board.OPEN)

    def run(self, instructions: str):
        moves = re.findall(r"\d+", instructions)
        turns = re.findall(r"[LR]", instructions)
        for i, dist in enumerate(moves):
            self.move(int(dist))
            try:
                self.direction = self.TURN[self.direction][turns[i]]
            except IndexError:
                # Ran out of turns
                return

    def move(self, distance: int):
        next_position = self.next_position()
        while distance and next_position != self.position:
            self.position = next_position
            distance -= 1
            next_position = self.next_position()

    def next_position(self) -> tuple[int, int]:
        """
        Return the (row, col) of the next position to move to,
        given the current position and current direction.

        If the next position is a wall, return the current position.
        """
        if self.direction in [self.Direction.U, self.Direction.D]:
            next_pos_col = self.position[1]
            if self.direction == self.Direction.U:
                if self.position[0] == 0 or self.board.board[self.position[0] - 1][self.position[1]] == Board.NULL:
                    next_pos_row = self.last_row()
                else:
                    next_pos_row = self.position[0] - 1
            else:
                if self.position[0] == len(self.board.board) - 1 or self.board.board[self.position[0] + 1][self.position[1]] == Board.NULL:
                    next_pos_row = self.first_row()
                else:
                    next_pos_row = self.position[0] + 1
        else:  # L or R
            next_pos_row = self.position[0]
            if self.direction == self.Direction.L:
                if self.position[1] == 0 or self.board.board[self.position[0]][self.position[1] - 1] == Board.NULL:
                    next_pos_col = self.last_col()
                else:
                    next_pos_col = self.position[1] - 1
            else:
                if self.position[1] == len(self.board.board[0]) - 1 or self.board.board[self.position[0]][self.position[1] + 1] == Board.NULL:
                    next_pos_col = self.first_col()
                else:
                    next_pos_col = self.position[1] + 1

        if self.board.board[next_pos_row][next_pos_col] == Board.WALL:
            return self.position
        else:
            return next_pos_row, next_pos_col

    def last_row(self) -> int:
        row = len(self.board.board) - 1
        while self.board.board[row][self.position[1]] == Board.NULL:
            row -= 1
        return row

    def first_row(self) -> int:
        row = 0
        while self.board.board[row][self.position[1]] == Board.NULL:
            row += 1
        return row

    def last_col(self) -> int:
        col = len(self.board.board[0]) - 1
        while self.board.board[self.position[0]][col] == Board.NULL:
            col -= 1
        return col

    def first_col(self) -> int:
        col = 0
        while self.board.board[self.position[0]][col] == Board.NULL:
            col += 1
        return col


ROW_MULTIPLIER = 1000
COL_MULTIPLIER = 4
DIRECTION_SCORE = {
    Pawn.Direction.R: 0,
    Pawn.Direction.D: 1,
    Pawn.Direction.L: 2,
    Pawn.Direction.U: 3,
}


def main():
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        raw_board, instructions = f_in.read().split("\n\n")
    board = Board(raw_board.split("\n"))
    pawn = Pawn(board)
    pawn.run(instructions.strip())
    password = sum(
        [(pawn.position[0] + 1) * ROW_MULTIPLIER,
         (pawn.position[1] + 1) * COL_MULTIPLIER,
         DIRECTION_SCORE[pawn.direction]],
    )
    print("PART 1:", password)


if __name__ == "__main__":
    main()

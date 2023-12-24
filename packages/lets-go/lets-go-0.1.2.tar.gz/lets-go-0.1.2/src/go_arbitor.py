# -*- coding: utf-8 -*-

#   Copyright 2023 Brooks Su
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""A GoArbitor class to record moves of Go game, and determine if the
moves on the game grid are valid.
"""

from dataclasses import dataclass


BLACK_STONE = 0
WHITE_STONE = 1

_STONE_MASK = 0x01
_ALIVE = 0x10
_CHECKED = 0x80


@dataclass(frozen=True)
class Move:
    """Record of one move of the Go game.
    """
    grid: list[list[int]] | None
    row: int
    col: int
    stone: int
    captures: list[tuple[int, int]] | None
    _c_stones: int


    def is_identical_grid(
        self,
        grid: list[list[int]],
        c_stones: int,
    ) -> bool:
        """To check if a given grid is exactly same as this moves'.

        Args:
            grid: The grid to compare.
            c_stones: number of stones on the grid for fast comparing.

        Returns:
            True if the grid completely identical with this moves',
            otherwise False.
        """
        return self._c_stones == c_stones and self.grid == grid


def _gridcopy(grid):
    return [line.copy() for line in grid]


class GoArbitor:
    """A Go game arbitor to record moves and determine whether they are
    valid.
    """
    def __init__(
        self,
        size: int = 19,
        first_move: int = BLACK_STONE,
        komi: float = 7.5
    ):
        """Initializes arbitor with parameters of the game info.
        """
        self._moves = []
        self._grid = [[None for _ in range(size)] for _ in range(size)]
        self._cur_stone = first_move
        self._c_captures = [0, 0]   # [balck, white]
        self._komi = komi

    # pylint: disable=too-many-arguments
    def _check_alive(self, grid, row, col, stone, captures=None):
        # Dectects alive state of a group of connected stones by recursion.
        # Dead stones will be stored in captures.
        #
        if not (0 <= row < len(grid) and 0 <= col < len(grid)):
            return False
        cur = grid[row][col]
        if cur is None:     # there is a liberty
            return True
        if cur != stone:    # opposite or checked stone
            if (cur & _STONE_MASK == stone) and (cur & _ALIVE):
                # A same camp stone has been checked and proved alive.
                return True
            return False
        grid[row][col] |= _CHECKED

        if (self._check_alive(grid, row, col - 1, stone, captures) or
                self._check_alive(grid, row - 1, col, stone, captures) or
                self._check_alive(grid, row, col + 1, stone, captures) or
                self._check_alive(grid, row + 1, col, stone, captures)):
            grid[row][col] |= _ALIVE
            return True

        if captures is not None:
            captures.append((row, col))
        return False


    def _check_around(self, grid, row, col, stone):
        # Checks opposite stones around the current, returns captures if
        # any of them aren't alive any more.
        #
        left_cpts = []
        if self._check_alive(grid, row, col - 1, stone, left_cpts):
            left_cpts.clear()
        upper_cpts = []
        if self._check_alive(grid, row - 1, col, stone, upper_cpts):
            upper_cpts.clear()
        right_cpts = []
        if self._check_alive(grid, row, col + 1, stone, right_cpts):
            right_cpts.clear()
        lower_cpts = []
        if self._check_alive(grid, row + 1, col, stone, lower_cpts):
            lower_cpts.clear()
        return left_cpts + upper_cpts + right_cpts + lower_cpts


    def _take_back(self, row, col, captures):
        opp_stone = not self._grid[row][col]
        self._grid[row][col] = None
        for point in captures:
            self._grid[point[0]][point[1]] = opp_stone
        self._c_captures[opp_stone] -= len(captures)


    def try_move(self, row: int, col: int) -> Move | None:
        """Try to make a move on a coordinate of the grid, returns the
        move record if success, otherwise returns None.
        """
        if self._grid[row][col] is not None:
            return None
        cur, opp = self._cur_stone, not self._cur_stone

        # Checks alive states of current and surrounding opposite stones.
        grid = [r.copy() for r in self._grid]
        grid[row][col] = cur
        captures = self._check_around(grid, row, col, opp)
        if not self._check_alive(grid, row, col, cur) and not captures:
            # A prohibited point for suicide.
            return None

        # Makes change
        for point in captures:
            self._grid[point[0]][point[1]] = None
        self._c_captures[opp] += len(captures)
        self._grid[row][col] = cur

        # Checks identical situation
        c_stones = len(self._moves) + 1 - sum(self._c_captures)
        for i in range(len(self._moves) - 1, -1, -1):
            if self._moves[i].is_identical_grid(
                    self._grid, c_stones):
                # Rollback for prohibition of the identical situation.
                self._take_back(row, col, captures)
                return None

        # Commits change
        self._moves.append(
                Move(_gridcopy(self._grid), row, col, cur, captures, c_stones))
        self._cur_stone = not self._cur_stone
        return self._moves[-1]


    def undo(self) -> Move | None:
        """Takes back a move from the game. Returns the move record on
        success, returns None if there aren't any moves.
        """
        if self._moves:
            move = self._moves.pop()
            if move.row >= 0:   # not a pass move
                self._take_back(move.row, move.col, move.captures)
            self._cur_stone = not self._cur_stone
            return move
        return None


    def pass_move(self) -> Move:
        """Makes a pass move. Always successly returns a move record
        with coordinate of (-1, -1).
        """
        self._moves.append(Move(None, -1, -1, self._cur_stone, None, 0))
        self._cur_stone = not self._cur_stone
        return self._moves[-1]


    @property
    def game_state(self) -> tuple[int, int, list[int], float]:
        """Game state in a tuple:
            (
            c_moves: int,
            current_stone: int,
            c_captures: [black: int, white: int],
            komi: float
            )
        """
        return len(self._moves), self._cur_stone, self._c_captures, self._komi

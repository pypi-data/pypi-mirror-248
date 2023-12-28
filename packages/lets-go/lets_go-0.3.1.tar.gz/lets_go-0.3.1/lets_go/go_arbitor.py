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


    def is_identical_grid(self, grid: list[list[int]], c_stones: int) -> bool:
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


def check_alive(grid, row, col, stone, captures):
    """Dectects alive state of a group of connected stones.

    Returns:
        True if the group of stones have liberties. Otherwise returns
        False with all stones be stored in captures.
        Functions does not clear the set flags on checked stones when
        return, for efficiecy of multi-times checking.
    """
    if not (0 <= row < len(grid) and 0 <= col < len(grid)):
        return False
    if (grid[row][col] is None or
        (grid[row][col] & _STONE_MASK == stone and grid[row][col] & _ALIVE)
        ):  # a liberty or an alive stone in same camp
        captures.clear()
        return True
    if grid[row][col] != stone:  # opposite or checked stone
        return False
    grid[row][col] |= _CHECKED

    if (check_alive(grid, row, col - 1, stone, captures) or
            check_alive(grid, row - 1, col, stone, captures) or
            check_alive(grid, row, col + 1, stone, captures) or
            check_alive(grid, row + 1, col, stone, captures)):
        grid[row][col] |= _ALIVE
        return True

    captures.append((row, col))
    return False


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


    def _check_around(self, grid, row, col, stone):
        # Checks opposite stones around the current, returns captures if
        # any of them aren't alive any more.
        #
        left_cps = []
        check_alive(grid, row, col - 1, stone, left_cps)
        upper_cps = []
        check_alive(grid, row - 1, col, stone, upper_cps)
        right_cps = []
        check_alive(grid, row, col + 1, stone, right_cps)
        lower_cps = []
        check_alive(grid, row + 1, col, stone, lower_cps)
        return left_cps + upper_cps + right_cps + lower_cps


    def _take_back(self, row, col, captures):
        opp_stone = not self._grid[row][col]
        self._grid[row][col] = None
        for point in captures:
            self._grid[point[0]][point[1]] = opp_stone
        self._c_captures[opp_stone] -= len(captures)


    def try_move(self, row: int, col: int) -> Move | None:
        """Tries to make a move on the specified coordinate of the grid,
        returns the move record if success, otherwise returns None.
        """
        if not (0 <= row < len(self._grid) and 0 <= col < len(self._grid)
                and self._grid[row][col] is None):
            return None
        cur, opp = self._cur_stone, not self._cur_stone

        # Checks alive states of current and surrounding opposite stones.
        grid = _gridcopy(self._grid)
        grid[row][col] = cur
        captures = self._check_around(grid, row, col, opp)
        if not check_alive(grid, row, col, cur, []) and not captures:
            return None  # prohibits suicide.

        # Makes change
        for point in captures:
            self._grid[point[0]][point[1]] = None
        self._c_captures[opp] += len(captures)
        self._grid[row][col] = cur

        # Checks identical situation
        c_stones = len(self._moves) + 1 - sum(self._c_captures)
        for move in reversed(self._moves):
            if move.is_identical_grid(self._grid, c_stones):
                # Rollback for prohibition of the identical situation.
                self._take_back(row, col, captures)
                return None

        # Commits change
        self._moves.append(
                Move(_gridcopy(self._grid), row, col, cur, captures, c_stones))
        self._cur_stone = not self._cur_stone
        return self._moves[-1]


    def undo(self) -> Move | None:
        """Takes back the last move from the game. Returns the move record
        on success, returns None if there aren't any moves.
        """
        if self._moves:
            move = self._moves.pop()
            if move.row >= 0:   # not a pass move
                self._take_back(move.row, move.col, move.captures)
            self._cur_stone = not self._cur_stone
            return move
        return None


    def pass_move(self) -> Move:
        """Makes a pass move. Always successly returns a move record with
        coordinate of (-1, -1).
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

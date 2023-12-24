#!/usr/bin/env python3
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

"""A simple Go game in character terminal environment.

No AI, no GTP, no joseki, no kifu, no tsumego, just playing for fun.
"""

import os

import color256 as co
from color256 import Color
import cursor
import termkey
from termkey import Key
from unicon import UnicodeIcon as UIcon

import go_arbitor as goa
import go_board as gob


STONES = (UIcon.BLACK_CIRCLE, UIcon.WHITE_CIRCLE)


def lets_go(
    board: gob.CursorGoBoard,
    text_bar: gob.TextBar,
    arbitor: goa.GoArbitor
):
    """Receives keyboard input to determine what to do.

    It is the controller of the game, uses GoBoard as the game view and
    GoArbitor as the logic and rule processor. This mode is well known as
    MVC.
    """
    def try_move():
        move = arbitor.try_move(board.cur_row, board.cur_col)
        if move:
            board.elem_in(board.cur_row, board.cur_col, STONES[move.stone])
            for point in move.captures:
                board.elem_out(point[0], point[1])
            return True
        return False

    def undo_move():
        move = arbitor.undo()
        if move:
            if move.row >= 0:   # not a pass move
                for point in move.captures:
                    board.elem_in(point[0], point[1], STONES[not move.stone])
                board.elem_out(move.row, move.col)
            return True
        return False

    key_funcs = {
        Key.SPACE: try_move,
        Key.UP: board.cursor_up,
        Key.DOWN: board.cursor_down,
        Key.RIGHT: board.cursor_right,
        Key.LEFT: board.cursor_left,
        ord('h'): board.cursor_left,
        ord('l'): board.cursor_right,
        ord('k'): board.cursor_up,
        ord('j'): board.cursor_down,
        ord('w'): lambda: board.cursor_right(3),
        ord('b'): lambda: board.cursor_left(3),
        ord('K'): lambda: board.cursor_up(3),
        ord('J'): lambda: board.cursor_down(3),
        ord('H'): board.cursor_top,
        ord('L'): board.cursor_bottom,
        ord('0'): board.cursor_leftmost,
        ord('$'): board.cursor_rightmost,
        ord('M'): board.cursor_center,
        Key.ESC: arbitor.pass_move,
        Key.DEL: undo_move,
        ord('u'): undo_move,
    }

    text_bar.add_blank_row()
    text_bar.add_text_row('SPACE: move   VI-KEYS: move cursor   '
                          'ESC: pass   DEL: undo   CTRL-X: exit')
    state_row = text_bar.add_blank_row()  # locate a row for state update
    text_bar.add_blank_row()

    key = termkey.getkey()
    while key != Key.CONTROL_X:
        if key_funcs.get(key, lambda: False)():
            moves, cur_stone, cps, komi = arbitor.game_state
            text_bar.update_row(state_row,
                f'Moves: {moves:<3d}    '
                f'Current Move: {STONES[cur_stone]}       '
                f'Captures: {STONES[0]} {cps[0]:<3d} {STONES[1]} {cps[1]:<3d}'
                f' Komi: {komi}')
        key = termkey.getkey()


def main():
    """Main entry of the lets-go game.

    Detects the terminal environment and setup a game view for playing.

    Raises:
        EnvironmentError: Screen too small to fit game.
    """
    scr_width, scr_height = os.get_terminal_size()
    if scr_width < 80 or scr_height < 43:
        raise EnvironmentError('Screen too small to fit game, 80x43 required.')
    o_row = (scr_height - 36) // 2 - 2
    o_col = (scr_width - 72) // 2

    cursor.switch_screen()
    cursor.clear_screen()
    cursor.hide_cursor()
    termkey.setparams(echo=False, intr=False)

    try:
        board = gob.CursorGoBoard(o_row, o_col)
        text_bar = board.text_bar_on()
        text_bar.color_scheme((Color.DEEP_KHAKI, Color.COFFEE,
                               Color.BLACK, Color.BRONZE))
        co.set_color(Color.BLACK, Color.BRONZE)
        board.refresh()
        board.show_coordinate_bar()
        board.cursor_on()
        arbitor = goa.GoArbitor()

        lets_go(board, text_bar, arbitor)
    finally:
        termkey.setparams()
        co.reset_color()
        cursor.show_cursor()
        cursor.restore_screen()


if __name__ == '__main__':
    main()

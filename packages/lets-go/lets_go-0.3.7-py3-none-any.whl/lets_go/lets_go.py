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

import ltermio
from ltermio import Color, TextAttr, Key, MouseEvent, UIcon

from .backend import GoBackend
from .board import CursorGoBoard, TextBar


STONES = (UIcon.BLACK_CIRCLE, UIcon.WHITE_CIRCLE)


def lets_go(
    board: CursorGoBoard,
    text_bar: TextBar,
    backend: GoBackend
):
    """Continuously reads key from keyboard, and dispatchs key events to
    appropriate functions.

    It is the controller of the game, uses GoBoard as the game view and
    GoBackend as the backend service. This mode is well known as MVC.
    """
    def place_move(move):
        if move:
            if move.row >= 0:   # not a pass move
                board.elem_in(move.row, move.col, STONES[move.stone])
                for point in move.cur_cpts:
                    board.elem_out(point[0], point[1])
            return True
        return False

    def takeback_move(move):
        if move:
            if move.row >= 0:   # not a pass move
                for point in move.cur_cpts:
                    board.elem_in(point[0], point[1], STONES[not move.stone])
                board.elem_out(move.row, move.col)
            return True
        return False

    def on_mouse(event, row, col, modifiers):
        if not modifiers:
            row, col = board.trans_screen_co(row, col)
            if event == MouseEvent.B_LEFT_CLICKED:
                return place_move(backend.try_move(row, col))
            if event == MouseEvent.B_RIGHT_CLICKED:
                return takeback_move(backend.undo())
            if event == MouseEvent.B_SCROLL_FORW:
                return place_move(backend.scroll_forw())
            if event == MouseEvent.B_SCROLL_BACK:
                return takeback_move(backend.scroll_back())
        return False

    key_funcs = {
        Key.SPACE: lambda: place_move(
            backend.try_move(board.cur_row, board.cur_col)
            ),
        Key.UP: board.cursor_up,
        Key.DOWN: board.cursor_down,
        Key.RIGHT: board.cursor_right,
        Key.LEFT: board.cursor_left,
        Key.RIGHT + Key.SHIFT: lambda: place_move(backend.scroll_forw()),
        Key.LEFT + Key.SHIFT: lambda: takeback_move(backend.scroll_back()),
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
        Key.ESC: backend.pass_move,
        Key.DEL: lambda: takeback_move(backend.undo()),
        ord('u'): lambda: takeback_move(backend.undo()),
    }

    ltermio.set_textattr(TextAttr.BOLD)
    text_bar.add_blank_row()
    text_bar.add_text_row(f'Move - {UIcon.MOUSE} LEFT, SPACE       '
                          f'Cursor - {UIcon.LEFT_ARROW} {UIcon.UP_ARROW} '
                          f'{UIcon.RIGHT_ARROW} {UIcon.DOWN_ARROW}      '
                          '        Pass - ESC')
    text_bar.add_text_row(
            f'Undo - {UIcon.MOUSE} RIGHT, DEL        '
            f'Scroll - {UIcon.MOUSE} WHEEL, '
            f'{UIcon.SHIFT}{UIcon.LEFT_ARROW} '
            f'{UIcon.SHIFT}{UIcon.RIGHT_ARROW}       '
            'Exit - CONTROL-X')
#    ltermio.set_textattr(TextAttr.NORMAL)
    text_bar.add_blank_row()
    state_row = text_bar.add_blank_row()  # locate a row for state update

    ltermio.set_mouse_mask(MouseEvent.B_LEFT_CLICKED |
                           MouseEvent.B_RIGHT_CLICKED |
                           MouseEvent.B_SCROLL_BACK |
                           MouseEvent.B_SCROLL_FORW)
    key = ltermio.getkey()
    while key != Key.CONTROL_X:
        if key_funcs.get(key,
                         lambda: (on_mouse(*ltermio.decode_mouse_event(key))
                                  if key > Key.MOUSE_EVENT else
                                  False)
                         )():
            c_moves, cur_stone, cps, komi = backend.game_state
            text_bar.update_row(state_row,
                f'Moves - {c_moves:<3d}   '
                f'Current Move - {STONES[cur_stone]}    '
                f'Captures - {STONES[0]} {cps[0]:<3d} {STONES[1]} {cps[1]:<3d}'
                f'    Komi - {komi}')
        key = ltermio.getkey()


@ltermio.appentry_args(mouse=True)
def main():
    """Main entry of the lets-go game.

    Detects the terminal environment and setup a game view for playing.

    Raises:
        EnvironmentError: Screen too small to fit game.
    """
    scr_width, scr_height = os.get_terminal_size()
    if scr_width < 80 or scr_height < 45:
        raise EnvironmentError('Screen too small to fit game, 80x45 required.')
    o_row = (scr_height - 36) // 2 - 2
    o_col = (scr_width - 72) // 2

    board = CursorGoBoard(o_row, o_col)
    text_bar = board.text_bar_on()
    text_bar.color_scheme((Color.DEEP_KHAKI, Color.COFFEE,
                           Color.BLACK, Color.BRONZE))
    ltermio.set_color(Color.BLACK, Color.BRONZE)
    board.refresh()
    board.show_coordinate_bar()
    board.cursor_on()
    backend = GoBackend()

    lets_go(board, text_bar, backend)

if __name__ == '__main__':
    main()

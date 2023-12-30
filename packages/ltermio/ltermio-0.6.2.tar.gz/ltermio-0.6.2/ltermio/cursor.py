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

r"""Wrapper functions of the CSI(Control Sequence Introducer) sequences about
cursor and screen.

A several of additional functions are provided for text composing:

    v_composing()
    downward_seq()
    vert_seq()
    rect_border_seq()

Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
           https://www.xfree86.org/current/ctlseqs.html
"""

import enum
from wcwidth import wcswidth


_CSI_LEAD = '\033['


def cursor_up_seq(num: int = 1):
    r"""Returns a sequence string that can move the cursor up 'num' rows.
    """
    return f'{_CSI_LEAD}{num}A'


def cursor_up(num: int = 1):
    r"""Moves the cursor up 'num' rows.
    """
    print(cursor_up_seq(num), end='', flush=True)


def cursor_down_seq(num: int = 1):
    r"""Returns a sequence string that can move the cursor down 'num' rows.
    """
    return f'{_CSI_LEAD}{num}B'


def cursor_down(num: int = 1):
    r"""Moves the cursor down 'num' rows.
    """
    print(cursor_down_seq(num), end='', flush=True)


def cursor_right_seq(num: int = 1):
    r"""Returns a sequence string that can move the cursor 'num' columns
    to right.
    """
    return f'{_CSI_LEAD}{num}C'


def cursor_right(num: int = 1):
    r"""Moves the cursor 'num' columns to right.
    """
    print(cursor_right_seq(num), end='', flush=True)


def cursor_left_seq(num: int = 1):
    r"""Returns a sequence string that can move the cursor 'num' columns
    to left.
    """
    return f'{_CSI_LEAD}{num}D'


def cursor_left(num: int = 1):
    r"""Moves the cursor 'num' columns to left.
    """
    print(cursor_left_seq(num), end='', flush=True)


def cursor_pos_seq(row: int, col: int):
    r"""Returns a sequence string that can move the cursor to the coordinate
    (row, col).
    """
    return f'{_CSI_LEAD}{row};{col}H'


def cursor_pos(row: int, col: int):
    r"""Moves the cursor to the coordinate (row, col).
    """
    print(cursor_pos_seq(row, col), end='', flush=True)


def putmsg(
    row: int,
    col: int,
    message: str,
    *args,
    end: str = '',
    flush: bool = True,
    **kwargs,
):
    r"""Moves the cursor to the coordinate (row, col), and prints message.

    Function sets flush to True and does not append '\n' at the end of
    the message by default.
    """
    print(f'{cursor_pos_seq(row, col)}{message}',
          *args, **kwargs, end=end, flush=flush)


def clear_screen():
    r"""Clears current screen buffer.
    """
    print(f'{_CSI_LEAD}2J', end='', flush=True)


def scroll_up(num: int = 1):
    r"""Scroll whole page up by 'num' rows. New rows are added at bottom.
    """
    print(f'{_CSI_LEAD}{num}S', end='', flush=True)


def scroll_down(num: int = 1):
    r"""Scroll whole page down by 'num' rows. New rows are added at top.
    """
    print(f'{_CSI_LEAD}{num}T', end='', flush=True)


def show_cursor():
    r"""Shows the cursor on screen.
    """
    print(f'{_CSI_LEAD}?25h', end='', flush=True)


def hide_cursor():
    r"""Hides the cursor from screen.
    """
    print(f'{_CSI_LEAD}?25l', end='', flush=True)


class CursorShape(enum.IntEnum):
    """Enumerates constants of the cursor shapes.
    """
    DEFAULT = 0
    BLOCK = 2
    UNDERLINE = 4
    BAR = 6


def set_cursor_shape(shape: CursorShape, blinking: bool = False):
    """Changes cursor shape to the 'shape'. Sets 'blinking' to True makes
    cursor to blink.
    """
    print(f'{_CSI_LEAD}{shape - blinking} q', end='', flush=True)


def switch_screen():
    r"""Uses alternate screen buffer to display message, it makes the content
    in the normal screen buffer remaining unchange.
    """
    print(f'{_CSI_LEAD}?47h', end='', flush=True)


def restore_screen():
    r"""Switches back to the normal screen buffer.
    """
    print(f'{_CSI_LEAD}?47l', end='', flush=True)


_COMP_FUNCS = {
    'h': cursor_left_seq,
    'l': cursor_right_seq,
    'k': cursor_up_seq,
    'j': cursor_down_seq,
}

def v_composing(comp_seq: str) -> str:
    r"""Generates text composing sequence.

    The parameter 'comp_seq' can use a series of VI like commands(hlkj)
    to specify relative cursor movements, using ':' command to insert
    text, and an ESC(\x1b) to back command mode. A numberic prefix can be
    added to the command to specify repetition times.

    Following sample code displays three big colorful greetings:

        from ltermio import putmsg, v_composing

        _P1 = ':{0}\x1b3hj'
        _P15 = ':{0}\x1b6l:{0}\x1b11hj'
        _DASH = '5:{0}\x1b11hj'
        _NEXT_POS = '5k17l'

        LETTERS = {
            'E': v_composing(f'{(_DASH + _P1) * 2}{_DASH}{_NEXT_POS}'),
            'H': v_composing(f'{_P15 * 2}{_DASH}{_P15 * 2}{_NEXT_POS}'),
            'L': v_composing(f'{_P1 * 4}{_DASH}{_NEXT_POS}'),
            'O': v_composing(f'{_DASH}{_P15 * 3}{_DASH}'),
        }

        greeting = ''.join(map(LETTERS.get, 'HELLO'))
        putmsg(3, 20, greeting.format('\u2b50'))
        putmsg(9, 14, greeting.format('\u2b55'))
        putmsg(15, 8, greeting.format('\U0001f7e2'))
        print('\n')

    Returns:
        A text composing sequnce that can be output to the screen in the
        expected shape.

    Raises:
        ValueError: Invalid composing sequence.
    """
    result = []
    index = repeat = 0

    while index < len(comp_seq):
        cmd = comp_seq[index]
        index += 1
        if cmd.isdigit():
            repeat = repeat * 10 + int(cmd)
        elif cmd in _COMP_FUNCS:
            result.append(_COMP_FUNCS[cmd](repeat if repeat else 1))
            repeat = 0
        elif cmd == ':':  # In insertion mode
            esc = comp_seq.find('\x1b', index)
            if esc < 0:
                result.append(comp_seq[index:] * (repeat if repeat else 1))
                break
            result.append(comp_seq[index:esc] * (repeat if repeat else 1))
            repeat = 0
            index = esc + 1
        elif cmd != '\x1b':
            raise ValueError('Invalid composing sequence')
        # else: ignores redundant ESC(\x1b)
    return ''.join(result)


def downward_seq(text: str, back_cols: int) -> str:
    r"""Generates a text sequence that makes subsequent text to be output
    in downward direction.

    After the result text be output to screen, the cursor takes 'back_cols'
    columns back from the end position of the output and moves to the next
    line.

    The following example code draws a triangle on screen:

        putmsg(1, 40, downward_seq('\u2b50', 3) * 24)
        putmsg(1, 40, downward_seq('\u2b50', 1) * 24)
        putmsg(24, 17, '\u2b50' * 24)
    """
    return v_composing(f':{text}\x1b{back_cols}hj')


def vert_seq(text:str) -> str:
    r"""Generates a text sequence that makes subsequent text be output in
    vertical downward direction.

    It is just a simple wapper of the downward_seq().
    """
    return downward_seq(text, wcswidth(text))


def rect_border_seq(width: int, height: int, sym: str) -> str:
    r"""Generates a text sequence that draws a rectangle border.
    """
    sym_w = wcswidth(sym)
    hori_border = f':{sym * width}\x1b{sym_w * width}hj'
    vert_borders = ((f':{sym}\x1b{sym_w * (width - 2)}l'
                     f':{sym}\x1b{sym_w * width}hj') * (height - 2))
    return v_composing(hori_border + vert_borders + hori_border)


def _test_cursor():
    def greeting_show():
        p10 = ':{0}\x1b3hj'
        p00001 = '8l:{0}\x1b11hj'
        p10001 = ':{0}\x1b6l:{0}\x1b11hj'
        p1001 = ':{0}\x1b4l:{0}\x1b9hj'
        dash = '5:{0}\x1b11hj'
        next_pos = '5k17l'
        letters = {
            'C': v_composing(f'{dash}{p10 * 3}{dash}{next_pos}'),
            'E': v_composing(f'{(dash + p10) * 2}{dash}{next_pos}'),
            'H': v_composing(f'{p10001 * 2}{dash}{p10001 * 2}{next_pos}'),
            'L': v_composing(f'{p10 * 4}{dash}{next_pos}'),
            'O': v_composing(f'{dash}{p10001 * 3}{dash}{next_pos}'),
            'R': v_composing(f'{dash}{p10001}{dash}{p1001}{p10001}{next_pos}'),
            'S': v_composing(f'{dash}{p10}{dash}{p00001}{dash}{next_pos}'),
            'U': v_composing(f'{p10001 * 4}{dash}{next_pos}'),
        }
        # Here letters.get() never returns None.
        # pytype: disable=wrong-arg-types
        hello = ''.join(map(letters.get, 'HELLO'))
        cursor = ''.join(map(letters.get, 'CURSOR'))
        # pytype: enable=wrong-arg-types
        putmsg(4, 20, hello.format('\U0001f7e4'))
        putmsg(10, 14, hello.format('\U0001f7e0'))
        putmsg(16, 8, cursor.format('\U0001f7e1'))

    def frame_show():
        putmsg(4, 2, rect_border_seq(39, 18, '\u2b50'))
        putmsg(1, 40, downward_seq('\U0001f339', 3) * 24)
        putmsg(1, 40, downward_seq('\U0001f339', 1) * 24)
        putmsg(24, 17, '\U0001f339' * 24)

    switch_screen()
    clear_screen()
    hide_cursor()
    try:
        greeting_show()
        cursor_pos(24, 1)
        input('Enter to continue.')
        clear_screen()
        frame_show()
        cursor_pos(24, 1)
        input('Enter to exit.')
    finally:
        show_cursor()
        restore_screen()


if __name__ == '__main__':
    _test_cursor()

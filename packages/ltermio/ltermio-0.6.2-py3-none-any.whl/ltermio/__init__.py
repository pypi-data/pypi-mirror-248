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

r"""A lightweight POSIX character terminal I/O library.

Repo - https://github.com/brookssu/ltermio.git
"""

import functools

from .color256 import (
    rgb,
    Color,
    set_fcolor,
    reset_fcolor,
    set_bcolor,
    reset_bcolor,
    set_color,
    reset_color,
    TextAttr,
    set_textattr,
    reset_textattr,
)
from .cursor import (
    cursor_up,
    cursor_down,
    cursor_right,
    cursor_left,
    cursor_pos,
    putmsg,
    clear_screen,
    scroll_up,
    scroll_down,
    show_cursor,
    hide_cursor,
    switch_screen,
    restore_screen,
    v_composing,
    downward_seq,
    vert_seq,
    rect_border_seq,
    CursorShape,
    set_cursor_shape,
)
from .termkey import (
    getch,
    ungetch,
    Key,
    ungetkey,
    setparams,
    getkey,
)
from .termouse import (
    mouse_tracking_on,
    mouse_tracking_off,
    MouseEvent,
    set_mouse_mask,
    set_click_interval,
    decode_mouse_event,
)
from .unicon import UnicodeIcon as UIcon


__version__ = '0.6.2'
__all__ = ['color256', 'cursor', 'termkey', 'termouse', 'unicon',]


def appentry(func):
    r"""A decorator of the ltermio application entry.

    Before enters entry function, the decorator switchs and clears
    screen, disables input echo and keyboard interrupts, and hides
    cursor.
    And after the entry function returns, the decorator restores
    screen, shows cursor, resets color, and enables input echo and
    keyboard interrupts.

    Another parameterized decorator appentry_args() supports more
    flexible customizing.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        switch_screen()
        clear_screen()
        setparams(echo=False, intr=False)
        hide_cursor()
        try:
            return func(*args, **kwargs)
        finally:
            show_cursor()
            reset_color()
            setparams()
            restore_screen()
    return wrapper


def appentry_args(*, echo=False, intr=False, cursor=False, mouse=False):
    r"""A parameterized decorator of the ltermio application entry.

    Before enters entry function, the decorator switchs and clears
    screen, sets cursor and other input attributes according to the
    parameters.
    And after the entry function returns, the decorator restores screen,
    and reset cursor, color and other set attributes.

    Args:
        echo: Echoes input characters if True, False to disable.
        intr: False to disable keyboard interrupt signals.
        cursor: False to hide cursor while True to show.
        mouse: True to enable mouse tracking.
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            switch_screen()
            clear_screen()
            setparams(echo=echo, intr=intr)
            if not cursor:
                hide_cursor()
            if mouse:
                mouse_tracking_on()
            try:
                return func(*args, **kwargs)
            finally:
                mouse_tracking_off()
                show_cursor()
                reset_color()
                setparams()
                restore_screen()
        return inner
    return wrapper

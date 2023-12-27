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

"""Detects and reports mouse events.

The implementation of the module follows the XTerm specification of the
mouse tracking and uses normal tracking mode, see also:

    https://www.xfree86.org/current/ctlseqs.html#Mouse%20Tracking

Calls ltermio.mouse_tracking_on() to turn on the mouse tracking, or sets
the parameter `mouse=True` on the decorator ltermio.appentry().

The mouse events are reported by ltermio.getkey(), with value encoded in
a 32-bits integer and larger than Key.MOUSE_EVENT. It is simple to make
difference from normal key code by `code > Key.MOUSE_EVENT`.
Decodes the event code by calling ltermio.decode_mouse_event() which
returns a tuple with explicit items.
"""

import time
from enum import IntEnum

from .termkey import getkey, setparams, mouse_handler, Key


# Constants of mouse tracking modes
_NORMAL_TRACKING = 1000
#_HILITE_TRACKING = 1001
#_CELL_MOTION_TRACKING = 1002
#_ANY_MOTION_TRACKING = 1003


class MouseEvent(IntEnum):
    """Enum constants of the mouse events.
    """
    B1_PRESSED = 0x0002_0000
    B1_RELEASED = 0x0004_0000
    B1_CLICKED = 0x0008_0000
    B2_PRESSED = 0x0010_0000
    B2_RELEASED = 0x0020_0000
    B2_CLICKED = 0x0040_0000
    B3_PRESSED = 0x0080_0000
    B3_RELEASED = 0x0100_0000
    B3_CLICKED = 0x0200_0000
    B4_PRESSED = 0x0400_0000
    B4_RELEASED = 0x0800_0000
    B4_CLICKED = 0x1000_0000
    B5_PRESSED = 0x2000_0000
    B5_RELEASED = 0x4000_0000
    B5_CLICKED = 0x8000_0000


_MOUSE_EVENTS = (
    (MouseEvent.B1_PRESSED, MouseEvent.B1_RELEASED, MouseEvent.B1_CLICKED),
    (MouseEvent.B2_PRESSED, MouseEvent.B2_RELEASED, MouseEvent.B2_CLICKED),
    (MouseEvent.B3_PRESSED, MouseEvent.B3_RELEASED, MouseEvent.B3_CLICKED),
    (MouseEvent.B4_PRESSED, MouseEvent.B4_RELEASED, MouseEvent.B4_CLICKED),
    (MouseEvent.B5_PRESSED, MouseEvent.B5_RELEASED, MouseEvent.B5_CLICKED),
)
_PRESSED_INDEX = 0
_RELEASED_INDEX = 1
_CLICKED_INDEX = 2


# pylint: disable=invalid-name
# pylint: disable=global-statement
_mouse_mask: int = 0xfffe_0000
_pressed_button: int = 0
_pressed_time: float = 0.
_click_interval: float = 0.2  # seconds


def _tracking_on(mode: int):
    # DEC private mode set(DECSET)
    print(f'\033[?{mode}h', end='', flush=True)


def _tracking_off(mode: int):
    # DEC private mode reset(DECRST)
    print(f'\033[?{mode}l', end='', flush=True)


def mouse_tracking_on():
    """Truns on mouse tracking.
    """
    mouse_handler(_on_mouse_event)
    _tracking_on(_NORMAL_TRACKING)


def mouse_tracking_off():
    """Truns off mouse tracking.
    """
    _tracking_off(_NORMAL_TRACKING)
    mouse_handler(None)


def set_mouse_mask(mask: int):
    """Sets the mouse events to be reported.

    If turns mouse tracking on and does not call this function, all
    mouse events are reported by default.

    Args:
        mask: A bitwise combination of the mouse events, e.g.
            MouseEvent.B1_CLICKED + MouseEvent.B3_CLICKED
    """
    global _mouse_mask
    _mouse_mask = mask


def set_click_interval(interval: float):
    """Sets the maximum time limit between press and release in order
    that code can recognize them as one click.

    When a CLICKED event occurs, it also means that a RELEASED event
    has occurred at the same time.  In this case, ltermio does not
    report two events but only reports the CLICKED, or only reports
    the RELEASED when the CLICKED event is masked.

    Args:
        interval: time interval in seconds, the default value is 0.2s.
    """
    global _click_interval
    _click_interval = interval


def decode_mouse_event(code: int) -> tuple[int, int, int, int]:
    """Decodes the mouse event code into a tuple.

    Args:
        code: The mouse event code that returns by ltermio.getkey(), which
            can be determined by `code > Key.MOUSE_EVENT`.

    returns:
        A tuple with 4 items: (event, row, col, modifiers):
        event: One of the mouse events which defined in the module.
        row, col: Screen coordinate of the mouse when the event occurs.
        modifiers: Modifier keys(Shift, Alt or Meta, Control) that be
            pressed when the event occurs, their values are identical
            to their values in ltermio.Key.
    """
    return (code & 0xfffe0000,  # event
            (code & 0x3f80) >> 7,  # row
            code & 0x7f,  # col
            (code & 0x1c000) >> 6)  # modifiers


def _on_mouse_event(data: int, col: int, row: int) -> int:
    global _pressed_button, _pressed_time

    button = data & 0x03
    # Encodes modifiers, row and col into lower 17 bits of the event code.
    lower = ((data & 0x1c) << 12) | (row << 7) | col

    if button == 3:  # Button released
        if time.perf_counter() - _pressed_time < _click_interval:
            event = _MOUSE_EVENTS[_pressed_button][_CLICKED_INDEX]
            if _mouse_mask & event:
                return event | lower
        event = _MOUSE_EVENTS[_pressed_button][_RELEASED_INDEX]
        return (event | lower) if (_mouse_mask & event) else Key.NONE

    # Button pressed
    if data >= 64:  # Wheel mouse returns button 4 or 5
        if button > 1:
            return Key.NONE
        button += 3
    _pressed_button = button
    _pressed_time = time.perf_counter()
    event = _MOUSE_EVENTS[button][_PRESSED_INDEX]
    return (event | lower) if (_mouse_mask & event) else Key.NONE


def _test_termouse():
    mouse_tracking_on()
#    set_mouse_mask(MouseEvent.B3_CLICKED + MouseEvent.B1_CLICKED)
    setparams(echo=False, intr=False)
    code = getkey()
    while code != Key.CONTROL_X:
        code = getkey()
        if code > Key.MOUSE_EVENT:
            event, row, col, modifiers = decode_mouse_event(code)
            print(f'e:{event:08x} y:{row} x:{col} m:{modifiers:04x}')
    setparams()
    mouse_tracking_off()


if __name__ == '__main__':
    _test_termouse()

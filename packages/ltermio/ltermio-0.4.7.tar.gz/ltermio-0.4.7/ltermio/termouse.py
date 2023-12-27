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
the parameter `mouse=True` on the ltermio.appentry() decorator.

The mouse events are reported by ltermio.getkey(), with value encoded in
a 32-bits integer and larger than Key.MOUSE_EVENT. It is simple to make
difference from normal key code by `code > Key.MOUSE_EVENT`.
Decodes the code by calling ltermio.decode_mouse_event() which returns a
tuple with explicit items.
"""

import time

from .termkey import getkey, setparams, mouse_handler, Key


# Constants of mouse tracking modes
_NORMAL_TRACKING = 1000
#_HILITE_TRACKING = 1001
#_CELL_MOTION_TRACKING = 1002
#_ANY_MOTION_TRACKING = 1003


# Constants of mouse events. For wheel mice, button 4 and 5 should never
# release and click but just reserved.
MB1_PRESSED = 0x0002_0000
MB1_RELEASED = 0x0004_0000
MB1_CLICKED = 0x0008_0000
MB2_PRESSED = 0x0010_0000
MB2_RELEASED = 0x0020_0000
MB2_CLICKED = 0x0040_0000
MB3_PRESSED = 0x0080_0000
MB3_RELEASED = 0x0100_0000
MB3_CLICKED = 0x0200_0000
MB4_PRESSED = 0x0400_0000
MB4_RELEASED = 0x0800_0000
MB4_CLICKED = 0x1000_0000
MB5_PRESSED = 0x2000_0000
MB5_RELEASED = 0x4000_0000
MB5_CLICKED = 0x8000_0000

_MOUSE_EVENTS = (
    (MB1_PRESSED, MB1_RELEASED, MB1_CLICKED),
    (MB2_PRESSED, MB2_RELEASED, MB2_CLICKED),
    (MB3_PRESSED, MB3_RELEASED, MB3_CLICKED),
    (MB4_PRESSED, MB4_RELEASED, MB4_CLICKED),
    (MB5_PRESSED, MB5_RELEASED, MB5_CLICKED),
)
_PRESSED_INDEX = 0
_RELEASED_INDEX = 1
_CLICKED_INDEX = 2


# pylint: disable=invalid-name
# pylint: disable=global-statement
_mouse_mask: int = 0xfffe_0000
_last_button: int = 0
_last_time: float = 0.
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

    If turns mouse tracking on and never calls this function, all mouse
    events are reported by default.

    Args:
        mask: A bitwise combination of mouse events, e.g.
            ltermio.MB1_CLICKED + ltermio.MB3_CLICKED
    """
    global _mouse_mask
    _mouse_mask = mask


def set_click_interval(interval: float):
    """Sets the maximum time limit between press and release in order
    that code can recognize them as one click.

    When a CLICKED occurs, it also means that a RELEASED event occurred.
    In this situation, ltermio does not report two events, but only the
    CLICKED be reported. 

    Args:
        interval: time interval in seconds, the default value is 0.2 s.
    """
    global _click_interval
    _click_interval = interval


def decode_mouse_event(code: int) -> tuple[int, int, int, int]:
    """Decodes the mouse event code into a tuple.

    Args:
        code: The mouse event code that returns by ltermio.getkey(), which
            can be determined by `code > Key.MOUSE_EVENT`.

    returns:
        A tuple with 4 items: (event, row, col, modifiers).
            event: One of the mouse events which defined in the module.
            row, col: Screen coordinate of the mouse when the event occurs.
            modifiers: Modifier keys(Shift, Alt or Meta, Control) that be
                pressed when the event occurs, their values are identical
                to the values in ltermio.Key.
    """
    return (code & 0xfffe0000,  # event
            (code & 0x3f80) >> 7,  # row
            code & 0x7f,  # col
            (code & 0x1c000) >> 6)  # modifiers


def _on_mouse_event(data: int, col: int, row: int) -> int:
    global _last_button, _last_time

    button = data & 0x03
    modifiers = (data & 0x1c) << 12
    if button == 3:  # button released
        event = _MOUSE_EVENTS[_last_button][
                    _CLICKED_INDEX
                    if (time.perf_counter() - _last_time) < _click_interval
                    else
                    _RELEASED_INDEX
                ]
        return ((event | modifiers | (row << 7) | col)
                if (_mouse_mask & event) else
                Key.NONE)
    # button pressed
    if data >= 64:  # wheel mouse returns button 4 or 5
        if button > 1:
            return Key.NONE
        button += 3
    _last_button = button
    _last_time = time.perf_counter()
    event = _MOUSE_EVENTS[button][_PRESSED_INDEX]
    return ((event | modifiers | (row << 7) | col)
            if (_mouse_mask & event) else
            Key.NONE)


def _test_termouse():
    mouse_tracking_on()
    set_mouse_mask(MB3_PRESSED + MB1_CLICKED)
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

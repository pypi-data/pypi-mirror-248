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

r"""Detects and reports mouse events.

The implementation of the module follows the XTerm specification of the
mouse tracking and uses normal tracking mode, see also:

    https://www.xfree86.org/current/ctlseqs.html#Mouse%20Tracking
    https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Mouse-Tracking

Calls ltermio.mouse_tracking_on() to turn on the mouse tracking, or sets
the parameter `mouse=True` on the decorator ltermio.appentry_args().

The mouse events are reported by ltermio.getkey(), with value encoded in
a 32-bits integer and larger than Key.MOUSE_EVENT. It is simple to make
difference from normal key codes by `code > Key.MOUSE_EVENT`.
Decodes the event codes by calling ltermio.decode_mouse_event() which
returns a tuple with explicit items.

An example to get key and mouse inputs as following:

    from ltermio import Key, MouseEvent

    ltermio.mouse_tracking_on()
    ltermio.setparams(echo=False)

    code = ltermio.getkey()
    while code != Key.CONTROL_X:
        if code > Key.MOUSE_EVENT:
            event, row, col, modifiers = ltermio.decode_mouse_event(code)
            if event == MouseEvent.B1_CLICKED:
                ... # do something with mouse event
        else:
            ... # do something with key input
        code = ltermio.getkey()

    ltermio.setparams(echo=True)
    ltermio.mouse_tracking_off()
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
    r"""Enum constants of the mouse events.

    There are 3 types of events for buttons 1, 2 and 3: PRESSED, RELEASED
    and CLICKED. Buttons 4~7 PRESSEDs are defined for wheel mice, but they
    have only PRESSED event for wheel buttons have no releases.
    """
    B1_PRESSED  = 0x0008_0000
    B1_RELEASED = 0x0010_0000
    B1_CLICKED  = 0x0020_0000
    B2_PRESSED  = 0x0040_0000
    B2_RELEASED = 0x0080_0000
    B2_CLICKED  = 0x0100_0000
    B3_PRESSED  = 0x0200_0000
    B3_RELEASED = 0x0400_0000
    B3_CLICKED  = 0x0800_0000

    B4_PRESSED  = 0x1000_0000
    B5_PRESSED  = 0x2000_0000
    B6_PRESSED  = 0x4000_0000
    B7_PRESSED  = 0x8000_0000

    # Aliases for B1_XXX
    B_LEFT_PRESSED = B1_PRESSED
    B_LEFT_RELEASED = B1_RELEASED
    B_LEFT_CLICKED = B1_CLICKED

    # Aliases for B2_XXX
    B_MIDDLE_PRESSED = B2_PRESSED
    B_MIDDLE_RELEASED = B2_RELEASED
    B_MIDDLE_CLICKED = B2_CLICKED

    # Aliases for B3_XXX
    B_RIGHT_PRESSED = B3_PRESSED
    B_RIGHT_RELEASED = B3_RELEASED
    B_RIGHT_CLICKED = B3_CLICKED

    B_SCROLL_BACK = B4_PRESSED  # Alias for B4_PRESSED
    B_SCROLL_FORW = B5_PRESSED  # Alias for B5_PRESSED


_MOUSE_EVENTS = (
    (MouseEvent.B1_PRESSED, MouseEvent.B1_RELEASED, MouseEvent.B1_CLICKED),
    (MouseEvent.B2_PRESSED, MouseEvent.B2_RELEASED, MouseEvent.B2_CLICKED),
    (MouseEvent.B3_PRESSED, MouseEvent.B3_RELEASED, MouseEvent.B3_CLICKED),
    (MouseEvent.B4_PRESSED,),
    (MouseEvent.B5_PRESSED,),
    (MouseEvent.B6_PRESSED,),
    (MouseEvent.B7_PRESSED,),
)
_PRESSED_INDEX = 0
_RELEASED_INDEX = 1
_CLICKED_INDEX = 2


# pylint: disable=invalid-name
# pylint: disable=global-statement
_mouse_mask: int = 0xfff8_0000
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
    r"""Truns on mouse tracking.
    """
    mouse_handler(_on_mouse_event)
    _tracking_on(_NORMAL_TRACKING)


def mouse_tracking_off():
    r"""Truns off mouse tracking.
    """
    _tracking_off(_NORMAL_TRACKING)
    mouse_handler(None)


def set_mouse_mask(mask: int):
    r"""Sets the mouse events to be reported.

    If turns mouse tracking on and does not call this function, all
    mouse events are reported by default.

    Args:
        mask: A bitwise combination of the mouse events, e.g.
            MouseEvent.B1_CLICKED + MouseEvent.B3_CLICKED
    """
    global _mouse_mask
    _mouse_mask = mask


def set_click_interval(interval: float):
    r"""Sets the maximum time limit between press and release in order
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
    r"""Decodes the mouse event code into a tuple.

    Args:
        code: The mouse event code that returns by ltermio.getkey(), which
            can be determined by `code > Key.MOUSE_EVENT`.

    returns:
        A tuple with 4 items: (event, row, col, modifiers):
        event: One of the mouse events which defined in the MouseEvent.
        row, col: Screen coordinate of the mouse when the event occurs.
        modifiers: Modifier keys(Shift, Alt or Meta, Control) that be
            pressed when the event occurs, their values are identical
            to their values in ltermio.Key.
    """
    return (code & 0xfff8_0000,  # event
            (code & 0xff00) >> 8,  # row
            code & 0xff,  # col
            (code & 0x7_0000) >> 4)  # modifiers


def _on_mouse_event(data: int, col: int, row: int) -> int:
    global _pressed_button, _pressed_time

    # On button press or release, xterm sends CSI M Cb Cx Cy. The low two
    # bits of Cb(data) encode button information:
    #       0=B1 pressed, 1=B2 pressed, 2=B3 pressed, 3=release.
    # The next three bits encode the modifiers which were down when the
    # button was pressed and are added together:
    #       4=Shift, 8=Alt(Meta), 16=Control.
    button = data & 0x03

    # Encodes modifiers, row and col into lower 19 bits of the event code:
    #       0~7: col, 8~15: row, 16~18: modifiers
    lower = ((data & 0x1c) << 14) | (row << 8) | col

    # if data >= 128:
    #     ? buttons 8~11 not supports yet, just ignores to treat them as
    #     buttons 4~7.
    #
    if data >= 64:
        # Wheel mice may return buttons 4 ~ 7. Those buttons are also
        # represented by the low two bits of Cb, except that 64 is added
        # to the event data.
        button += 3
    elif button == 3:  # Button released
        if time.perf_counter() - _pressed_time < _click_interval:
            event = _MOUSE_EVENTS[_pressed_button][_CLICKED_INDEX]
            if _mouse_mask & event:
                return event | lower
        event = _MOUSE_EVENTS[_pressed_button][_RELEASED_INDEX]
        return (event | lower) if (_mouse_mask & event) else Key.NONE
    else:  # data < 64 and button != 3
        # Saves PRESSED event for CLICKED event, but just buttons 1~3 for
        # release events for the wheel buttons are not reported.
        _pressed_button = button
        _pressed_time = time.perf_counter()
    event = _MOUSE_EVENTS[button][_PRESSED_INDEX]
    return (event | lower) if (_mouse_mask & event) else Key.NONE


def _mdf_names(code):
    modifiers = []
    if code & Key.SHIFT:
        modifiers.append(Key.SHIFT.name)
    if code & Key.ALT:
        modifiers.append(Key.ALT.name)
    if code & Key.CONTROL:
        modifiers.append(Key.CONTROL.name)
    if code & Key.META:
        modifiers.append(Key.META.name)
    return ' '.join(modifiers)


def _test_termouse():
    mouse_tracking_on()
    setparams(echo=False, intr=False)
    print('Press any key or click mouse to get code, CONTROL-X to exit.')
    code = getkey()
    while code != Key.CONTROL_X:
        if code < Key.MOUSE_EVENT:
            print(f'Key code({code:04X}) - char({chr(code)!r})'
                  f' {_mdf_names(code)}')
        else:
            event, row, col, modifiers = decode_mouse_event(code)
            print(f'Mouse code({code:08X}) - {MouseEvent(event).name}'
                  f'({row}, {col}) {_mdf_names(modifiers)}')
        code = getkey()
    setparams()
    mouse_tracking_off()


if __name__ == '__main__':
    _test_termouse()

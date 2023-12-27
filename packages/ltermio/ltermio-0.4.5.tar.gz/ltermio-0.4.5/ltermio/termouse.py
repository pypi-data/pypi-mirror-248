#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from .termkey import getkey, setparams, mouse_handler, Key


# Constants of mouse tracking modes
_NORMAL_TRACKING = 1000
#_HILITE_TRACKING = 1001
#_CELL_MOTION_TRACKING = 1002
#_ANY_MOTION_TRACKING = 1003


# Constants of mouse events. For wheel mice, button4 and 5 should never
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
    mouse_handler(_on_mouse_event)
    _tracking_on(_NORMAL_TRACKING)


def mouse_tracking_off():
    mouse_handler(None)
    _tracking_off(_NORMAL_TRACKING)


def set_mouse_mask(mask: int):
    global _mouse_mask
    _mouse_mask = mask


def set_click_interval(interval: float):
    global _click_interval
    _click_interval = interval


def decode_mouse_event(event: int):
    return (event & 0xfffe0000,
            (event & 0x3f80) >> 7,
            event & 0x7f,
            (event & 0x1c000) >> 6)


def _on_mouse_event(data: int, col: int, row: int) -> int:
    global _last_button, _last_time, _click_interval

    button = data & 0x03
    modifiers = (data & 0x1c) << 12
    if button == 3:  # button released
        event = _MOUSE_EVENTS[_last_button][
                    _CLICKED_INDEX
                    if (time.perf_counter() - _last_time) < _click_interval
                    else
                    _RELEASED_INDEX
                ]
        return ((event | modifiers | (col << 7) | row)
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
    return ((event | modifiers | (col << 7) | row)
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
            event, col, row, modifiers = decode_mouse_event(code)
            print(f'event:{event:08x} col:{col} row:{row} m:{modifiers:04x}')
    setparams()
    mouse_tracking_off()


if __name__ == '__main__':
    _test_termouse()

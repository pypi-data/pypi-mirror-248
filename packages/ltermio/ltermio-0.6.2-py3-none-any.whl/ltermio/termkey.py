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

r"""Functions to read input in non-canonical mode.

There are 5 curses like functions:

    getch(): Gets a character from stdin.
    ungetch(): Puts one or more characters into the key buffer.
    getkey(): Calls getch() and transforms character to keycode.
    ungetkey(): Puts a keycode into the key buffer.
    setparams(): Sets frenquently-used attributes of the input.

And a function to support mouse tracking.

    mouse_handler(): Sets a function to handle mouse report.

Function keycodes in common using are defined in enum class Key.

A typical usage example as following:

    import ltermio
    from ltermio import Key

    ltermio.setparams(echo=False)
    key = ltermio.getkey()
    while key != Key.ESC:
        ...
        key = ltermio.getkey()
    ltermio.setparams()

Applicability: Implementations are base on XTerm specification and
termios, so they are only for POSIX terminal applications.
"""

import re
import sys
import termios
from enum import IntEnum


_ch_buffer = []

BLOCKING_ = -1

def getch(timeout: int = BLOCKING_) -> str:
    r"""Gets a character from stdin with non-canonical mode.

    Instead of waiting for a CR in canonical mode, function returns
    immediately once read a key.

    Args:
        timeout: An integer to specify a waiting time in units of 1/10
            second. If timeout = BLOCKING_, function will block until
            read a charactor, otherwise returns immediately if timeout
            occurs, regardless of whether a charactor is read or not.

    Returns:
        A character in string if successful reading. Otherwise returns
        an empty string '' when timeout.
    """
    if _ch_buffer:
        return _ch_buffer.pop(0)

    in_fd = sys.stdin.fileno()
    # The Python termios flags is a list, as following:
    #   [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    old_flags = termios.tcgetattr(in_fd)
    new_flags = old_flags[:]
    new_flags[6] = old_flags[6][:]

    # Sets lflag(local flag) to non-canonical mode
    new_flags[3] &= ~termios.ICANON

    # Sets cc(control characters): At least reads 1 character in blocking
    # mode, otherwise 0 with a specific timeout.
    if timeout == BLOCKING_:
        new_flags[6][termios.VMIN] = 1
    else:
        new_flags[6][termios.VMIN] = 0
        # Sets minimal waiting time, in units of 1/10 second.
        new_flags[6][termios.VTIME] = timeout

    try:
        termios.tcsetattr(in_fd, termios.TCSANOW, new_flags)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(in_fd, termios.TCSANOW, old_flags)


def ungetch(key_chs: str):
    r"""Puts one or more key characters into the key buffer in order that
    following getch() or getkey() can read it(them).
    """
    _ch_buffer.extend(key_chs)


def ungetkey(key_code: int):
    r"""Puts a key code into the key buffer in order that following getch()
    or getkey() can read it.
    """
    _ch_buffer.append(chr(key_code))


def setparams(*, echo: bool = True, intr: bool = True):
    r"""Sets frequently-used attributes of the input(stdin).

    Args:
        echo: Echoes input characters if True, otherwise does not echo
            (also known as password mode).
        intr: If True, system generates keyboard interrupt signals when
            read special keys(e.g. Control-C). Sets it to False to treat
            them as normal keys.
    """
    in_fd = sys.stdin.fileno()
    flags = termios.tcgetattr(in_fd)
    flags[3] = ((flags[3] | termios.ECHO | termios.ECHONL)
                if echo else
                (flags[3] & ~(termios.ECHO | termios.ECHONL)))
    flags[3] = ((flags[3] | termios.ISIG)
                if intr else
                (flags[3] & ~termios.ISIG))
    termios.tcsetattr(in_fd, termios.TCSANOW, flags)


class Key(IntEnum):
    r"""Defines function key codes that returns by getkey().

    The normal key codes here are 16 bit integers: The single-byte keys
    are simply transformed by ord() function, and the multi-bytes CSI
    sequence keys are pesudo codes that begin from 0x101. Function key
    modifiers defined as bitmasks that could be combined with other key
    codes, like: CONTROL + SHIFT + F5

    To support mouse tracking, an indicator code MOUSE_EVENT additionally
    defined in the class. All mouse event codes that returns by getkey()
    are larger than the indicator while all normal key codes smaller
    than it.

    The term 'CSI sequences key' here refers to key sequences lead with
    '\\033['(CSI) or '\\033O'(SS3) in XTerm specification.
    reference: https://www.xfree86.org/current/ctlseqs.html
    """

    NONE        = 0x0000
    BELL        = 0x07
    BACKSPACE   = 0x08
    TAB         = 0x09
    ENTER       = 0x0A
    ESC         = 0x1B
    SPACE       = 0x20
    DEL         = 0x7F
    CONTROL_A   = 0x01
    CONTROL_B   = 0x02
    CONTROL_C   = 0x03
    CONTROL_D   = 0x04
    CONTROL_E   = 0x05
    CONTROL_F   = 0x06
    CONTROL_G   = 0x07
    CONTROL_H   = 0x08
    CONTROL_I   = 0x09
    CONTROL_J   = 0x0A
    CONTROL_K   = 0x0B
    CONTROL_L   = 0x0C
    CONTROL_M   = 0x0D
    CONTROL_N   = 0x0E
    CONTROL_O   = 0x0F
    CONTROL_P   = 0x10
    CONTROL_Q   = 0x11
    CONTROL_R   = 0x12
    CONTROL_S   = 0x13
    CONTROL_T   = 0x14
    CONTROL_U   = 0x15
    CONTROL_V   = 0x16
    CONTROL_W   = 0x17
    CONTROL_X   = 0x18
    CONTROL_Y   = 0x19
    CONTROL_Z   = 0x1A

    # Pseudo codes for multi-bytes CSI sequence keys.
    UP          = 0x0101
    DOWN        = 0x0102
    RIGHT       = 0x0103
    LEFT        = 0x0104
    HOME        = 0x0105
    END         = 0x0106
    INSERT      = 0x0107
    DELETE      = 0x0108
    PAGEUP      = 0x0109
    PAGEDOWN    = 0x010A
    F1          = 0x010B
    F2          = 0x010C
    F3          = 0x010D
    F4          = 0x010E
    F5          = 0x010F
    F6          = 0x0110
    F7          = 0x0111
    F8          = 0x0112
    F9          = 0x0113
    F10         = 0x0114
    F11         = 0x0115
    F12         = 0x0116
    F13         = 0x0117
    F14         = 0x0118
    F15         = 0x0119
    F16         = 0x011A
    F17         = 0x011B
    F18         = 0x011C
    F19         = 0x011D
    F20         = 0x011E
    F0          = 0x011F

    # Pseudo codes for function key modifiers.
    SHIFT       = 0x1000
    ALT         = 0x2000
    CONTROL     = 0x4000
    META        = 0x8000
    OPTION      = 0x8000
    MODIFIERS   = 0xf000  # mask

    # Indicator code of mouse events.
    MOUSE_EVENT = 0x0008_0000


_csi_sequences = {
    # XTerm sequences
    'A' : Key.UP,
    'B' : Key.DOWN,
    'C' : Key.RIGHT,
    'D' : Key.LEFT,
    'F' : Key.END,
    'H' : Key.HOME,
    'P' : Key.F1,
    'Q' : Key.F2,
    'R' : Key.F3,
    'S' : Key.F4,
    '1P' : Key.F1,
    '1Q' : Key.F2,
    '1R' : Key.F3,
    '1S' : Key.F4,

    # VT sequences
    '1~' : Key.HOME,
    '2~' : Key.INSERT,
    '3~' : Key.DELETE,
    '4~' : Key.END,
    '5~' : Key.PAGEUP,
    '6~' : Key.PAGEDOWN,
    '7~' : Key.HOME,
    '8~' : Key.END,
    '10~' : Key.F0,
    '11~' : Key.F1,
    '12~' : Key.F2,
    '13~' : Key.F3,
    '14~' : Key.F4,
    '15~' : Key.F5,
    '17~' : Key.F6,
    '18~' : Key.F7,
    '19~' : Key.F8,
    '20~' : Key.F9,
    '21~' : Key.F10,
    '23~' : Key.F11,
    '24~' : Key.F12,
    '25~' : Key.F13,
    '26~' : Key.F14,
    '28~' : Key.F15,
    '29~' : Key.F16,
    '31~' : Key.F17,
    '32~' : Key.F18,
    '33~' : Key.F19,
    '34~' : Key.F20,
}


# The XTerm encodes function key modifiers as parameters appended before the
# final character of the control sequence, and the modifiers are encoded in
# range of 2-16.
# The tuple '_modifiers' recorded those modifiers, and made their indices in
# the tuple equal to their codes.
# See also: http://www.leonerd.org.uk/hacks/fixterms/
_modifiers = ( 0, 0,
    Key.SHIFT,
    Key.ALT,
    Key.SHIFT + Key.ALT,
    Key.CONTROL,
    Key.SHIFT + Key.CONTROL,
    Key.ALT + Key.CONTROL,
    Key.SHIFT + Key.ALT + Key.CONTROL,
    Key.META,
    Key.META + Key.SHIFT,
    Key.META + Key.ALT,
    Key.META + Key.ALT + Key.SHIFT,
    Key.META + Key.CONTROL,
    Key.META + Key.CONTROL + Key.SHIFT,
    Key.META + Key.CONTROL + Key.ALT,
    Key.META + Key.CONTROL + Key.ALT + Key.SHIFT
)


def _match_csi_sequence(seq):
    if seq in _csi_sequences:
        return _csi_sequences[seq]
    csi = re.match(r'(.+);(1[0-6]|[1-9])([@-~])$', seq)
    if csi is not None:
        reduct = csi.group(1) + csi.group(3)  # Omits argument of modifier.
        if reduct in _csi_sequences:
            return _modifiers[int(csi.group(2))] + _csi_sequences[reduct]
        # Omits all arguments and try again for convention reason.
        if csi.group(1) == '1' and csi.group(3) in _csi_sequences:
            return _modifiers[int(csi.group(2))] + _csi_sequences[csi.group(3)]
    return Key.NONE


# pylint: disable=invalid-name
_mouse_handler = None

def mouse_handler(func):
    r"""Sets a function to handle mouse report.

    The handle function prototype:
        func(event: int, col: int, row: int) -> int
    """
    # pylint: disable=global-statement
    global _mouse_handler
    _mouse_handler = func


def _get_mouse_event():
    # XTerm sends { CSI M Cb Cx Cy } for mouse event report, and encodes
    # numeric parameters in a single character as (value + 32).
    seq = getch(0)  # Cb
    seq += getch(0)  # Cx
    seq += getch(0)  # Cy
    if not _mouse_handler or len(seq) < 3:
        return Key.NONE
    return _mouse_handler(*map(lambda ch: (ord(ch) - 32), seq))


def getkey(timeout: int = BLOCKING_, raw: bool = False) -> Key | int:
    r"""Gets key(s) from getch() and tranforms it(them) from string to code.

    Function keys in form of CSI sequences will be tranformed to pseudo
    key codes that defined in class Key when 'raw' = False. All other
    unrecognized ESC sequence keys be treated as an ESC and leftover
    individual keys.
    The getkey() also returns mouse event codes after mouse tracking mode
    be turned on. The event codes always larger than Key.MOUSE_EVENT while
    normal key codes smaller than it.

    Args:
        timeout: An argument passed to getch().
        raw: If True, getkey() will not try to tranform CSI sequence in
            keycode, but just return their code of ord() byte by byte.
            This is usually used for key or mouse testing purpose.

    Returns:
        Character's keycode from ord(), or function keycode that defined
        in class Key, or mouse event code that larger than Key.MOUSE_EVENT,
        all these codes may combines with modifier key codes.
        Returns Key.NONE if timeout or failure.
    """
    key_ch = getch(timeout)
    if not key_ch:
        return Key.NONE
    key_code = ord(key_ch)
    if key_code == Key.ESC and not raw:
        seq = getch(0)
        if seq in '[O':
            # In CSI sequence for leading by '\033[' or '\033O'.
            key_ch = getch(0)
            if key_ch == 'M':  # mouse event report
                return _get_mouse_event()
            while key_ch:
                seq += key_ch
                if 0x40 <= ord(key_ch) <= 0x7E:
                    # CSI terminal character are in range of 0x40-0x7E.
                    fkey_code = _match_csi_sequence(seq[1:])
                    if fkey_code:
                        return fkey_code
                    break
                key_ch = getch(0)
        # Due to unknown sequence, puts left characters back to buffer.
        _ch_buffer.extend(seq)
    return key_code


def _test_termkey():
    # Continuously reads input and prints codes for testing purpose.
    #
    raw = (len(sys.argv) > 1 and sys.argv[1] == '-r')
    print('Press any key to get code, CONTROL-X to exit.')
    setparams(echo=False, intr=False)
    keycode = getkey(raw=raw)
    while keycode != Key.CONTROL_X:
        try:
            print(f'code: {keycode:04x} - {Key(keycode).name}')
        except ValueError:
            print(f'code: {keycode:04x} - char: {chr(keycode)!r}')
        keycode = getkey(raw=raw)
    setparams()


if __name__ == '__main__':
    _test_termkey()

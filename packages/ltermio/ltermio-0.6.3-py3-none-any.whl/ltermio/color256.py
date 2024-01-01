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

r"""Sets 256-color display attributes of character terminal.

There are three pairs of functions to set or restore colors according
to their literal name, and another pair to set text display attributes:

    set_fcolor(color: int)
    reset_fcolor()
    set_bcolor(color: int)
    reset_bcolor()
    set_color(fcolor: int, bcolor: int)
    reset_color()
    set_textattr(attr: TextAttr | int)
    reset_textattr(attr: TextAttr | int)

All color functions use indexed color as parameters, function rgb() can
make indexed color number from given RGB parameters. Enum class Color
defined constants of some common-used indexed colors and grayscales.

Enum class TextAttr defined constants of text attributes, like BOLD, ITALIC
and UNDERLINED, etc.

Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
"""

import enum

_CSI_LEAD = '\033['

def rgb(red: int, green: int, blue: int) -> int:
    r"""Returns an indexed 256-color according to the given RGB parameters.

    Args:
        All parameters' valid values must be in range of 0~5.

    Raises:
        ValueError: Argument value out of range.
    """
    if not (0 <= red <= 5 and 0 <= green <= 5 and 0 <= blue <= 5):
        raise ValueError('Argument value out of range.')
    return 16 + red * 36 + green * 6 + blue


class Color(enum.IntEnum):
    r"""Enumerates some common-used constants of colors.
    """
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    BRIGHT_BLACK = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN = 14
    BRIGHT_WHITE = 15

    GRAYSCALE_DARKEST = 232
    GRAYSCALE_DARK = 238
    GRAYSCALE_MIDDLE = 243
    GRAYSCALE_LIGHT = 249
    GRAYSCALE_LIGHTEST = 255
    GRAY = rgb(3, 3, 3)
    SILVER = rgb(4, 4, 4)

    TAN = rgb(5, 4, 3)
    BRONZE = rgb(4, 3, 1)
    COPPER = BRONZE
    COFFEE = rgb(2, 1, 0)
    CHOCOLATE = rgb(4, 2, 1)
    BROWN = rgb(3, 1, 1)

    PINK = rgb(5, 3, 3)
    HOT_PINK = rgb(5, 2, 4)
    DEEP_PINK = rgb(5, 0, 3)
    TOMATO = rgb(5, 2, 2)
    INDIAN_RED = TOMATO
    MAROON = RED
    CRIMSON = rgb(5, 0, 1)
    SCARLET = CRIMSON

    VIOLET = rgb(3, 0, 5)
    BRIGHT_VIOLET = rgb(5, 3, 5)
    ORCHID = rgb(3, 1, 5)
    BRIGHT_ORCHID = rgb(4, 2, 4)
    PLUM = rgb(5, 4, 5)
    LAVENDER = rgb(4, 4, 5)
    MEDIUM_PURPLE = rgb(3, 2, 5)
    PURPLE = rgb(3, 0, 3)

    INDIGO = rgb(1, 0, 4)
    NAVY = rgb(0, 0, 3)
    ROYAL_BLUE = rgb(2, 3, 5)
    SKY_BLUE = rgb(3, 5, 5)
    DEEP_SKY_BLUE = rgb(0, 4, 5)
    AZURE = rgb(4, 5, 5)

    TURQUOISE = rgb(2, 5, 4)
    SPRING_GREEN = rgb(2, 4, 3)
    SEA_GREEN = rgb(1, 4, 4)
    DEEP_SEA_GREEN = rgb(1, 3, 2)
    OLIVE = rgb(3, 3, 0)

    BEIGE = rgb(5, 5, 4)
    IVORY = BEIGE
    KHAKI = rgb(5, 5, 3)
    DEEP_KHAKI = rgb(4, 4, 2)
    GOLD = rgb(5, 4, 0)
    ORANGE = rgb(5, 3, 0)
    DEEP_ORANGE = rgb(5, 2, 0)


def set_fcolor(color: int):
    r"""Sets foreground color.
    """
    print(f'{_CSI_LEAD}38;5;{color}m', end='')


def reset_fcolor():
    r"""Restores the foreground color to the default value.
    """
    print(f'{_CSI_LEAD}39m', end='')


def set_bcolor(color: int):
    r"""Sets background color.
    """
    print(f'{_CSI_LEAD}48;5;{color}m', end='')


def reset_bcolor():
    r"""Restores the background color to the default value.
    """
    print(f'{_CSI_LEAD}49m', end='')


def set_color(fcolor: int, bcolor: int):
    r"""Sets foreground to 'fcolor' and background to 'bcolor'.
    """
    print(f'{_CSI_LEAD}38;5;{fcolor}m{_CSI_LEAD}48;5;{bcolor}m',
          end='')


def reset_color():
    r"""Restores foreground and background color to the default value.
    """
    print(f'{_CSI_LEAD}39;49m', end='')


class TextAttr(enum.IntEnum):
    """Enumerates attributes that can be set to text.
    """
    DEFAULT = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    INVERT = 7
    HIDE = 8
    CROSSED_OUT = 9

    NORMAL = 22
    NOT_ITALIC = 23
    NOT_UNDERLINE = 24
    NOT_BLINK = 25
    NOT_INVERT = 27
    NOT_HIDE = 28
    NOT_CROSSED_OUT = 9


def textattr_seq(attr: TextAttr | int):
    """Returns a sequence string that can set attribute of text.
    """
    return f'{_CSI_LEAD}{attr}m'


def set_textattr(attr: TextAttr | int):
    """Sets text attribute to 'attr' that affects the subsequent output.
    """
    print(textattr_seq(attr), end='', flush=True)


def reset_textattr(attr: TextAttr | int):
    """Restores text attribute from set 'attr'.
    """
    if not 0 < attr < 10:
        raise ValueError('Invalid attribute')
    set_textattr(22 if attr <= 2 else attr + 20)


def _test_color256():
    def color_greetings():
        for i in range(6):
            set_textattr(i + 1)
            for char in 'Hello, color256!':
                set_fcolor(ord(char) % 32 + 20 + i * 36)
                print(char, end='')
            reset_textattr(i + 1)
            print()
        reset_fcolor()

    def grayscales():
        for color in range(Color.GRAYSCALE_DARKEST,
                           Color.GRAYSCALE_LIGHTEST + 1):
            set_bcolor(color)
            print('   ', end='')
        reset_bcolor()
        print()

    def all_rgbs():
        for red in range(6):
            for green in range(6):
                for blue in range(6):
                    set_bcolor(rgb(red, green, blue))
                    print('  ', end='')
            reset_bcolor()
            print()

    def enum_colors():
        for color in sorted(Color):
            print(f'{color.name:18s}: {color.value:3d} ', end='')
            set_bcolor(color)
            print(' ' * 12, end='')
            reset_bcolor()
            print()

    color_greetings()
    grayscales()
    all_rgbs()
    enum_colors()


if __name__ == '__main__':
    _test_color256()

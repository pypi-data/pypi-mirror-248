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

"""A lightweight POSIX character terminal I/O library.

Repo - https://github.com/brookssu/ltermio.git
"""

import functools

from .color256 import *
from .cursor import *
from .termkey import *
from .unicon import UnicodeIcon as UIcon


__version__ = '0.4.0'
__all__ = ['cursor', 'termkey', 'color256', 'unicon', 'termouse']


def appentry(func, echo=False, intr=False, cursor=False):
    """A decorator of the ltermio application entry.

    Before enters entry function, the decorator switchs and clears screen,
    sets cursor and other input attributes according to the parameters.
    And while the entry function returns, the decorator restores screen,
    cursor, color and other set attributes.

    Args:
        echo: Echoes input characters if True, False to disable.
        intr: False to disable keyboard interrupt signals.
        cursor: False to hide cursor while True to show.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        switch_screen()
        clear_screen()
        if not cursor:
            hide_cursor()
        setparams(echo=echo, intr=intr)
        try:
            return func(*args, **kwargs)
        finally:
            setparams()
            reset_color()
            show_cursor()
            restore_screen()
    return wrapper

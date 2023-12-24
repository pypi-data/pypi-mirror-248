# ltermio - A Lightweight POSIX terminal I/O library

The package contains four modules: **cursor**, **termkey**, **color256** and **unicon**. Tested only on **MacOS terminal** and **iTerm2**, so the platform compatibility has not been well verfied yet.
All functions are based on **CSI** sequences or **termios**, no additional requirements other than the standard library.

## Installation
Uses pip to install the package:

`pip3 install ltermio`

## cursor
Wrapper functions of **CSI(Control Sequence Introducer)** sequences about cursor and screen. And additionally provides a several of functions for text composing.

## termkey
There are only three functions: **getch()** and **getkey()** reads keyboard in non-canonical mode, **setparams()** sets frequently-used input attributes.  **getch()** reads raw key characters byte by byte, **getkey()** calls getch() and transforms the CSI sequences of function keys into key codes that defined in an enumerate class Key.

## color256
Sets 256-color display attributes of the character terminal.

## unicon
Collection of some common icons in unicode character set.

## History & Why
When I was learning Python a few months ago, I decided to write a terminal Tetris game as a practice of the language learning. Due to the learning reason, I did not want to use any third-party packages. So when I finally finished the game, there naturally formed this by-product, I named it ltermio.


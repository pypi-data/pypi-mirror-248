# ltermio - A Lightweight POSIX terminal I/O library

The package contains four modules: **cursor**, **termkey**, **color256** and **unicon**. Tested only on **MacOS terminal** and **iTerm2**, so the platform compatibility has not been well verfied yet.
All functions are based on **CSI** sequences or **termios**, no additional requirements other than the standard library.

## Installation
Uses pip to install the package:

`pip3 install ltermio`

## cursor
A series of functions about screen and cursor operations. And additionally provides 4 interesting functions for text composing, where **v_composing()** supports using VI like cursor commands to layout text display.

## termkey
There are 5 curses like functions: **getch()**, **getkey()**, **ungetch()**, **ungetkey()**, **setparams()**.

getch() and getkey() read keyboard in non-canonical mode, ungetch() and ungetkey() put keys back to the key buffer for next reading, setparams() sets frequently-used input attributes.

## color256
Sets 256-color display attributes of the character terminal.

## unicon
Collection of some common icons in unicode character set.

## History & Why
When I was learning Python a few months ago, I decided to write a terminal Tetris game as a practice of the language learning. Due to the learning reason, I did not want to use any third-party packages. So when I finally finished the game, there naturally formed this by-product, I named it ltermio.

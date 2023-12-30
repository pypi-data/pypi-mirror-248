# ltermio - A Lightweight POSIX terminal I/O library

The package contains 5 modules: ***cursor***, ***termkey***, ***termouse***, ***color256*** and ***unicon***. Tested only on **MacOS terminal** and **iTerm2**, so the platform compatibility has not been well verfied yet.  
All functions are based on **XTerm** specification, **CSI** sequences and **termios**, no additional requirements other than the standard library.

**Applicability**: They are only for **POSIX** terminal applications.

References:  
<https://en.wikipedia.org/wiki/ANSI_escape_code>  
<https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>  
<https://www.xfree86.org/current/ctlseqs.html>

## Installation & Usage
Uses pip to install the package:

`pip3 install ltermio`

More details on module usage:

`pydoc ltermio.module-name`

## History & Why
As we all know, character terminal are outdated facilities, why did I still write such a package?

When I was learning **Python** a few months ago, I decided to write a terminal **Tetris** game as a practice of the language learning. Due to the learning reason, I did not want to use any third-party packages. So when I finally finished the game, there naturally formed this by-product.

## color256 module
Sets 256-color display attributes of character terminal.

There are three pairs of functions to set or restore colors according to their literal name, and another pair to set text display attributes:

```python
    set_fcolor(color: int)
    reset_fcolor()
    set_bcolor(color: int)
    reset_bcolor()
    set_color(fcolor: int, bcolor: int)
    reset_color()
    set_textattr(attr: TextAttr | int)
    reset_textattr(attr: TextAttr | int)
```

All color functions use indexed color as parameter, function *rgb()* can make indexed color number from given RGB parameters. Enum class *Color* defined constants of some common-used indexed colors and grayscales.

Enum class *TextAttr* defined constants of text display attributes, like *BOLD*, *ITALIC* and *UNERLINED*, etc.

Following sample code prints gradually bright colorful greetings:

```python
    from ltermio import set_fcolor, reset_fcolor

    for i in range(6):
        for char in 'Hello, color256!':
            set_fcolor(ord(char) % 32 + 20 + i * 36)
            print(char, end='')
        print()
    reset_fcolor()
```

Another sample to output all colors:

```python
    from ltermio import rgb, set_bcolor, reset_bcolor

    for red in range(6):
        for green in range(6):
            for blue in range(6):
                set_bcolor(rgb(red, green, blue))
                print('  ', end='')
        print()
    reset_bcolor()
```

## cursor module
Wrapper functions of the **CSI(Control Sequence Introducer)** sequences about cursor and screen.

A several of additional functions are provided for text composing:

```python
    v_composing(seq: str) -> str
    downward_seq(text: str, cols: int) -> str
    vert_seq(text: str) -> str
    rect_border_seq(width: int, height: int, sym: str) -> str
```

Following sample code of *v_composing()* displays three big colorful greetings:

```python
    from ltermio import putmsg, v_composing

    _P1 = ':{0}\x1b3hj'
    _P15 = ':{0}\x1b6l:{0}\x1b11hj'
    _DASH = '5:{0}\x1b11hj'
    _NEXT_POS = '5k17l'

    LETTERS = {
        'E': v_composing(f'{(_DASH + _P1) * 2}{_DASH}{_NEXT_POS}'),
        'H': v_composing(f'{_P15 * 2}{_DASH}{_P15 * 2}{_NEXT_POS}'),
        'L': v_composing(f'{_P1 * 4}{_DASH}{_NEXT_POS}'),
        'O': v_composing(f'{_DASH}{_P15 * 3}{_DASH}'),
    }

    greeting = ''.join(map(LETTERS.get, 'HELLO'))
    putmsg(3, 20, greeting.format('\u2b50'))
    putmsg(9, 14, greeting.format('\u2b55'))
    putmsg(15, 8, greeting.format('\U0001f7e2'))
    print('\n')
```

## termkey module
Functions to read input in non-canonical mode.

There are 5 ***curses*** like functions:

+ *getch()*: Gets a character from stdin.
+ *ungetch()*: Puts one or more characters into the key buffer.
+ *getkey()*: Calls getch() and transforms character to keycode.
+ *ungetkey()*: Puts a keycode into the key buffer.
+ *setparams()*: Sets frenquently-used attributes of the input.

And a function to support mouse tracking.

+ *mouse_handler()*: Sets a function to handle mouse report.

Function keycodes in common using are defined in enum class *Key*.

A typical usage example as following:

```python
    import ltermio
    from ltermio import Key

    ltermio.setparams(echo=False)
    key = ltermio.getkey()
    while key != Key.ESC:
        ...
        key = ltermio.getkey()
    ltermio.setparams()
```

## termouse module
Detects and reports mouse events.

The implementation of the module follows the **XTerm** specification of the mouse tracking and uses normal tracking mode, see also:

<https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Mouse-Tracking>  
<https://www.xfree86.org/current/ctlseqs.html#Mouse%20Tracking>
    
Calls *ltermio.mouse_tracking_on()* to turn on the mouse tracking, or sets the parameter `mouse=True` on the decorator *ltermio.appentry_args()*.

The mouse events are reported by *ltermio.getkey()*, with value encoded in a 32-bits integer and larger than *Key.MOUSE_EVENT*. It is simple to make difference from normal key codes by `code > Key.MOUSE_EVENT`.  
Decodes the event codes by calling *ltermio.decode_mouse_event()* which returns a tuple with explicit items.
        
An example to get key and mouse inputs as following:

```python
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
```

## unicon module
Collection of some common icons in unicode character set.

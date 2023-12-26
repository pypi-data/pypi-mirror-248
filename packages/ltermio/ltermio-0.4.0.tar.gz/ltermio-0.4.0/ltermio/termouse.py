#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ltermio.termkey import getkey, setparams, mouse_handler, Key

def decset(mode: int):
    print(f'\033[?{mode}h', end='', flush=True)


def decrst(mode: int):
    print(f'\033[?{mode}l', end='', flush=True)


def _test_termouse():
    def on_mouse_report(report: str):
        for ch in report:
            print(f'{ord(ch):02x} ', end='')
        print('')

    mouse_handler(on_mouse_report)

    decset(1000)
    setparams(echo=False, intr=False)
    key = getkey()
    while key != Key.CONTROL_X:
        key = getkey()
    setparams()
    decrst(1000)

if __name__ == '__main__':
    _test_termouse()

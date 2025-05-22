# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
class_print.py

Screen output with color
Output sent to stdout
Colors are turned off if non-tty
"""
# pylint: disable=too-few-public-methods
from typing import (TextIO)
from collections.abc import (Callable)
import sys
from .color_pick import color_pick

type PrntMsg = Callable[[str | list[str],
                        str | None, str | None, bool | None],
                        None]


def rpt_colors(theme: str):
    """
    Colors used for report
    """
    light = ''
    if theme and theme.lower().startswith('l'):
        light = 'l'

    rpt_map = {
            'high': 'tan' + light,
            'norm': 'cyan' + light,
            'good': 'green' + light,
            'warn': 'warn' + light,
            'error': 'error' + light,
            }
    return rpt_map


class AscCol:
    """
    Simple Ascii Color Map
    """
    # pylint: disable=
    def __init__(self, theme):
        self.theme = theme
        self.color_map = {
                'blue': '27',
                'cyan': '51',
                'cyanl': '39',
                'green': '10',
                'greenl': '2',
                'orange': '9',
                'pink': '13',
                'redl': '196',
                'red': '196',
                'tan': '208',
                'tanl': '131',
                'yellow': '11',
                'yellowl': '13',
                'white': '254',
                'warn': '11',
                'warnl': '13',
                'fail': '160',
                'error': '196',
                'errorl': '196',
                'info': '208',
                'hdr': '227',
                }

        # List of known colors
        self.col_list = list(self.color_map.keys())
        self.rpt_color_map = rpt_colors(theme)
        self.rpt_col_list = list(self.rpt_color_map.keys())

    def _lookup_color_number(self, color: str) -> str:
        """
        Maps color name to ascii color number (256 color)

        - number -
        - report keys
        - any known color
        - default fg for theme

        color can be abbreviated so we expand it to find
        match using color_pick()

        e.g.
        if color == 'blu' then blue is actual color

        """
        #
        # check / expand if report color name
        #
        color_rpt = color_pick(color, self.rpt_col_list)
        if color_rpt:
            color = self.rpt_color_map[color_rpt]

        #
        # known color
        #
        color_matched = color_pick(color, self.col_list)
        if color_matched:
            color_num = self.color_map[color_matched]
            return color_num

        if color.isdigit():
            return color

        #
        # unknown -> default for theme
        #
        color_num = '254'
        if self.theme and self.theme.lower().startswith('l'):
            color_num = '0'   # black
        return color_num

    def colorize(self,
                 txt: str,
                 fg: str = '',
                 bg: str = '',
                 bold: bool = False) -> tuple[str, int]:
        """
        Colorize a string using 256 color ascii escapes
        Colors are a few names or digit from 0-255
        return colorized text and number of additional chars used to color
         - needed to keep format widths correct
        """
        esc = '\033['
        set_fg = '38;5;'
        set_bg = '48;5;'
        set_off = '0'
        # under = '\033[4m'

        cdel = 0

        set_bold = ''
        color_fg = ''
        color_bg = ''
        if bold:
            set_bold = ';1'

        if fg:
            color_fg = self._lookup_color_number(fg)
            color_fg = f'{set_fg}{color_fg}'

        if bg:
            color_bg = self._lookup_color_number(bg)
            color_bg = f'{set_bg}{color_bg}'

        if fg or bg or bold:
            lbefore = len(txt)
            txt = f'{esc}{color_fg}{color_bg}{set_bold}m{txt}{esc}{set_off}m'
            lafter = len(txt)
            cdel = lafter - lbefore

        return (txt, cdel)


class Prnt:
    """
    Prnt class - handles screen writes
    see prnt() and companion methods
    """
    # pylint: disable=
    def __init__(self, theme: str):
        self.color: AscCol = AscCol(theme)
        self.fpo: TextIO = sys.stdout
        self.tty: bool = False
        self.theme: str = theme

        if self.fpo.isatty():
            self.tty = True

    def msg(self,
            txt: str | list[str],
            fg: str = '',
            bg: str = '',
            bold: bool = False):
        """
        Handles the work for messages with header or footer (dashes)

        txt can be string or list of strings
        Single string can contain newlines.
        fg: ascii color uses first letter or use number 0-254 (Default 'w')
            blue Bold cyan fail red green head under warn
        """
        # pylint: disable=R0913
        if not txt:
            return

        if isinstance(txt, list):
            text = ''.join(txt)
        else:
            text = txt
        (text, _cdel) = self.colorize(text, fg=fg, bg=bg, bold=bold)
        self.fpo.write(text)
        self.fpo.flush()

    def colorize(self, txt, fg=None, bg=None, bold=False) -> tuple[str, int]:
        """
        colorize text without printing
          - also returns how many chars the color esacapes occupy in string
            useful when formatiing specific widths since color
            escapes take space in string but not on screen
        """
        cdel = 0
        if self.tty and self.theme:
            (txt, cdel) = self.color.colorize(txt, fg=fg, bg=bg, bold=bold)
        return (txt, cdel)

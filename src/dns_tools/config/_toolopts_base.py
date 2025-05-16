# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-tool
 All controls are command line arguments.
"""
# pylint: disable=too-few-public-methods

from utils import Prnt

from ._config import Config
from ._parse_args import parse_args
from ._toolopts_avail import available_tool_options


class ToolOptsBase(Config):
    """
    holds config settings are command line options
     - after getting raw options, map to more convenient form
       e.g. group ksk items together and zsk items together.
    """
    def __init__(self):
        super().__init__()
        self.do_keys = False

        #
        # signing options
        #
        self.sign: bool = False
        self.serial_bump: bool = False
        self.keep_include: bool = False

        self.print_keys = False

        #
        # Command line options override config
        #
        _command_line_options(self)

        # now theme is set, initialize print
        self.prnt = Prnt(self.theme)

        #
        # Implied Key related options
        # e.g. moving next keys to curr is part of doing a roll
        #
        self.key_opts.implied_options()

        # self.do_keys = self.key_opts.do_keys
        # self.serial_bump = self.key_opts.serial_bump


def _command_line_options(opts: ToolOptsBase):
    """
    Parse command line options for dns tool.
    """
    me = 'dns_tools: key (ksk and zsk) generation\n'
    me += 'zone files sign, key rolls, serial bumps'

    avail_options = available_tool_options()
    parsed_options = parse_args(me, avail_options)

    #
    # save if found any options
    #
    if not parsed_options:
        return

    #
    # map options to attributes
    # Key options mapped:
    #
    #  - ksk_xxx, gen_ksk_yyy => ksk_opts(xxx, gen_yyy)
    #  - zsk_xxx, gen_zsk_yyy => zsk_opts(xxx, gen_yyy)
    #
    for (opt, val) in parsed_options.items():
        if val in (None, []):
            continue

        if opt == 'zones' and val:
            opts.domains = val

        elif 'ksk_' in opt:
            opts.key_opts.ksk.set_opt(opt, val)

        elif 'zsk_' in opt:
            opts.key_opts.zsk.set_opt(opt, val)

        elif opt == 'sign':
            opts.key_opts.sign = val

        else:
            setattr(opts, opt, val)

    #
    # color turned off when theme is "none"
    #
    if opts.theme and opts.theme.lower() == 'none':
        opts.theme = ''

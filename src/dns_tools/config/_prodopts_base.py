# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
 Initialize for dns-prod
"""
# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-code

from dns_tools.utils import Prnt

from ._config import Config
from ._parse_args import parse_args
from ._prodopts_avail import available_prod_options


class ProdOptsBase(Config):
    """ Manage pushing to production """
    def __init__(self):
        #
        # Prod specific options not part of shared config
        #
        super().__init__()

        self.dns_restart: bool = False
        self.to_production: bool = False
        self.int_zones: bool = True
        self.ext_zones: bool = True

        #
        # command line options override config
        #
        _command_line_options(self)

        # now theme is set, initialize print
        self.prnt = Prnt(self.theme)


def _command_line_options(opts: ProdOptsBase):
    """
    Parse command line options for dns prod
    """
    me = 'dns_tools: key (ksk and zsk) generation\n'
    me += 'zone files sign, key rolls, serial bumps'

    avail_options = available_prod_options()
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

        # if opt == 'zones' and val:
        #     opts.domains = val

        # elif 'ksk_' in opt:
        #     opts.ksk_opts.set_opt(opt, val)

        # elif 'zsk_' in opt:
        #     opts.zsk_opts.set_opt(opt, val)
        if opt == 'int_ext':
            if val.lower().startswith('int'):
                opts.int_zones = True
                opts.ext_zones = False

            elif val.lower().startswith('ext'):
                opts.int_zones = False
                opts.ext_zones = True

            else:
                opts.int_zones = True
                opts.ext_zones = True
        else:
            setattr(opts, opt, val)

    #
    # color turned off when theme is "none"
    #
    if opts.theme and opts.theme.lower() == 'none':
        opts.theme = ''

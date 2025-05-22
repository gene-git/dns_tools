# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Each operation has own command line arguments.

 Keep all options here so they are all in one place and
 makes it easier to avoid any conflicts.
"""
# pylint: disable=duplicate-code

from ._parse_args import Opt


def available_prod_options() -> list[Opt]:
    """
    options for pushing to production
      - work staging -> production staging ( to_staging )
      - production staging to live productions (to_live )
    """
    opt: Opt
    opts: list[Opt] = []

    opt = (('--theme'),
           {'help': 'Color theme: dark, light or none)'})
    opts.append(opt)

    opt = (('--int-ext', '--int_ext'),
           {'help': 'What to push: internal, external or both (both)',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--to-production', '--to_production'),
           {'help': 'Copy zone files from work staging to live production',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--dns-restart', '--dns_restart'),
           {'help': 'Restart the DNS server after zones updated',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('-t', '--test'),
           {'help': 'Test mode - print but dont do',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('-v', '--verb'),
           {'help': 'More verbosity',
            'action': 'store_true'})
    opts.append(opt)

    #
    # sort
    #
    opts.sort(key=lambda item: item[0][0])

    return opts

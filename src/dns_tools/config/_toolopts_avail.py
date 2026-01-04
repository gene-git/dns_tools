# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
 Each operation has own command line arguments.

 Keep all options here so they are all in one place and
 makes it easier to avoid any conflicts.
"""
# pylint: disable=duplicate-code

from ._parse_args import Opt


def opts_sign() -> list[Opt]:
    """
    Signing options.
    """
    opts: list[Opt] = []

    opts.append((('--serial-bump', '--serial_bump'),
                 {'help': 'Bump all serials',
                  'action': 'store_true'}
                 ))

    opts.append((('--keep-include', '--keep_include'),
                 {'help': 'Keep temp file $INCLUDE expanded',
                  'action': 'store_true'}
                 ))

    opts.append((('--sign'),
                 {'help': 'Sign with curr keys (ksk and zsk)',
                  'action': 'store_true'}
                 ))

    opts.append((('--sign-ksk-next', '--sign_ksk_next'),
                 {'help': 'Sign with both next and curr ksk',
                  'action': 'store_true'}
                 ))

    opts.append((('--sign-zsk-next', '--sign_zsk_next'),
                 {'help': 'Sign with both next and curr zsk',
                  'action': 'store_true'}
                 ))

    return opts


def opts_keys() -> list[Opt]:
    """
    Key options
    """
    opts: list[Opt] = []

    opts.append((('--gen-zsk-curr', '--gen_zsk_curr'),
                 {'help': 'Generate ZSK for curr',
                  'action': 'store_true'}
                 ))

    opts.append((('--gen-zsk-next', '--gen_zsk_next'),
                 {'help': 'Generate ZSK for next',
                  'action': 'store_true'}
                 ))

    opts.append((('--gen-ksk-curr', '--gen_ksk_curr'),
                 {'help': 'Generate KSK for curr',
                  'action': 'store_true'}
                 ))

    opts.append((('--gen-ksk-next', '--gen_ksk_next'),
                 {'help': 'Generate KSK for next',
                  'action': 'store_true'}
                 ))

    opts.append((('--zsk-roll-1', '--zsk_roll_1'),
                 {'help': 'ZSK Phase 1 roll - old and new',
                  'action': 'store_true'}
                 ))

    opts.append((('--zsk-roll-2', '--zsk_roll_2'),
                 {'help': 'ZSK Phase 2 roll - new only',
                  'action': 'store_true'}
                 ))

    note = '** Plesae Update registrar'
    opts.append((('--ksk-roll-1', '--ksk_roll_1'),
                 {'help': f'KSK Phase 1 roll: old & new. {note}',
                  'action': 'store_true'}
                 ))

    opts.append((('--ksk-roll-2', '--ksk_roll_2'),
                 {'help': 'KSK Phase 2 roll - new only',
                  'action': 'store_true'}
                 ))

    opts.append((('--print-keys', '--print_keys'),
                 {'help': 'Print keys (curr and next)',
                  'action': 'store_true'}
                 ))

    opts.append((('--ksk-algo', '--ksk_algo'),
                 {'help': 'Key algorithm for KSK)'}
                 ))

    opts.append((('--zsk-algo', '--zsk_algo'),
                 {'help': 'Key algorithm for ZSK)'}
                 ))
    return opts


def available_tool_options() -> list[Opt]:
    """
    Define the full set of options
    """
    opts: list[Opt] = []

    opts.append((('--theme'),
                 {'help': 'Color theme: dark, light or none)'}
                 ))

    opts.append((('-t', '--test'),
                 {'help': 'Test mode - print but dont do',
                  'action': 'store_true'}
                 ))

    opts.append((('-v', '--verb'),
                 {'help': 'More verbosity',
                  'action': 'store_true'}
                 ))

    opts.append((('zones'),
                 {'help': 'Zones/domains this action applies to',
                  'nargs': '*'}
                 ))

    opts += opts_sign()
    opts += opts_keys()

    #
    # sort
    #  may have short + long opts or jusr long opt
    #  sort by first option name element (may only be one)
    #
    opts.sort(key=lambda item: item[0][0])

    return opts

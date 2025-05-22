# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
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
    opt: Opt
    opts: list[Opt] = []

    opt = (('--serial-bump', '--serial_bump'),
           {'help': 'Bump all serials',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--keep-include', '--keep_include'),
           {'help': 'Keep temp file $INCLUDE expanded',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--sign'),
           {'help': 'Sign with curr keys (ksk and zsk)',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--sign-ksk-next', '--sign_ksk_next'),
           {'help': 'Sign with both next and curr ksk',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--sign-zsk-next', '--sign_zsk_next'),
           {'help': 'Sign with both next and curr zsk',
            'action': 'store_true'})
    opts.append(opt)

    return opts


def opts_keys() -> list[Opt]:
    """
    Key options
    """
    opt: Opt
    opts: list[Opt] = []

    opt = (('--gen-zsk-curr', '--gen_zsk_curr'),
           {'help': 'Generate ZSK for curr',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--gen-zsk-next', '--gen_zsk_next'),
           {'help': 'Generate ZSK for next',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--gen-ksk-curr', '--gen_ksk_curr'),
           {'help': 'Generate KSK for curr',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--gen-ksk-next', '--gen_ksk_next'),
           {'help': 'Generate KSK for next',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--zsk-roll-1', '--zsk_roll_1'),
           {'help': 'ZSK Phase 1 roll - old and new',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--zsk-roll-2', '--zsk_roll_2'),
           {'help': 'ZSK Phase 2 roll - new only',
            'action': 'store_true'})
    opts.append(opt)

    note = '** Plesae Update registrar'
    opt = (('--ksk-roll-1', '--ksk_roll_1'),
           {'help': f'KSK Phase 1 roll: old & new. {note},',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--ksk-roll-2', '--ksk_roll_2'),
           {'help': 'KSK Phase 2 roll - new only',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--print-keys', '--print_keys'),
           {'help': 'Print keys (curr and next)',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('--ksk-algo', '--ksk_algo'),
           {'help': 'Key algorithm for KSK)'})
    opts.append(opt)

    opt = (('--zsk-algo', '--zsk_algo'),
           {'help': 'Key algorithm for ZSK)'})
    opts.append(opt)

    return opts


def available_tool_options() -> list[Opt]:
    """
    Define the full set of options
    """
    opt: Opt
    opts: list[Opt] = []

    opt = (('--theme'),
           {'help': 'Color theme: dark, light or none)'})
    opts.append(opt)

    opt = (('-t', '--test'),
           {'help': 'Test mode - print but dont do',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('-v', '--verb'),
           {'help': 'More verbosity',
            'action': 'store_true'})
    opts.append(opt)

    opt = (('zones'),
           {'help': 'Zones/domains this action applies to',
            'nargs': '*'})

    opts += opts_sign()
    opts += opts_keys()

    #
    # sort
    #  may have short + long opts or jusr long opt
    #  sort by first option name element (may only be one)
    #
    opts.sort(key=lambda item: item[0][0])

    return opts

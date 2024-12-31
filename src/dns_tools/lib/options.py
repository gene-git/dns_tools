# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Each operation has own command line arguments.
"""

def opts_sign():
    """ signing options """

    opts = [
            [['--serial_bump'], {
             'action' : 'store_true',
             'help' : 'Bump all serials',
             }],
            [['--keep_include'], {
             'action' : 'store_true',
             'help' : 'Keep temp file $INCLUDE expanded',
             }],
            [['--sign'], {
             'action' : 'store_true',
             'help' : 'Sign with curr keys (ksk and zsk)',
             }],
            [['--sign_ksk_next'], {
             'action' : 'store_true',
             'help' : 'Sign with both next and curr ksk',
             }],
            [['--sign_zsk_next'], {
             'action' : 'store_true',
             'help' : 'Sign with both next and curr zsk',
            }],
            ]
    return opts

def opts_keys():
    """ signing options """

    opts = [
            [['--gen_zsk_curr'], {
             'action' : 'store_true',
             'help' : 'Generate ZSK for curr',
             }],
            [['--gen_zsk_next'], {
             'action' : 'store_true',
             'help' : 'Generate ZSK for next',
             }],
            [['--gen_ksk_curr'], {
             'action' : 'store_true',
             'help' : 'Generate KSK for curr',
             }],
            [['--gen_ksk_next'], {
             'action' : 'store_true',
             'help' : 'Generate KSK for next',
             }],
            [['--zsk_roll_1'], {
             'action' : 'store_true',
             'help' : 'ZSK Phase 1 roll - old and new',
             }],
            [['--zsk_roll_2'], {
             'action' : 'store_true',
             'help' : 'ZSK Phase 2 roll - new only',
             }],
            [['--ksk_roll_1'], {
             'action' : 'store_true',
             'help' : 'KSK Phase 1 roll - old and new - NB must add to degistrar',
             }],
            [['--ksk_roll_2'], {
             'action' : 'store_true',
             'help' : 'KSK Phase 2 roll - new only',
             }],
            [['--print_keys'], {
             'action' : 'store_true',
             'help' : 'Print keys (curr and next)',
             }],
           ]
    return opts

def get_option_list():
    """
    Define the full set of options
    """
    opts = [
            [['--theme'], {
             'help' : 'Color theme : dark, light or none',
             }],
            [['-t', '--test'], {
             'action' : 'store_true',
             'help' : 'Test mode - print but dont do',
             }],
            [['-v', '--verb'], {
             'action' : 'store_true',
             'help' : 'More verbosity',
             }],
             [['zones'],
              {'nargs' : '*',
               'help' : 'Zones/domains this action applies to',
             }]
            ]
    opts += opts_sign()
    opts += opts_keys()

    return opts

def get_prod_option_list():
    """
    options for pushing to production
      - work staging -> production staging ( to_staging )
      - production staging to live productions (to_live )
    """

    opts = [
            [['--theme'], {
             'help' : 'Color theme : dark, light or none',
             }],
            [['--int_ext'], {
             'default' : 'both',
             'help' : 'What to push: internal, external or both (both)',
             }],
            [['--to_production'], {
             'action' : 'store_true',
             'help' : 'Copy zone files from work staging to live production',
             }],
            [['--dns_restart'], {
             'action' : 'store_true',
             'help' : 'Restart the nsd server after zones updated',
             }],
            [['-t', '--test'], {
             'action' : 'store_true',
             'help' : 'Test mode - print but dont do',
             }],
            [['-v', '--verb'], {
             'action' : 'store_true',
             'help' : 'More verbosity',
             }],
            ]
    return opts

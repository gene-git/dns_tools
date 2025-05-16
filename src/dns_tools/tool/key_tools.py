# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Key Tools
   dns_print_all_keys()
   dnd_add_missing_signing_keys()
"""


def print_all_keys(tool):
    """
    Printd names of keys for all domains
    """
    msg = tool.opts.prnt.msg
    domains = tool.opts.domains

    msg('Key IDs :\n', fg='high')
    for dom in domains:
        msg(f'  {dom}\n', fg='norm')
        this_key = tool.keys[dom]

        curr_ksk_id = this_key.ksk.curr.key_id
        next_ksk_id = this_key.ksk.next.key_id

        curr_zsk_id = this_key.zsk.curr.key_id
        next_zsk_id = this_key.zsk.next.key_id

        msg(f'    curr ksk : {curr_ksk_id}\n')
        msg(f'         zsk : {curr_zsk_id}\n')

        msg(f'    next ksk : {next_ksk_id}\n')
        msg(f'         zsk : {next_zsk_id}\n')


def dns_add_missing_signing_keys(tool):
    """
    Get list of any missing signing keys
        - dont need this - simply generate if needed when go to sign
        - get key - no key - make new one
    """
    domains = tool.opts.domains

    ksk_keys = []
    zsk_keys = []

    for dom in domains:
        print(f'Keys for : {dom}')
        this_key = tool.keys[dom]

        # update key_ids
        this_key.key_id()
        curr_ksk_id = this_key.ksk.curr.key_id
        next_ksk_id = this_key.ksk.next.key_id

        curr_zsk_id = this_key.zsk.curr.key_id
        next_zsk_id = this_key.zsk.next.key_id

        if not curr_ksk_id:
            ksk_keys.append((dom, 'ksk', 'curr'))

        if not next_ksk_id:
            ksk_keys.append((dom, 'ksk', 'next'))

        if not curr_zsk_id:
            zsk_keys.append((dom, 'zsk', 'curr'))

        if not next_zsk_id:
            zsk_keys.append((dom, 'zsk', 'next'))

    return (ksk_keys, zsk_keys)

# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
Process requested key updates
"""
def process_key_updates(tool):
    """
    Update any keys if asked
    """
    domains = tool.opts.domains
    prnt = tool.prnt

    if not domains :
        return

    ksk_opts = tool.opts.ksk_opts
    zsk_opts = tool.opts.zsk_opts

    prnt.msg('\nKey updates\n', fg_col='high')
    for dom in domains:
        prnt.msg(f'  {dom}\n', fg_col='norm')
        dom_keys = tool.keys[dom]

        #
        # Ksk keys
        #
        if ksk_opts.gen_curr:
            print('    ksk curr:')
            dom_keys.ksk.make_new_curr_key()

        if ksk_opts.gen_next:
            print('    ksk next:')
            dom_keys.ksk.make_new_next_key()

        #
        # Zsk keys
        #
        if zsk_opts.gen_curr:
            print('    zsk curr:')
            dom_keys.zsk.make_new_curr_key()

        if zsk_opts.gen_next:
            print('    zsk next:')
            dom_keys.zsk.make_new_next_key()

# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Process requested key updates
"""
# pylint: disable=too-many-branches
from dns_tools.config import (KeyOpts, ToolOpts)
from dns_tools.keys import DnsKey

from .dnstool_base import DnsToolBase


def process_key_updates(tool: DnsToolBase):
    """
    Update any keys if asked
    """
    domains = tool.opts.domains
    msg = tool.opts.prnt.msg

    if not domains:
        return

    ksk_opts = tool.opts.key_opts.ksk
    zsk_opts = tool.opts.key_opts.zsk

    msg('\nKey updates\n', fg='high')
    for dom in domains:
        msg(f'  {dom}\n', fg='norm')
        dom_keys = tool.keys[dom]

        #
        # Ksk keys
        #
        if not _make_new_key(tool.opts, ksk_opts, dom_keys.ksk):
            tool.okay = False
        #
        # Zsk keys
        #
        if not _make_new_key(tool.opts, zsk_opts, dom_keys.zsk):
            tool.okay = False


def _make_new_key(opts: ToolOpts, key_opts: KeyOpts,
                  dns_key: DnsKey) -> bool:
    """
    Make a new key.

    Args:
        key_opts (KeyOpts):    options

        dns_key (DnsKey):   ksk or zsk key to work with.

    Returns:
        bool:
        True if all okay, otherwise False
    """
    okay = True
    msg = opts.prnt.msg

    if key_opts.gen_curr:
        msg(f'    {key_opts.ktype} curr:')
        if not dns_key.make_new_curr_key(opts):
            msg('Failed\n', fg='error')
            okay = False
        else:
            msg('')

    if key_opts.gen_next:
        msg(f'    {key_opts.ktype} next:')
        if not dns_key.make_new_next_key(opts):
            msg('Failed\n', fg='error')
            okay = False
        else:
            msg('')
    return okay

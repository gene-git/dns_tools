# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
DNS key class
"""
from dns_tools.config import ToolOpts

from ._key import DnsKey


class DnsKeys:
    """
    Manage a domain's keys for both ZSK and KSK.
    """
    # pylint: disable=
    def __init__(self, domain: str, key_dir: str):
        self.key_dir: str = key_dir
        self.domain: str = domain

        self.ksk = DnsKey(domain, 'ksk', key_dir)
        self.zsk = DnsKey(domain, 'zsk', key_dir)

    def roll_ksk_keys(self, opts: ToolOpts):
        """
        do any key rolls for this domain
         - rename the sym links next.xxx to curr.xxx
         - key.curr = key_next
         - key_next = None
        """
        self.ksk.roll_next_to_curr(opts)

    def roll_zsk_keys(self, opts: ToolOpts):
        """
        do any key rolls for this domain
         - rename the sym links next.xxx to curr.xxx
         - key.curr = key_next
         - key_next = None
        """
        self.zsk.roll_next_to_curr(opts)

# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
dnssec class
"""

from dns_tools.zone import set_zone_perms

from .dnstool_base import DnsToolBase
from .bump_serial_sign import dns_bump_serial_sign_zones
from .process_keys import process_key_updates
from .key_tools import print_all_keys


class DnsTool(DnsToolBase):
    """
    DNS Tool Class

    Actions/methods are here.
    Attributes in parent base class.
    """
    def do_key_updates(self):
        """
        do key updates
         - rollover phase 1 requires new 'next' key(s)
        """
        if not self.opts.key_opts.do_keys:
            return

        msg = self.opts.prnt.msg
        process_key_updates(self)
        if not self.okay:
            msg('Error: key update failed\n')

        if self.opts.print_keys:
            self.print_keys()

    def do_key_rollovers(self):
        """
        move next to current key
        """
        msg = self.opts.prnt.msg
        opts = self.opts

        if opts.key_opts.ksk.roll_2:
            msg('KSK Key roll - next to curr\n', fg='high')
            if opts.test:
                msg('  Skipped - Test mode\n')
            else:
                for dom in opts.domains:
                    self.keys[dom].roll_ksk_keys(opts)

        if opts.key_opts.zsk.roll_2:
            msg('ZSK Key roll - next to curr\n', fg='high')
            if opts.test:
                msg('  Skipped - Test mode\n')
            else:
                for dom in self.opts.domains:
                    self.keys[dom].roll_zsk_keys(opts)

    def do_serial_bump_sign_zones(self):
        """
        - bump serials (tool.opts.serial_bump)
        - sign zones   (opts.key_opts.sign)
        """
        if not (self.opts.key_opts.sign or self.opts.serial_bump):
            return

        msg = self.opts.prnt.msg
        if not dns_bump_serial_sign_zones(self):
            self.okay = False
            msg('Error: zone signing failed\n')

    def print_keys(self):
        """ print out all keys (none if not found) """
        print_all_keys(self)

    def create_missing_keys(self):
        """
        Check any needed keys are available
         - make new key if missing
        """
        msg = self.opts.prnt.msg
        opts = self.opts

        msg('\nChecking that required keys are available\n', fg='high')
        if opts.test and opts.key_opts.do_keys:
            msg('  Test mode - may have false positives\n')

        for dom in opts.domains:
            dom_key = self.keys[dom]
            if opts.key_opts.ksk.sign_curr:
                dom_key.ksk.make_missing_curr_key(opts)

            if opts.key_opts.ksk.sign_next:
                dom_key.ksk.make_missing_next_key(opts)

            if opts.key_opts.zsk.sign_curr:
                dom_key.zsk.make_missing_curr_key(opts)

            if opts.key_opts.zsk.sign_next:
                dom_key.zsk.make_missing_next_key(opts)

    def zone_perms(self):
        """ ensure correct owner and permissions """
        set_zone_perms(self.opts)

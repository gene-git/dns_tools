# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
dnssec class
"""
import os
from .class_opts import DnsOpts
from .class_key import DnsKeys
from .process_signing import dns_process_signing_zones
from .process_keys import process_key_updates
from .key_tools import print_all_keys
from .zone_perms import set_zone_perms
from .class_print import Prnt
from .config import config_check

class DnsTool:
    """ handles all dns sec operations """
    def __init__(self):
        self.opts = DnsOpts()
        self.okay = self.opts.okay
        self.cwd = os.getcwd()
        self.prnt = Prnt(self.opts.theme)

        # sanity check on inputs
        if not config_check(self.prnt, self.opts):
            self.okay = False

        # if sign - get keys per domain
        self.keys = {}
        if self.opts.domains:
            for dom in self.opts.domains:
                self.keys[dom] = DnsKeys(self, dom, self.opts.key_dir)

    def do_key_updates(self):
        """
        do key updates
         - rollover phase 1 requires new 'next' key(s)
        """
        if not self.opts.do_keys:
            return

        process_key_updates(self)
        if self.opts.print_keys:
            self.print_keys()

    def do_key_rollovers(self):
        """
        move next to current key
        """
        if self.opts.ksk_opts.roll_2 :
            self.prnt.msg('KSK Key roll - next to curr\n', fg_col='high')
            if self.opts.test:
                self.prnt.msg('  Skipped - Test mode\n')
            else:
                for dom in self.opts.domains:
                    self.keys[dom].roll_ksk_keys()

        if self.opts.zsk_opts.roll_2 :
            self.prnt.msg('ZSK Key roll - next to curr\n', fg_col='high')
            if self.opts.test:
                self.prnt.msg('  Skipped - Test mode\n')
            else:
                for dom in self.opts.domains:
                    self.keys[dom].roll_zsk_keys()

    def do_sign_zones(self):
        """ do signkey actions """
        if not self.opts.sign:
            return

        dns_process_signing_zones(self)

    def print_keys(self):
        """ print out all keys (none if not found) """
        print_all_keys(self)

    def create_missing_keys(self):
        """
        Check any needed keys are available
         - make new key if missing
        """
        self.prnt.msg('\nChecking that required keys are available\n', fg_col='high')
        if self.opts.test and self.opts.do_keys:
            self.prnt.msg('  Test mode - may have false positives\n')

        for dom in self.opts.domains:
            dom_key = self.keys[dom]
            if self.opts.ksk_opts.sign_curr:
                dom_key.ksk.make_missing_curr_key()

            if self.opts.ksk_opts.sign_next:
                dom_key.ksk.make_missing_next_key()

            if self.opts.zsk_opts.sign_curr:
                dom_key.zsk.make_missing_curr_key()

            if self.opts.zsk_opts.sign_next:
                dom_key.zsk.make_missing_next_key()

    def zone_perms(self):
        """ ensure correct owner and permissions """
        set_zone_perms(self)

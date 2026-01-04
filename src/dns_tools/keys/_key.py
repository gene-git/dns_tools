# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
DNS key class
"""
import os

from dns_tools.config import ToolOpts
from dns_tools.utils import rel_from_abs_path

from ._keyinfo import KeyInfo
from ._keyfile_extensions import keyfile_extensions


class DnsKey:
    """
    Key class for one key: one domain and one key type (ksk or zsk).

    Handles both "curr" and "next",

    key_dir is directory under which all keys live.
    i.e. for curr:
        this_key_dir = <key_dir>/domain/<key_type>
        keyfile link = <this_key_dir>/curr.<ext>  -> data/<xxx.ext>

        <xxx.ext> = K<domain>.<key-id>.<ext>

        key-id is of the form "+nnn+nnnnn"
        <ext> for ksk is 'key' or 'private'
        next is similar to curr. zsk has additional extensions for DS.

    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, domain: str, ktype: str, key_dir: str):

        self.domain: str = domain
        self.ktype: str = ktype                  # zsk or ksk
        self.key_dir: str = key_dir
        self.this_key_dir: str = os.path.join(key_dir, domain, ktype)

        self.curr = KeyInfo(domain, 'curr', ktype, self.this_key_dir)
        self.next = KeyInfo(domain, 'next', ktype, self.this_key_dir)

        self.key_id: str = ''
        self.key_base: str = ''
        self.key_link: str = ''

        #
        # keys in key_dir/<sdomain>/zsk,ksk
        #
        self.curr.get_key_base()
        self.curr.get_key_id()

        self.next.get_key_base()
        self.next.get_key_id()

    def get_key_id(self):
        """ construct key_id, key_base """
        self.curr.get_key_id()
        self.next.get_key_id()

    def make_new_curr_key(self, opts: ToolOpts) -> bool:
        """
        make one new key

        Returns:
            bool:
            True if okay else False
        """
        self.curr.make_new_key(opts)
        if self.curr.key_id:
            return True
        return False

    def make_new_next_key(self, opts: ToolOpts) -> bool:
        """ make one new key """
        self.next.make_new_key(opts)
        if self.next.key_id:
            return True
        return False

    def make_missing_curr_key(self, opts: ToolOpts):
        """ make one new key """
        self.curr.make_missing_key(opts)

    def make_missing_next_key(self, opts: ToolOpts):
        """ make one new key """
        self.next.make_missing_key(opts)
        if self.next.key_id:
            return True
        return False

    def roll_next_to_curr(self, opts: ToolOpts):
        """
        roll next key to be new curr key
        """
        _roll_next_to_curr_files(opts, self)
        self.curr = self.next

        # self.next = None
        self.next = KeyInfo(self.domain, 'next', self.ktype,
                            self.this_key_dir)


def _roll_next_to_curr_files(opts: ToolOpts, dns_key: DnsKey):
    """
    For one "key" instance i.e. for one domain
     make the next key the new curr key.
     next must exist - should we validate?
    """
    okay = True
    ktype = dns_key.ktype
    curr_key_base = dns_key.curr.key_base
    next_key_base = dns_key.next.key_base

    exts = keyfile_extensions(ktype)
    for ext in exts:
        fcur = curr_key_base + ext
        fnxt = next_key_base + ext

        fcur_rel = rel_from_abs_path(fcur, opts.work_dir)
        fnxt_rel = rel_from_abs_path(fnxt, opts.work_dir)

        if os.path.islink(fnxt):
            try:
                print(f'  Rolling {ktype} {fnxt_rel} to {fcur_rel}')
                if not opts.test:
                    os.rename(fnxt, fcur)
            except OSError as err:
                print(f'  ** Error Rolling {ktype} {fnxt} to {fcur} - {err}')
                okay = False
        else:
            print(f'  ** Error Rolling {ktype}: Missing link {fnxt}')
            okay = False
    return okay

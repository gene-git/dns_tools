# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
DNS key class
"""
import os

from dns_tools.config import ToolOpts

from ._keyinfo_base import KeyInfoBase
from ._keyid_from_filename import keyid_from_filename
from ._generate_key import generate_key


class KeyInfo(KeyInfoBase):
    """
    Key Class for one key - methods.

    Used for either 'curr' or 'next'
    """
    def get_key_base(self):
        """
        Basename of key files:
            key_base ~ key_dir/{curr,next}
            key_link ~ key_dir/{curr,next}.key
        """
        which = self.which
        self.key_base = os.path.join(self.this_key_dir, f'{which}')
        self.key_link = f'{self.key_base}.key'

    def get_key_id(self):
        """
        Key ID is symlink target minus trailing ".key"
        """
        self.key_id = keyid_from_filename(self)
        return self.key_id

    def make_new_key(self, opts: ToolOpts):
        """
        Generate new key.
        """
        self.key_id = generate_key(opts, self)

    def make_missing_key(self, opts: ToolOpts):
        """
        check for missing key
         - read key_id from file (in case was just generated)
         - if no key_id then go ahead and make new one
        """
        self.get_key_id()
        if not self.key_id:
            print(f'    Generating key {self.which}')
            self.key_id = generate_key(opts, self)

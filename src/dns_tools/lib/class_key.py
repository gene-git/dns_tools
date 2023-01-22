# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
DNS key class
"""
import os
from .dns_keys import get_key_id_from_keyfile
from .dns_keys import generate_new_key
from .roll_keys import roll_next_to_curr_files

class KeyInfo:
    """ data for one key (current or next) """
    def __init__(self, which, this_key_dir):
        self.which = which              # curr or next
        self.key_id = None
        self.key_base = None
        self.key_link = None
        self.this_key_dir = this_key_dir

    def get_key_base(self):
        """
        get key_base ~ key_dir/{curr,next}
        and key_link ~ key_dir/{curr,next}.key
        """
        which = self.which
        self.key_base = os.path.join(self.this_key_dir, f'{which}')
        self.key_link = os.path.join(self.this_key_dir, f'{which}.key')

    def get_key_id(self):
        """ from existing sym link, get target file without the trailing .key """
        self.key_id = get_key_id_from_keyfile(self)
        return self.key_id

    def make_new_key(self, tool, dnskey):
        """ generate new key """
        self.key_id = generate_new_key(tool, dnskey,  self)

    def make_missing_key(self, tool, dnskey):
        """
        check for missing key
         - read key_id from file (in case was just generated)
         - if no key_id then go ahead and make new one
        """
        self.get_key_id()
        if not self.key_id:
            print(f'    Generating key {self.which}')
            self.key_id = generate_new_key(tool, dnskey, self)

class DnsKey:
    """ all key related tasks provided """
    def __init__(self, dnskeys, domain, ktype, key_dir):

        self.dnskeys = dnskeys                # parent
        self.domain = domain
        self.ktype = ktype                  # zsk or ksk
        self.exts = None
        self.key_dir = key_dir
        self.this_key_dir = os.path.join(key_dir, domain, ktype)

        self.curr = KeyInfo('curr', self.this_key_dir)
        self.next = KeyInfo('next', self.this_key_dir)

        self.key_id = None
        self.key_base = None
        #self.base_name = None
        self.key_link = None

        match ktype:
            case 'ksk' :
                self.exts = ['.all.ds', '.ds', '.key', '.private']
            case 'zsk' :
                self.exts = ['.key', '.private']
            case _:
                print(f'Error: unknown ktype {ktype}')
                return

        # keys in key_dir/<sdomain>/zsk,ksk
        self.curr.get_key_base()
        self.next.get_key_base()
        self.curr.get_key_id()
        self.next.get_key_id()

    def get_key_id(self):
        """ construct key_id, key_base """
        self.curr.get_key_id()
        self.next.get_key_id()

    def make_new_curr_key(self):
        """ make one new key """
        self.curr.make_new_key(self.dnskeys.tool, self)

    def make_new_next_key(self):
        """ make one new key """
        self.next.make_new_key(self.dnskeys.tool, self)

    def make_missing_curr_key(self):
        """ make one new key """
        self.curr.make_missing_key(self.dnskeys.tool, self)

    def make_missing_next_key(self):
        """ make one new key """
        self.next.make_missing_key(self.dnskeys.tool, self)

    def roll_next_to_curr(self, tool):
        """
        roll next key to be new curr key
        """
        roll_next_to_curr_files(tool, self)
        self.curr = self.next
        self.next = None

class DnsKeys:
    """ Handeles ZSK and KSK """
    # pylint: disable=R0903
    def __init__(self, tool, domain, key_dir):
        self.tool = tool            # parent DnsTool instance
        self.key_dir = key_dir
        self.domain = domain

        self.ksk = DnsKey(self, domain, 'ksk', key_dir)
        self.zsk = DnsKey(self, domain, 'zsk', key_dir)

    def roll_ksk_keys(self):
        """
        do any key rolls for this domain
         - rename the sym links next.xxx to curr.xxx
         - key.curr = key_next
         - key_next = None
        """
        self.ksk.roll_next_to_curr(self.tool)

    def roll_zsk_keys(self):
        """
        do any key rolls for this domain
         - rename the sym links next.xxx to curr.xxx
         - key.curr = key_next
         - key_next = None
        """
        self.zsk.roll_next_to_curr(self.tool)

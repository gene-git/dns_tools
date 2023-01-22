# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Initialize for dns-tool
 All controls are command line arguments.
"""
# pylint: disable=R0801,R0903,R0914
import os
import argparse
import datetime
from .class_dnsserv import DnsServer
from .options import get_option_list
from .config import load_config_into_opts
from .config import config_paths_normalize

class DnsOptsRaw:
    """ config and command line options """

    def __init__(self):

        # config options
        self.domains = []
        self.verb = False
        self.test = False
        self.theme = None

        self.work_dir = '/etc/nsd_tools'
        self.key_dir = './keys'
        self.expire = '90d'
        self.dns_user = 'nds'
        self.dns_group = 'nds'
        self.production_zone_dir = '/etc/nsd/zones'

        self.sign_server = ''

        # signing options
        self.sign = False
        self.sign_ksk_next = False
        self.sign_zsk_next = False
        self.serial_bump = False
        self.keep_include = False

        # key options
        self.gen_zsk_curr = False
        self.gen_zsk_next = False
        self.gen_ksk_curr = False
        self.gen_ksk_next = False
        self.ksk_roll_1 = False
        self.ksk_roll_2 = False
        self.zsk_roll_1 = False
        self.zsk_roll_2 = False
        self.print_keys = False

        # config settings
        self.internal = DnsServer()
        self.external = DnsServer()

        # load config
        load_config_into_opts(self)

        # time stamps
        now =  datetime.datetime.now()
        self.now = now.strftime('%Y%m%d-%H%M%S')

        me = 'dns_tools: key (ksk and zsk) generation, zone files sign, key rolls, serial bumps'
        opts = get_option_list()

        par = argparse.ArgumentParser(description=me)

        for opt in opts:
            opt_list, kwargs = opt
            opt_s = opt_list[0]
            if len(opt_list) > 1:
                opt_l = opt_list[1]
                par.add_argument(opt_s, opt_l, **kwargs)
            else:
                par.add_argument(opt_s, **kwargs)

        parsed = par.parse_args()
        if parsed:
            # map options to attributes
            for (opt, val) in vars(parsed).items():
                if val in (None, []):
                    continue
                if opt == 'zones' and val:
                    self.domains = val
                else :
                    setattr(self, opt, val)

class KeyOpts:
    """ options for keys """
    def __init__(self, ktype):
        self.ktype = ktype
        self.gen_curr = False
        self.gen_next = False
        self.roll_1 = False
        self.roll_2 = False
        self.sign_curr = False
        self.sign_next = False

    def set_opt(self, okey, oval):
        """ set correspondingf option for self.ktype """
        if self.ktype == 'ksk':
            txt = 'ksk_'
        else:
            txt = 'zsk_'
        new_okey = okey.replace(txt, '')
        setattr(self, new_okey, oval)

    def do_sign(self):
        """ return true if sign_curr or sign_next is true """
        if self.sign_curr or self.sign_next:
            return True
        return False

class DnsOpts:
    """
    holds config settings are command line options
     - after getting raw options, map to more convenient form
       e.g. group ksk items together and zsk items together.
    """
    # pylint: disable=R0912,R0915
    def __init__(self):
        # actions
        self.okay = True
        self.test = False
        self.do_keys = False
        self.sign = None
        self.theme = None
        self.euid = os.geteuid()

        # config options
        self.domains = []
        self.key_dir = './keys'

        # key options
        self.ksk_opts = KeyOpts('ksk')
        self.zsk_opts = KeyOpts('zsk')

        # config settings
        self.internal = None
        self.external = None

        self.print_keys = False

        _opts_raw = DnsOptsRaw()

        for (okey, oval) in vars(_opts_raw).items():
            if 'ksk_' in okey :
                self.ksk_opts.set_opt(okey, oval)
            elif 'zsk_' in okey:
                self.zsk_opts.set_opt(okey, oval)
            else:
                setattr(self, okey, oval)

        if self.zsk_opts.do_sign() or self.ksk_opts.do_sign():
            self.sign = True

        #
        # roll phase 1 and 2 are mutually exclusive - either but not both
        #
        if self.ksk_opts.roll_1 and self.ksk_opts.roll_2:
            print('Error - ksk_roll must be 1 or 2 not both')
            self.okay = False
            return

        if self.zsk_opts.roll_1 and self.zsk_opts.roll_2:
            print('Error - zsk_roll must be 1 or 2 not both')
            self.okay = False
            return

        #
        # Implied options
        # moving next to curr keys is part of roll itself (no options)
        #
        if self.ksk_opts.roll_1:
            self.serial_bump = True
            self.ksk_opts.gen_next = True
            self.ksk_opts.sign_curr = True
            self.ksk_opts.sign_next = True

            self.zsk_opts.sign_curr = True
            self.sign = True

        if self.ksk_opts.roll_2:
            self.serial_bump = True
            self.ksk_opts.sign_curr = True
            self.zsk_opts.sign_curr = True
            self.sign = True

        if self.zsk_opts.roll_1:
            self.serial_bump = True
            self.zsk_opts.gen_next = True
            self.zsk_opts.sign_curr = True
            self.zsk_opts.sign_next = True

            self.ksk_opts.sign_curr = True
            self.sign = True

        if self.zsk_opts.roll_2:
            self.serial_bump = True
            self.ksk_opts.sign_curr = True
            self.zsk_opts.sign_curr = True
            self.sign = True

        if self.serial_bump:
            self.sign = True    # keep consistent, change zone must resign

        if self.sign:
            self.ksk_opts.sign_curr = True
            self.zsk_opts.sign_curr = True

        for subopt in (self.zsk_opts, self.ksk_opts):
            if subopt.sign_curr or subopt.sign_next:
                self.sign = True
            if subopt.gen_curr or subopt.gen_next:
                self.do_keys = True

        #
        # Normalize all paths to absolute
        #  - relative paths made absolute relative to to work_dir
        #
        config_paths_normalize(self)

        # color turned off when theme is "none"
        if self.theme and self.theme.lower() == 'none':
            self.theme = None

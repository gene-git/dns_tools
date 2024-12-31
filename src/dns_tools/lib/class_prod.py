# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-prod
"""
# pylint: disable=too-many-instance-attributes,invalid-name,too-few-public-methods
# pylint: disable=duplicate-code
import os
import argparse
import datetime
from .class_dnsserv import DnsServer
from .options import get_prod_option_list
from .config import load_config_into_opts
from .config import config_paths_normalize
from .config import config_check
from .zone_perms import set_zone_perms
from .prod import staging_zones_to_production
from .dns_server_restart import restart_dns_servers
from .class_print import Prnt

class ProdOpts:
    """
    holds config settings are command line options for pushing to production
    """
    # pylint: disable=R0912,R0915
    def __init__(self):
        # actions
        self.okay = True
        self.verb = False
        self.theme = None
        self.euid = os.geteuid()

        # config options
        self.test = False
        self.domains = []

        self.work_dir = '/etc/dns_tools'
        self.key_dir = './keys'
        self.sign_server = ''
        self.production_zone_dir = '/etc/nsd/zones'

        self.dns_restart = False
        self.to_production = False
        self.int_ext = 'both'
        self.int_zones = False
        self.ext_zones = False

        # config settings
        self.internal = DnsServer()
        self.external = DnsServer()

        load_config_into_opts(self)

        now =  datetime.datetime.now()
        self.now = now.strftime('%Y%m%d-%H%M%S')

        me = 'dns_prod: pushing dns zone files from staging to production'
        opts = get_prod_option_list()
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
                if val not in (None, []):
                    setattr(self, opt, val)

        #
        # Normalize all paths to absolute
        #   - relative paths made absolute relative to to work_dir
        #
        config_paths_normalize(self)

        #
        # internal/external or both
        #
        if self.int_ext.startswith('int'):
            self.int_zones = True
        elif self.int_ext.startswith('ext'):
            self.ext_zones = True
        else:
            self.int_zones = True
            self.ext_zones = True

        #
        # color turned off when theme is "none"
        #
        if self.theme and self.theme.lower() == 'none':
            self.theme = None


class DnsProd:
    """ Manage pushing to production """
    def __init__(self):

        self.opts = ProdOpts()
        self.okay = self.opts.okay
        self.prnt = Prnt(self.opts.theme)

        # sanity check on inputs
        if not config_check(self.prnt, self.opts):
            self.okay = False

    def to_production(self):
        """
        Copy files on from work staging zone dir to
        production zone dir on dns server
        - restart dns server if asked
        i.e.
         - rsync -a <work_staging_zones>/ [remote_server:]/etc/nsd/zones
        """
        staging_zones_to_production(self)

    def zone_perms(self):
        """ ensure correct owner and permissions """
        set_zone_perms(self)

    def dns_restart(self):
        """ restart dns servers """
        if self.opts.dns_restart:
            restart_dns_servers(self)

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-tool
 All controls are command line arguments.
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from typing import (List)
import os
import datetime

from utils import Prnt
from ._dnsserv import DnsServer
from ._keyopts import KeyOptions
from ._config_read import read_config


class Config:
    """
    Config File Settings

    - shared by DnsTool and DnsProd
    - base_options, ksk_options and zsk_options.

    """
    def __init__(self):
        #
        # Shared config
        #
        self.okay: bool = True
        self.verb: bool = False
        self.test: bool = False
        self.theme: str = ''
        self.euid = os.geteuid()
        self.cwd: str = os.getcwd()

        self.domains: List[str] = []
        self.work_dir: str = '/etc/nsd_tools'
        self.key_dir: str = './keys'
        self.expire: str = '90d'

        self.dns_user: str = 'nsd'
        self.dns_group: str = 'nsd'

        self.dns_restart_cmd: str = ''
        self.production_zone_dir: str = '/etc/nsd/zones'

        self.sign_server: str = ''

        #
        # key options
        # - ksk/zsk algo
        #
        self.key_opts = KeyOptions()

        #
        # DNS server(s) settings
        #
        self.internal = DnsServer()
        self.external = DnsServer()

        #
        # time stamps
        #  - need common time
        #
        now = datetime.datetime.now()
        self.now = now.strftime('%Y%m%d-%H%M%S')

        #
        # Load config file
        #
        _load_config_file(self)

        #
        # Once command line options are set, then theme
        # will be know. So sub class can then initialize
        #
        self.prnt: Prnt


def _load_config_file(conf: Config):
    """
    Read config and save into Config attributes.

    Returns:
        sets conf.okay to False if failed to read config file.
    """
    conf_dict = read_config()
    if not conf_dict:
        conf.okay = False
        return

    for (key, val) in conf_dict.items():

        if key == 'internal':
            for (subkey, subval) in val.items():
                setattr(conf.internal, subkey, subval)

        elif key == 'external':
            for (subkey, subval) in val.items():
                setattr(conf.external, subkey, subval)

        elif key == 'ksk_algo':
            if val:
                conf.key_opts.ksk.algo = val

        elif key == 'zsk_algo':
            if val:
                conf.key_opts.zsk.algo = val

        else:
            setattr(conf, key, val)

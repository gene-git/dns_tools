# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-tool
 All controls are command line arguments.
"""
# pylint: disable=R0903,R0914
import os

class DnsServer:
    """ info for internal or external dns server """
    def __init__(self):
        self.dns_server = None
        self.staging_zone_dir = None

    def set_opt(self, adict):
        """ map dictionary to attributes """
        if not adict:
            return
        for (key, val) in adict.items():
            setattr(self, key, val)

    def set_abs_paths(self, work_dir):
        """ make any relative paths absolute """
        if self.staging_zone_dir :
            if not os.path.isabs(self.staging_zone_dir):
                self.staging_zone_dir = os.path.join(work_dir, self.staging_zone_dir)
        self.staging_zone_dir = os.path.normpath(self.staging_zone_dir)
        self.staging_zone_dir = os.path.abspath(self.staging_zone_dir)

    def check_staging(self):
        """ check staging dir """
        if not self.staging_zone_dir:
            return False
        if os.path.exists(self.staging_zone_dir) and os.path.isdir(self.staging_zone_dir):
            return True
        return False

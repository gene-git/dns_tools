# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
DNS Server Class
"""
from typing import (Dict, Tuple)
import os

from utils import normalize_one_path


class DnsServer:
    """
    Info for DNS server (internal or external).
    """
    def __init__(self):
        self.dns_server: str = ''
        self.staging_zone_dir: str = ''

    def set_opt(self, adict: Dict[str, str]):
        """
        Map dictionary to our attributes.
        """
        if not adict:
            return

        for (key, val) in adict.items():
            setattr(self, key, val)

    def normalize_paths(self, work_dir: str):
        """
        Make relative paths absolute.
        """
        if self.staging_zone_dir:
            self.staging_zone_dir = normalize_one_path(work_dir,
                                                       self.staging_zone_dir)

    def _check_staging(self) -> bool:
        """
        Check staging dir.
        """
        staging_dir = self.staging_zone_dir
        if not staging_dir:
            return False

        if (os.path.exists(staging_dir) and os.path.isdir(staging_dir)):
            return True

        return False

    def check(self) -> Tuple[bool, str]:
        """
        Check have needed info
        """
        if not self.dns_server:
            return (False, 'Missing dns_server')

        if not self._check_staging():
            return (False, 'Missing staging_dir')

        return (True, '')

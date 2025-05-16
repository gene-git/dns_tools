# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-prod
"""
from zone import set_zone_perms

from ._prod_base import DnsProdBase
from ._to_prod import staging_zones_to_production
from ._dns_server_restart import restart_dns_servers


class DnsProduction(DnsProdBase):
    """
    Subclass of DnsProd for any methods in separate files.

    Avoids import cycles.
    """
    def to_production(self):
        """
        Copy zone files from work staging zone to production on dns server.

        e.g. rsync -a <work_staging_zones>/ [remote_server:]/etc/nsd/zones
        """
        staging_zones_to_production(self)

    def zone_perms(self):
        """
        Set correct owner and permissions.
        """
        set_zone_perms(self.opts)

    def dns_restart(self):
        """
        restart dns servers.

        Ignored unless self.opts.dns_restart = True
        """
        if self.opts.dns_restart:
            restart_dns_servers(self)

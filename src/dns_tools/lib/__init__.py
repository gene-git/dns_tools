# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
CLasses to support dns-tool (dnssec, ...)
"""
from .class_dnstool import DnsTool
from .class_prod import DnsProd
from .class_lock import DnsLock

from .zone import zone_file_read
from .zone import zone_file_write
from .dns_serial import zone_get_new_serial
from .dns_serial import zone_update_serial

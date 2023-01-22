# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
CLasses to support dns-tool (dnssec, ...)
"""
from .class_dnstool import DnsTool
from .class_prod import DnsProd
#from .zone import zone_modify
from .zone import zone_file_read
from .zone import zone_file_write
from .dns_serial import zone_get_new_serial
from .dns_serial import zone_update_serial

# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
read version from installed package
"""
from importlib.metadata import version
__version__ = version("dns_tools")

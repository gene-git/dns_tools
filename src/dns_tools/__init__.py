# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
read version from installed package
"""
from importlib.metadata import version
__version__ = version("dns_tools")

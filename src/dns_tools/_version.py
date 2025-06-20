# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Project dns_tools
"""
__version__ = "4.8.0"
__date__ = "2025-06-20"
__reldev__ = "release"


def version() -> str:
    """ report version and release date """
    vers = f'dns_tools: version {__version__} ({__date__})'
    return vers

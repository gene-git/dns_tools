# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Project dns_tools
"""
__version__ = "5.1.0"
__date__ = "2026-01-04"
__reldev__ = "release"


def version() -> str:
    """ report version and release date """
    vers = f'dns_tools: version {__version__} ({__date__})'
    return vers

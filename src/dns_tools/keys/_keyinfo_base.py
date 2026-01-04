# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
DNS key info base class
"""
# pylint: disable=too-few-public-methods


class KeyInfoBase:
    """
    Base Key Class for one key - data only.

    Used for either 'curr' or 'next'.
    Methods are in subclass KeyInfo
    """
    def __init__(self, domain: str, which: str,
                 key_type: str, this_key_dir: str):
        """
        Data:
            which: "curr" or "next" (will change on a roll)
            key_type: "ksk" or "zsk"   (cannot change)

        """
        self.which: str = which              # curr or next
        self.ktype: str = key_type
        self.domain: str = domain
        self.this_key_dir: str = this_key_dir
        self.key_id: str = ''
        self.key_base: str = ''
        self.key_link: str = ''

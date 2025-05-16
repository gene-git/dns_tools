# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Handle generating keys
"""
# pylint: disable=invalid-name,too-many-locals
import os

from ._keyinfo_base import KeyInfoBase


def keyid_from_filename(key_info: KeyInfoBase) -> str:
    """
    Get existing key_id:

    key_id is file the key link points to (minus trailing .key)
    Returns linkname and basename or None if link doesn't exist
    """
    key_link = key_info.key_link
    this_key_dir = key_info.this_key_dir
    key_id = ''

    if os.path.islink(key_link):
        targ_file = os.readlink(key_link)
        file = os.path.basename(targ_file)
        targ_path = os.path.join(this_key_dir, targ_file)

        if os.path.isfile(targ_path):
            key_id = file[0:-4]                 # strip trailing .key

    return key_id

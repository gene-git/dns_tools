# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Key File extensions
"""


def keyfile_extensions(key_type: str) -> list[str]:

    """
    list of file extensions for given key type.

    Args:
        key_type (str):
            "ksk" or "zsk"

    Returns:
        list(str):
        list of key file extensions for "key_type"
        If unknown key type, an empty list is returned.
    """
    exts: list[str] = []
    match key_type:
        case 'ksk':
            exts = ['.all.ds', '.ds', '.key', '.private']

        case 'zsk':
            exts = ['.key', '.private']

        case _:
            print(f'Error: unknown key_type {key_type}')

    return exts

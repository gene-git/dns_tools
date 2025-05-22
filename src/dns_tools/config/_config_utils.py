# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Read options from config files:
    1) ./conf.d/config
    2) /etc/dns_tools/conf.d/config
"""
import os


def directory_check(adir, is_local: bool = True) -> tuple[bool, str]:
    """
    Check directory:

    Args:
        adir (str):
        Directory to check.

        is_local (bool):
        If is_local file system, then we can check if path exists etc.
        If not local (remote), then skip this check.
    """
    if not adir:
        return (False, 'Missing directory')

    if is_local and not (os.path.exists(adir) and os.path.isdir(adir)):
        return (False, f'Invalid directory: {adir}')

    return (True, '')


def str_variable_check(variable: str) -> tuple[bool, str]:
    """
    String variable check
    Can only check existance.

    Return - same as for directory_check()
    """
    if not variable:
        return (False, 'Missing variable')
    return (True, '')

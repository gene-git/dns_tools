# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Shared File Lock Class
"""
import os
from lockmgr import LockMgr


class DnsLock:
    """ File locking to ensure 1 tool can run at a time """
    def __init__(self):
        euid = os.geteuid()
        lockdir = f'/tmp/.dns-tool-{euid}/'
        os.makedirs(lockdir, exist_ok=True)
        lockfile = f'{lockdir}/lock'

        # very generous timeout
        timeout = 5.0 * 60.0
        self.lockmgr = LockMgr(lockfile, timeout=timeout)

    def acquire_lock(self) -> bool:
        """
        Get the lock
        """
        print('Acquiring lock')
        if self.lockmgr.acquire():
            return True

        print('Failed to acquire lock (another dns-tool is holding it)')
        return False

    def release_lock(self):
        """ release the lock """
        self.lockmgr.release()

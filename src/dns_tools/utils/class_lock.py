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
        self.lockmgr = LockMgr(lockfile)

    def acquire_lock(self):
        """ get lock """
        print('Acquiring lock')
        tries = 1
        max_tries = 5
        gotit = self.lockmgr.acquired
        while not gotit and tries < max_tries:
            gotit = self.lockmgr.acquire_lock(wait=True, timeout=60)
            if gotit:
                return gotit
            tries += 1
        if not gotit:
            print('Failed to acquire lock (another dns-tool is holding it)')
        return self.lockmgr.acquired

    def release_lock(self):
        """ get lock """
        self.lockmgr.release_lock()

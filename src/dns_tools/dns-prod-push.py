#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Tool to push into production
  - work staging to production staging
  - production staging to live production
 gc - 2022
"""
# pylint: disable=invalid-name
from lib import DnsProd
from lib import DnsLock

def main():
    """
    - work staging to production staging
    - production staging to live production
    """
    #
    # check no other dns-tool active
    # If so, wait until we an get the lock
    #
    lock = DnsLock()
    got_lock = lock.acquire_lock()
    if not got_lock:
        return

    prod = DnsProd()
    if not prod.okay:
        return

    if prod.opts.to_production:
        prod.to_production()

    if prod.opts.dns_restart:
        prod.dns_restart()

if __name__ == '__main__':
    main()

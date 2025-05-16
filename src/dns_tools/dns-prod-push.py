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
from production import DnsProduction
from utils import DnsLock


def main():
    """
    - Work staging to production
    - Restart dns server(s)
    """
    #
    # Self protect - hold run if already running.
    # Wait until we get lock to proceed
    #
    lock = DnsLock()
    got_lock = lock.acquire_lock()
    if not got_lock:
        return

    prod = DnsProduction()
    if not prod.okay:
        print('Error: failed initilize DnsProduction')
        return

    if prod.opts.to_production:
        prod.to_production()
        if not prod.okay:
            print('Error: failed to production')
            return

    if prod.opts.dns_restart:
        prod.dns_restart()
        if not prod.okay:
            print('Error: failed to restart dns servers')
            return

    print('Success: all done')


if __name__ == '__main__':
    main()

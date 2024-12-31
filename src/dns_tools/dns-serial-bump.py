#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Read zone file = bump serial and write to stdout
"""
# pylint: disable=invalid-name
import argparse
from lib import zone_file_read
from lib import zone_file_write
from lib import zone_get_new_serial
from lib import zone_update_serial
from lib import DnsLock

def options():
    """
    Command line options
    """
    par = argparse.ArgumentParser(description='DNS Serial tool')
    par.add_argument('-c','--check',
                     action='store_true',
                     help='Check serial from zonefile')

    par.add_argument('zonefile', nargs='+',
                     help='Zone file(s) with serial numbers')
    parsed = par.parse_args()
    return parsed


def main():
    """
    Standalone tool to check and/or bump zone file serial
    """
    lock = DnsLock()
    got_lock = lock.acquire_lock()
    if not got_lock:
        return

    opts = options()
    zonepath_list = opts.zonefile
    check = opts.check

    if not zonepath_list:
        print('Missing zone file(s) to read')
        return

    for zonepath in zonepath_list:
        print(f'{zonepath}')
        zone = zone_file_read(zonepath)
        if not zone:
            print(f'  Failed to read zone file : {zonepath}')
            return

        print('  Checking serial:')
        (serial, new_serial) = zone_get_new_serial(zone)
        print(f'    Serial     = {serial}')
        print(f'    New Serial = {new_serial}')

        if not check and new_serial:
            print('    Saving updated zonefile')
            zone_new = zone_update_serial(zone)
            zone_file_write(zone_new, zonepath)

if __name__ == '__main__':
    main()

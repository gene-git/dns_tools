#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 DNSSEC management tool - aka easy dnssec

 Generate and manage KSK/ZSK keys. Handle key rolling.
 Signs dns zones with ksk/zsk current key, and for phase 1 of key roll
 also signes with the next key.

 Uses the ldns tools

 zone signing does the following:

   - zone:
       - Backup zone to Prev/zone
       - Update serial and save back to zone
   - read updated zone file - this also expands in $INCLUDE files
   - sign the expanded zone file
   - write signed zone file to dated file signed/data/xxx
   - create link signed/zone.signed -> data/xxx

 gc - 2022
"""
# pylint: disable=invalid-name, too-many-return-statements
from tool import DnsTool
from utils import DnsLock


def main():
    """
    Tool executes key and signing actions
    """
    #
    # check no other dns-tool active
    # If so, wait until we an get the lock
    #
    lock = DnsLock()
    got_lock = lock.acquire_lock()
    if not got_lock:
        return

    tool = DnsTool()
    if not tool.okay:
        lock.release_lock()
        return

    if tool.opts.print_keys:
        tool.print_keys()

    #
    # Key Updates
    # e.g. create new 'next' key
    #
    tool.do_key_updates()
    if not tool.okay:
        print('Error: key_update failed')
        return

    #
    # Make any required signing keys if not available
    #
    tool.create_missing_keys()
    if not tool.okay:
        print('Error: create missing keys failed')
        return

    #
    # If phase 2 roll then move next to be current key
    #
    tool.do_key_rollovers()
    if not tool.okay:
        print('Error: key rolloever failed')
        return

    #
    # Sign whatever needs signing.
    #
    tool.do_sign_zones()
    if not tool.okay:
        print('Error: zone sign failed')
        return

    #
    # Ensure correct file permissions and owner
    #
    tool.zone_perms()
    if not tool.okay:
        print('Error: zone permissions failed')
        return

    #
    # Caller should now invoke separate tool dns-prod-push
    # to push newly signed zones to dns primary servers
    #
    lock.release_lock()

    print('Success: all done')


if __name__ == '__main__':
    main()

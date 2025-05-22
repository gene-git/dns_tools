# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""

 DNSSEC management tool

 -ksk  - generate new KSK keys
 -zsk  - generate new ZSK keys
 -sign - sign zone
 -expire - zone signing expires in X days

 -no-serialn   - dont increment the serial in unsigned zone (original) file
                   signed zone inherits same serial.

 -keep-include - $INCLUDES are inserted into zone file before signing
                 this file is not kept by default.
                 zone -> zone.included -> zone.included.signed
               - only for testing and debugging and
                 should NOT be used in production

 This tool uses the ldns-xxx tools

 zone signing does the following:

   - zone:
       - Backup zone to Prev/zone
       - Update serial and save back to zone
   - read updated zone file - this also expands in $INCLUDE files
   - sign the expanded zone file
   - write signed zone file to signed/data/xxx
   - create link singed/zone.signed -> data/xxx

 gc - 2022
"""
import os

from utils import rel_from_abs_path
from utils import make_dir_if_needed
from zone import zone_file_read
from zone import zone_file_write
from zone import zone_expand_includes
from zone import zone_update_serial

from .dnstool_base import DnsToolBase
from .sign import zone_sign
from .sign import get_signing_key_base_names


def _do_one_zone(tool: DnsToolBase, domain: str, staging: str,
                 zone: list[str], zone_file_path: str):
    """
    Sign one zone file
    """
    # pylint: disable=too-many-locals
    msg = tool.opts.prnt.msg
    opts = tool.opts

    keep_include = opts.keep_include
    zone_fpath_rel = rel_from_abs_path(zone_file_path, opts.work_dir)

    msg(f'  {domain}\n', fg='norm')
    if tool.opts.serial_bump:

        #
        # Back up zone and update serial
        #
        zone_new = zone_update_serial(zone)

        saved_dir = os.path.dirname(zone_file_path)
        saved_dir = f'{saved_dir}.prev'
        saved_dir_rel = rel_from_abs_path(saved_dir, opts.work_dir)
        saved_zone_file = os.path.join(saved_dir, domain)

        if opts.verb:
            space = f'{"":10s} {"":20s}'
            print(f'{"":10s} {"Backing up":20s}')
            print(f'{space}: {zone_fpath_rel} to {saved_dir_rel}')

        if not opts.test:
            make_dir_if_needed(saved_dir)
            os.rename(zone_file_path, saved_zone_file)

        msg(f'{"":10s} {"Updating serial":20s}: {zone_fpath_rel}\n')
        zone_file_write(zone_new, zone_file_path)
        zone = zone_new.copy()

    if opts.key_opts.sign:
        msg(f'{"":10s} {"Signing":20s}: {zone_fpath_rel}\n')

        #
        # expand $INCLUDE the zone
        #
        zone_file_exp_path = f'{zone_file_path}-exp'
        if not opts.test:
            zone_exp = zone_expand_includes(zone)

        #
        # sign with one or more keys
        #
        (ksk_keys, zsk_keys) = get_signing_key_base_names(tool, domain)

        #
        # NB comments are removed
        #
        if not opts.test:
            zone_file_write(zone_exp, zone_file_exp_path)

        zone_signed_link = 'zone'
        zone_sign(tool, staging, domain, zone_file_exp_path,
                  ksk_keys, zsk_keys, zone_signed_link)

        if not keep_include and not opts.test:
            if os.path.isfile(zone_file_exp_path):
                os.unlink(zone_file_exp_path)


def dns_process_signing_zones(tool: DnsToolBase):
    """
    Sign each zone/domain with curr key,
    With next key if indicated by roll_1.
    """
    okay = True
    opts = tool.opts
    msg = tool.opts.prnt.msg

    if not opts.domains:
        return okay

    start_cwd = os.getcwd()
    #
    # working zone files dir
    #
    staging_dirs = []
    if opts.internal:
        staging_dirs.append(opts.internal.staging_zone_dir)

    if opts.external:
        staging_dirs.append(opts.external.staging_zone_dir)

    for staging in staging_dirs:
        rel_staging = rel_from_abs_path(staging, tool.opts.work_dir)
        msg(f'\n Signing zones in {rel_staging}\n', fg='high')

        try:
            os.chdir(staging)
            okay = True
        except OSError as err:
            msg(f' Error Failed to chdir to {staging}: {err}\n',
                fg='error')
            okay = False
            continue

        for domain in tool.opts.domains:
            zone_file_path = os.path.join(staging, domain)
            if not os.path.isfile(zone_file_path):
                msg(f'  Warning Missing file: {zone_file_path}\n',
                    fg='warn')
                continue

            zone = zone_file_read(zone_file_path)

            _do_one_zone(tool, domain, staging, zone, zone_file_path)

    os.chdir(start_cwd)

    return okay

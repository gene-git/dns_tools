# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Ensure correct permissions of all zone files
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments
import os
import stat

from utils import get_uid_gid
from config import Config


def set_zone_perms(opts: Config):
    """
    Ensure owner by nsd:nsd.

    - set dir to u=rwx,go=rx
    - set files to u=rw,g=r,o=
    """
    msg = opts.prnt.msg
    msg('\nSetting staging zone permissions\n', fg='high')

    #
    # User/Group owner
    dns_user = 'nsd'
    dns_group = 'nsd'

    if opts.dns_user:
        dns_user = opts.dns_user

    if opts.dns_group:
        dns_group = opts.dns_group

    # need root to change owner
    euid = opts.euid

    if euid == 0:
        (dns_uid, dns_gid) = get_uid_gid(dns_user, dns_group)
    else:
        (dns_uid, dns_gid) = (-1, -1)
        text = 'Warning: Must be root to set file ownership '
        text += f'{dns_user}:{dns_group}\n'
        msg(text, fg='warn')

    int_staging = opts.internal.staging_zone_dir
    ext_staging = opts.external.staging_zone_dir

    dmode = (stat.S_IRWXU |
             stat.S_IRGRP |
             stat.S_IXGRP |
             stat.S_IROTH |
             stat.S_IXOTH
             )

    fmode = (stat.S_IRUSR |
             stat.S_IWUSR |
             stat.S_IRGRP
             )

    _set_perms(opts, dns_uid, dns_gid, dmode, fmode, int_staging)
    _set_perms(opts, dns_uid, dns_gid, dmode, fmode, ext_staging)


def _set_perms(opts: Config, uid: int, gid: int,
               dmode: int, fmode: int, adir: str):
    """
    Set permissions and owner recursively
     - if uid/gid are -1, then owner/group are unchanged
    """
    msg = opts.prnt.msg

    if not os.path.exists(adir) or not os.path.isdir(adir):
        return

    #
    # scan directory
    #
    try:
        scan = os.scandir(adir)
    except OSError as err:
        msg(f'Failed to scan {adir}: {err}\n', fg='warn')
        scan = None

    if not scan:
        return

    #
    # set perms
    #
    try:
        os.chmod(adir, dmode)
        os.chown(adir, uid, gid)
    except OSError as err:
        msg(f'Failed to set perms on {adir}: {err}\n', fg='warn')
        return

    for item in scan:
        this_mode = fmode
        if item.is_dir():
            this_mode = dmode
        try:
            os.chmod(item.path, this_mode)
            os.chown(item.path, uid, gid)
        except OSError as err:
            msg(f'Failed set perms on {item.path}: {err}\n', fg='warn')
            continue

        if item.is_dir():
            _set_perms(opts, uid, gid, dmode, fmode, item.path)

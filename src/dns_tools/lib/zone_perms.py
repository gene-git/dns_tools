# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Ensure correct permissions of all zone files
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments
import os
import stat
from .tools import get_uid_gid

def set_zone_perms(tool):
    """
     - Ensure owner by nsd:nsd
     - set dir to u=rwx,go=rx
     - set files to u=rw,g=r,o=
    """
    prnt = tool.prnt

    prnt.msg('\nSetting staging zone permissions\n', fg_col='high')
    #
    # User/Group owner
    dns_user = 'nsd'
    dns_group = 'nsd'

    if tool.opts.dns_user :
        dns_user = tool.opts.dns_user
    if tool.opts.dns_group :
        dns_group = tool.opts.dns_group

    # need root to change owner
    euid = tool.opts.euid

    if euid == 0:
        (dns_uid, dns_gid) = get_uid_gid(dns_user, dns_group)
    else:
        (dns_uid, dns_gid) = (-1, -1)
        prnt.msg(f'Warning: Must be root to set file ownership to {dns_user}:{dns_group}\n',
                 fg_col='warn')

    int_staging = tool.opts.internal.staging_zone_dir
    ext_staging = tool.opts.external.staging_zone_dir

    dmode = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    fmode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

    _set_perms(prnt, dns_uid, dns_gid, dmode, fmode, int_staging)
    _set_perms(prnt, dns_uid, dns_gid, dmode, fmode, ext_staging)

def _set_perms(prnt, uid, gid, dmode, fmode, adir):
    """
    Set permissions and owner recursively
     - if uid/gid are -1, then owner/group are unchanged
    """

    if not os.path.exists(adir) or not os.path.isdir(adir):
        return

    #
    # scan directory
    #
    try:
        scan = os.scandir(adir)
    except OSError as err:
        prnt.msg(f'Failed to scan {adir} : {err}\n', fg_col='warn')
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
        prnt.msg(f'Failed to set perms on {adir} : {err}\n', fg_col='warn')
        return

    for item in scan:
        this_mode = fmode
        if item.is_dir():
            this_mode = dmode
        try:
            os.chmod(item.path, this_mode)
            os.chown(item.path, uid, gid)
        except OSError as err:
            prnt.msg(f'Failed set perms on {item.path} : {err}\n', fg_col='warn')
            continue

        if item.is_dir:
            _set_perms(prnt, uid, gid, dmode, fmode, item.path)

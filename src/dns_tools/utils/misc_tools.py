# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
supporting tools
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments
import os
import socket
import pwd
import grp

from .run_prog_local import run_prog


def _construct_remote_call(host_src: str, src: str, opts: list[str],
                           host_dst: str, dst: str) -> list[str]:
    """
    Handle:
       1 host: use rsync
         ssh needed to/from that host
       2 hosts
        - both same host - use ssh host rsync  local
          ssh to that host needed
          ssh from local machine to host
        - diff: ssh host_src rsync src host_dst:dst
          ssh needed from local to src and from src to dest
    NB
      - this requires ssh access to be allowed when its used.
    """
    rsync = ['/usr/bin/rsync'] + opts
    ssh = ['/usr/bin/ssh', '-T']

    #
    # Traack if any of src/dst are remote
    #
    num_hosts = 0
    if host_src:
        num_hosts += 1

    if host_dst:
        num_hosts += 1

    if num_hosts == 0:
        pargs = rsync + [src, dst]

    elif num_hosts == 1:
        if host_src:
            src = f'{host_src}:{src}'
        if host_dst:
            dst = f'{host_dst}:{dst}'

        pargs = rsync + [src, dst]

    elif host_src == host_dst:
        # src and target on same remote host
        pargs = ssh + [host_src] + rsync + [src, dst]

    else:
        # src and target on different remote hosts
        dst = f'{host_dst}:{dst}'
        pargs = ssh + [host_src] + rsync + [src, dst]

    return pargs


def rsync_copy(host_src: str, src: str, rsync_opts: list[str],
               host_dst: str, dst: str, test: bool, verb: bool) -> bool:
    """
    Use rsync to copy src to dst
      - if host_src then:
           ssh -T host_src <rsync_command>
         else
           <rsync_command>
      - <rsync_command>
         rsync opts src <dest>
      - <dest> is host_dst:dst if host_dst provided otherwise dst

      typical rsync_opts ['-av', '--owner', '--mkpath']
      Reminder for content of dir use '/' at end of src.
    """
    okay = True
    if not src or not dst:
        return okay

    pargs = _construct_remote_call(host_src, src, rsync_opts, host_dst, dst)

    (retc, _output, errors) = run_prog(pargs, test=test, verb=verb)
    if retc != 0:
        okay = False
        print('  Error: rsync failed')
        if errors:
            print(errors)
    return okay


def get_uid_gid(username: str, groupname: str) -> tuple[int, int]:
    """
    Get numerical uid/gid for user/group names
    defaults to -1
    """
    uid = -1
    gid = -1
    if username:
        try:
            pwnam = pwd.getpwnam(username)
            uid = pwnam[2]
        except KeyError as err:
            print(f'Error getting uid for {username}: {err}')

    if groupname:
        try:
            grnam = grp.getgrnam(groupname)
            gid = grnam[2]
        except KeyError as err:
            print(f'Error getting gid for {groupname}: {err}')

    return (uid, gid)


def get_my_hostname():
    """ return (hostname, fqdn) """
    fqdn = socket.gethostname()
    host = fqdn.split('.')[0]
    return (host, fqdn)


def normalize_one_path(pre_dir: str | None, fpath: str) -> str:
    """
    Normalize one path.

    Args:
        pre_dir (str|None):
        If set, prepend: path = pre_dir/fpath

        fpath (str):
        Path to file or directory.

    Returns:
        str:
        if fpath is absolute path then normalize and return
        if pre_dir is set and fpath is relative then prepend
        to fpath and then normalize.
        Normalized and absolute path.
    """
    if not fpath:
        return ''

    if pre_dir and not os.path.isabs(fpath):
        path = os.path.join(pre_dir, fpath)
    else:
        path = fpath

    path = os.path.abspath(os.path.normpath(path))
    return path

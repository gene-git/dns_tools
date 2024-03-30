# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
supporting tools
"""
# pylint: disable=too-many-arguments
import os
import socket
import pwd
import grp

from .run_prog import run_prog

def make_dir_if_needed(pathdir):
    """ make dir """
    try:
        os.makedirs(pathdir, exist_ok=True)
    except OSError as err:
        print(f'Error making directory {pathdir} : {err}')

def make_symlink (target, linkname):
    """
    Does equivalent to:  ln -s src dst
    Will overwrite existing link
    A correct existing link is not replaced
    """
    done = False

    #
    # Check if exists and valid
    # remove if wrong link
    #
    if os.path.islink(linkname):
        targ = os.readlink(linkname)
        if targ == target:
            done = True
        else:
            os.unlink(linkname)

    if not done:
        try:
            os.symlink(target, linkname)
        except OSError:
            pass
    return True

def os_scandir(tdir):
    """
    wrapper around scandir to handle exceptions
    """
    scan = None
    if os.path.exists(tdir) and os.path.isdir(tdir) :
        try:
            scan = os.scandir(tdir)
        except OSError as _error:
            scan = None
    return scan

#
# List contents of directory
#   [files, directories, links]
def get_dirlist(indir, which='name'):
    """
    Get a list of files in a local directory
    returns a list of files/dirs/links in a directory
    which - 'name' returns filename, 'path' returns the 'path'

    [flist, dlist, llist]
        flist = list of files
        dlist = list of dirds
        llist = list of links
    NB order care needed - symlinks are also files or dirs -
    so always check link before file or dir as we want links separated
    whether or not they point to a dir or file.
    """
    flist = []
    dlist = []
    llist = []

    scan = os_scandir(indir)
    if scan:
        for item in scan:
            file = item.name
            if which == 'path':
                file = item.path

            if item.is_symlink():
                llist.append(file)

            elif item.is_file() :
                flist.append(file)

            elif item.is_dir():
                dlist.append(file)

        scan.close()
    return [flist, dlist, llist]

def latest_file_mod_time (path,recurse=True):
    """
    Most recent modification time of any file in directory hierarchy
     - unused - delete
    """
    mtime = None
    if not path :
        return mtime

    recurse = True
    mtime = os.path.getmtime(path)

    if path and os.path.exists(path) and os.path.isdir(path) :
        scan = os.scandir(path)
        for item in scan:
            mtime_new = os.path.getmtime(item.path)
            mtime = max(mtime, mtime_new)
            if recurse and item.is_dir():
                mtime_new = latest_file_mod_time(item.path, recurse)
                mtime = max(mtime, mtime_new)

    return mtime

def open_file(path, mode):
    """
    Open a file and return file object
    """
    # pylint: disable=W1514,R1732
    try:
        fobj = open(path, mode)
    except OSError as err:
        print(f'Error opening file {path} : {err}')
        fobj = None
    return fobj

def rel_from_abs_path(abs_path, lead_dir):
    """
    if abs_path is of form lead_dir/xxx
      - return xxx
    """
    if lead_dir in abs_path:
        rel_path = os.path.relpath(abs_path, lead_dir)
        return rel_path
    return abs_path

def _construct_remote_call(host_src, src, opts, host_dst, dst):
    """
    Handle:
       1 host : use rsync
         ssh needed to/from that host
       2 hosts
        - both same host - use ssh host rsync  local
          ssh to that host needed
          ssh from local machine to host
        - diff : ssh host_src rsync src host_dst:dst
          ssh needed from local to src and from src to dest
    NB
      - this requires ssh access to be allowed when its used.
    """
    rsync = ['/usr/bin/rsync'] + opts
    ssh = ['/usr/bin/ssh', '-T']

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

def rsync_copy (host_src, src, rsync_opts, host_dst, dst, test, verb):
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

    pargs =  _construct_remote_call(host_src, src, rsync_opts, host_dst, dst)

    [retc, _output, errors] = run_prog(pargs, test=test, verb=verb)
    if retc != 0:
        okay = False
        print('  Error : rsync failed')
        if errors:
            print(errors)
    return okay

def get_uid_gid(username, groupname):
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
            print(f'Error getting uid for {username} : {err}')

    if groupname:
        try:
            grnam = grp.getgrnam(groupname)
            gid = grnam[2]
        except KeyError as err:
            print(f'Error getting gid for {groupname} : {err}')

    return (uid, gid)

def get_my_hostname():
    """ return (hostname, fqdn) """
    fqdn = socket.gethostname()
    host = fqdn.split('.')[0]
    return (host, fqdn)

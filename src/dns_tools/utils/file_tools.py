# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
supporting tools
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments
from typing import (IO)
import os


def make_dir_if_needed(pathdir: str):
    """
    make dir
    """
    try:
        os.makedirs(pathdir, exist_ok=True)
    except OSError as err:
        # print(f'Error making directory {pathdir}: {err}')
        raise OSError(f'Error making directory {pathdir}') from err


def make_symlink(target: str, linkname: str) -> bool:
    """
    Does equivalent to:  ln -s src dst
    Will overwrite existing link
    A correct existing link is not replaced
    """
    #
    # Check if exists and valid
    # remove if wrong link
    #
    done = False
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


def get_dirlist(indir: str, which: str = 'name'
                ) -> tuple[list[str], list[str], list[str]]:
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
    flist: list[str] = []
    dlist: list[str] = []
    llist: list[str] = []

    scan = None
    if os.path.exists(indir) and os.path.isdir(indir):
        try:
            scan = os.scandir(indir)
        except OSError:
            scan = None

    if not scan:
        return (flist, dlist, llist)

    for item in scan:
        file = item.name
        if which == 'path':
            file = item.path

        if item.is_symlink():
            llist.append(file)

        elif item.is_file():
            flist.append(file)

        elif item.is_dir():
            dlist.append(file)
    scan.close()
    return (flist, dlist, llist)


def open_file(path: str, mode: str) -> IO | None:
    """
    Open a file and return file object

    Returns:
        IO | None:
        File object - IO = TextIO or BinaryIO
    """
    # pylint: disable=W1514,R1732
    try:
        fobj = open(path, mode)
    except OSError as err:
        print(f'Error opening file {path}: {err}')
        fobj = None
    return fobj


def rel_from_abs_path(abs_path: str, lead_dir: str) -> str:
    """
    if abs_path is of form lead_dir/xxx
      - return xxx
    """
    if lead_dir in abs_path:
        rel_path = os.path.relpath(abs_path, lead_dir)
        return rel_path
    return abs_path

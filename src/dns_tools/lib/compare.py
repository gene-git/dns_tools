# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Compare 2 files same name different dir -
 used to check if zone file has changed
"""
# pylint: disable=R0914,R0912
import os
from .zone import zone_file_read

def compare_files(dir1, dir2, file, verb=False):
    """
     Compare same filename in 2 dirs - report if different
     If a link we compare content of what link points to
    """
    files_same = True
    path_1 = os.path.join(dir1, file)
    path_2 = os.path.join(dir2, file)

    link_1 = False
    link_2 = False
    exist_1 = False
    exist_2 = False

    if os.path.exists(path_1):
        exist_1 = True
        if os.path.islink(path_1):
            link_1 = True

    if os.path.exists(path_2):
        exist_2 = True
        if os.path.islink(path_2):
            link_2 = True

    is_link = link_1 or link_2
    if not exist_1 and not exist_2:
        # neither exists - call it the same
        files_same = True
        tdiff = 0.0
        is_link = False
        link_targ_same = False
        return [files_same, tdiff, is_link, link_targ_same]

    if (exist_1 and not exist_2 ) or (not exist_1 and exist_2):
        files_same = False
        if exist_1:
            tdiff = 1.0
        else:
            tdiff = -1.0
        link_targ_same = False
        return [files_same, tdiff, is_link, link_targ_same]

    #
    # time stamp
    #
    mtime_1 = os.path.getmtime(path_1)
    mtime_2 = os.path.getmtime(path_2)
    tdiff = mtime_1 - mtime_2

    #
    # Content
    #
    zone_1 = zone_file_read(path_1)
    zone_2 = zone_file_read(path_2)

    if zone_1 != zone_2:
        if verb:
            print (f'Files differ: {path_1} : {path_2}')
        files_same = False

    #
    # link check
    #
    link_targ_same = False
    if link_1 and link_2:
        targ_1 = os.readlink(path_1)
        targ_2 = os.readlink(path_2)
        if targ_1 == targ_2:
            link_targ_same = True
        elif verb:
            print (f'Files are links but not same target {targ_1} : {targ_2}')

    return [files_same, tdiff, is_link, link_targ_same]

# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Roll keys

 Roll next key to be current.
 This replaces the curr link (if it exists) with the next link
 No checks are performed here - if reach here all should be in order
 We require next be existing valid link(s) to all the required key(s)
"""
import os
from .tools import rel_from_abs_path

def roll_next_to_curr_files(tool, kinfo):
    """
    For one "key" instance i.e. for one domain
     make the next key the new curr key.
     next must exist - should we validate?
    """
    okay = True
    ktype = kinfo.ktype
    curr_key_base = kinfo.curr.key_base
    next_key_base = kinfo.next.key_base
    exts = kinfo.exts
    opts = tool.opts

    for ext in exts:
        fcur = curr_key_base + ext
        fnxt = next_key_base + ext

        fcur_rel = rel_from_abs_path(fcur, tool.opts.work_dir)
        fnxt_rel = rel_from_abs_path(fnxt, tool.opts.work_dir)

        if os.path.islink(fnxt):
            try:
                print(f'  Rolling {ktype} {fnxt_rel} to {fcur_rel}')
                if not opts.test:
                    os.rename(fnxt, fcur)
            except OSError as err:
                print(f'  ** Error Rolling {ktype} {fnxt} to {fcur} - {err}')
                okay = False
        else:
            print(f'  ** Error Rolling {ktype} : Missing link {fnxt}')
            okay = False
    return okay

# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Given a list of color names and a name (can be partial) find the match.
    e.g. given ['black', 'blue', 'brown']
    black would be matched by bla
    blue                   by blu
    etc.
    bl would not be a unique match - in this case we return the first match in list.
    We want to minimize failure
"""

def _get_matches(cnt, num_max, col, col_list):
    """
    return matches of first 'cnt' chars
    """
    if col in col_list:
        return [col]

    sub_list = []
    for color in col_list:
        if len(color) >= cnt and col[0:cnt] == color[0:cnt]:
            sub_list.append(color)
    if len(sub_list) > 1 and cnt <= num_max:
        sub_list = _get_matches (cnt + 1, num_max, col, sub_list)
    return sub_list

def color_pick (col, col_list):
    """
    Find matching color to 'col' which is a full or partial name
    """
    if not col:
        return None
    num_max = len(col)
    matches = _get_matches (1, num_max, col, col_list)
    if matches :
        return matches[0]
    return None

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Given a list of color names and a name (can be partial) find the match.

e.g. given ['black', 'blue', 'brown']
     black matched by bla
     blue  mathed by blu
     etc.

bl would not be a unique match. So return the first match in list.
We want to minimize failure
"""
from typing import (List)


def _get_matches(cnt: int, num_max: int,
                 col: str, col_list: List[str]) -> List[str]:
    """
    return matches of first 'cnt' chars
    of col in col_list
    """
    if col in col_list:
        return [col]

    sub_list = []
    for color in col_list:
        if len(color) >= cnt and col[0:cnt] == color[0:cnt]:
            sub_list.append(color)

    if len(sub_list) > 1 and cnt <= num_max:
        sub_list = _get_matches(cnt + 1, num_max, col, sub_list)

    return sub_list


def color_pick(color: str, color_list: List[str]) -> str:
    """
    Find matching color to 'col' which is a full or partial name
    in col_list
    """
    if not color:
        return ''

    num_max = len(color)
    matches = _get_matches(1, num_max, color, color_list)
    if matches:
        return matches[0]
    return ''

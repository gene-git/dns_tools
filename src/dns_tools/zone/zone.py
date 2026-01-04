# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
zone file read and wrte
"""
from dns_tools.utils import open_file


def zone_file_read(zone_file: str) -> list[str]:
    """
     Read zone file and return list of rows
    """
    zone: list[str] = []
    if not zone_file:
        return zone

    fobj = open_file(zone_file, 'r')
    if fobj:
        zone = fobj.readlines()
        fobj.close()
    return zone


def zone_file_write(zone: list[str], zone_file: str) -> bool:
    """
    Write zone file given list of rows.
    """
    okay = False
    if not zone or not zone_file:
        return okay

    fobj = open_file(zone_file, 'w')
    if fobj:
        for row in zone:
            fobj.write(row)
        fobj.close()
        okay = True
    return okay


def zone_expand_includes(zone: list[str]) -> list[str]:
    """
     Modify zone by expanding any $INCLUDE files
    """
    zone_new: list[str] = []
    if not zone:
        return zone_new

    #
    # Expand $include
    #
    for row in zone:
        # expand INCLUDE if not inside comment
        if '$INCLUDE' in row and not row.startswith(';'):
            srow = row.split()
            file = srow[1]
            zone_new.append('\n; ** begin expanded ' + row + '\n')
            included = zone_file_read(file)
            zone_new = zone_new + included
            zone_new.append('\n; ** end expanded ' + row + '\n')
        else:
            zone_new.append(row)

    return zone_new

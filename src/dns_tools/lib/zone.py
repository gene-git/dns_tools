# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
zone file read and wrte
"""
from .tools import open_file

def zone_file_read (zone_file):
    """
     Read zone file and return list of rows
    """
    zone = []
    if not zone_file:
        return zone

    fobj = open_file(zone_file,'r')
    if fobj:
        zone = fobj.readlines()
        fobj.close()
    return zone

def zone_file_write (zone, zone_file):
    """
    Write zone file given list of rows.
    """
    okay = False
    if not zone or not zone_file:
        return okay

    fobj = open_file(zone_file,'w')
    if fobj:
        for row in zone:
            fobj.write( row )
        fobj.close()
        okay = True
    return okay

def zone_expand_includes(zone):
    """
     Modify zone by expanding any $INCLUDE files
    """
    if not zone:
        return None

    #
    # Expand $include
    #
    zone_new = []
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

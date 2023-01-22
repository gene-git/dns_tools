# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Take 1 row of a zone file and update serial
 Algorithm assumes any string in form YYYYmmddnn is a serial.
"""
import datetime

def _today ():
    """ today as datetime """
    today = datetime.date.today()
    #today_str = today.strftime("%Y%m%d", today)
    return today

def _bump_serial (dt1, nn, setdate):
    """
     bump serial by 1 - handle format YYYmmddNN
     and when NN hits 99 reser to 0 and bump date by 1 day
     input is dt1 = datetime, and nn = integer (typically 0-99)
     return is updated dt and nn
    """
    done = False
    if setdate:
        # see if date is older than today
        today = _today()
        tdiff = today - dt1
        if tdiff.days > 0:
            done = True
            dt = today
            nn = 0

    if not done:
        if nn == 99:
            nn = 0
            dt = dt1 + datetime.timedelta(days = 1)
        else:
            nn = nn + 1
            dt = dt1
    return (dt, nn)

def _try_split_serial (bump, item, setdate):
    """
    Look for serial in standard form
    """
    # pylint: disable=R1702
    dts = None
    nns = None
    ok = False
    if item :
        length = len(item)
        if length == 10:
            dts = item[0:8]
            nns = item[8:]
            if nns and nns.isnumeric():
                nn = int(nns)
                if 0 <= nn <= 99:
                    try:
                        dt1 = datetime.datetime.strptime(dts, '%Y%m%d')
                        dt1 = dt1.date()
                        if bump:
                            (dt2, nn_new) = _bump_serial(dt1, nn, setdate)
                            dts_new = dt2.strftime('%Y%m%d')
                            nns_new = f'{nn_new:02d}'
                        else:
                            dts_new = dts
                            nns_new = nns
                        ok = True
                    except ValueError:
                        ok = False
    if ok:
        old_serial = dts + nns
        new_serial = dts_new + nns_new
    else:
        new_serial = None
        old_serial = None
    return (ok, old_serial, new_serial)

def zone_bump_serial_row (row, setdate=True):
    """
    for single row of zone file:
    - return row (serial is bumped if there is a serial in row)
    - if setdate and the date component of serial is prior to today - change it to today
      and set count to 01
    """
    new_row = None
    srow = row.split()
    bump = True
    new_row = row
    for item in srow:
        (is_serial, old_serial, new_serial) = _try_split_serial(bump, item, setdate)
        if is_serial :
            new_row = row.replace(old_serial, new_serial)

    return new_row

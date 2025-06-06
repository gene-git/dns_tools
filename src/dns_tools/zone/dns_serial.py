# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Take 1 row of a zone file and update serial
 Algorithm assumes any string in form YYYYmmddnn is a serial.
"""
import datetime
import re


def serial_from_rows(zone_rows: list[str]) -> str:
    """
    find row with SOA
     - handle multiline (parens) and single line (no parens)
     - if multiline append next N rows and look for (serial
     - if single look for serial as 5th number from end

     Returns:
        str:
        The serial number.
    """
    #
    # soa holds the row(s) containing the serial
    # num_rows is number of non comment, non empty rows after SOA for multiline
    # 1 should suffice, we are conservitive
    #
    soa: str = ''
    multiline: bool = False
    count = 1
    num_rows = 10

    for row in zone_rows:
        if not soa:
            if 'SOA' in row:
                soa = row
                if '(' in row:
                    multiline = True
                else:
                    break
        else:
            # skip comment lines and newlines
            row_clean = row.strip()
            if row_clean and not row_clean.startswith(';'):
                soa += row
                count += 1
                if count > num_rows:
                    break

    serial = ''
    if multiline:
        #
        # multiline: ... SOA ... (serial ... )
        #
        pat = r'.*\s+SOA\s+.*\(\s*(?P<serial>[^\n\s;]+)'
        got = re.search(pat, soa)
        if got:
            serial = got.group('serial')
    else:
        #
        # single line: ... SOA ... serial ...
        #
        split_line = soa.split()
        serial = split_line[-5]

    return serial


def canonical_serial() -> str:
    """
    Return canonical serial number.

    Returns:
        (str)
        Serial number: YYYYMMDD01
    """
    today = datetime.date.today()
    today_str = today.strftime("%Y%m%d")
    serial = f'{today_str}01'
    return serial


def split_std_serial(serial: str) -> tuple[bool, datetime.date | None, int]:
    """
    Given serial in form YYYMMDDnn (8-10 digits)
       where: nn can be empty, 1 digit or 2 digits
       return: (is_std, date, nn )
    """
    is_std = False
    len_serial = len(serial)
    if len_serial < 8:
        return (False, None, 0)

    dts = serial[0:8]
    nnn = 0
    if len_serial > 8:
        nnns = serial[8:]
        nnn = int(nnns)

    try:
        dt = datetime.datetime.strptime(dts, '%Y%m%d')
        dt1 = dt.date()
        is_std = True

    except ValueError:
        dt1 = None

    return (is_std, dt1, nnn)


def _increment_serial(dt1: datetime.date, nnn: int, setdate: bool
                      ) -> tuple[datetime.date, int]:
    """
    Given date and number split from canonical serial
    increment number by 1
    if setdate and date before today
        use today's date and nn = 00
    else:
        increment nn unless nnn == 99 then increment date by 1 day
        and set nn = 00
    """
    # pylint: disable=possibly-used-before-assignment
    done = False
    if setdate:
        today = datetime.date.today()
        tdiff = today - dt1
        if tdiff.days > 0:
            done = True
            dt_new = today
            nnn_new = 0

    if not done:
        if nnn == 99:
            nnn_new = 0
            dt_new = dt1 + datetime.timedelta(days=1)
        else:
            nnn_new = nnn + 1
            dt_new = dt1
    return (dt_new, nnn_new)


def make_new_serial(serial: str, setdate: bool = True) -> str:
    """
    Increment canonical dns serial.
    If setdate True and date is prior to today then use
    today for date part.
    if serial non-standard, do best we can to use it.
    A serial is invalid if: (not numbers, or more than 10 digits)
    """
    if not serial:
        return ''

    #
    # Must be numbers only
    #
    serial_new = ''
    if serial.isnumeric():
        serial_number = int(serial)
        serial_len = len(serial)
        if serial_len == 10:
            #
            # get and split standard format
            #
            (is_std, dt1, nnn) = split_std_serial(serial)
            if is_std and dt1 is not None:
                (dt_new, nnn_new) = _increment_serial(dt1, nnn, setdate)
                dts_new = dt_new.strftime('%Y%m%d')
                nns_new = f'{nnn_new:02d}'
                serial_new = f'{dts_new}{nns_new}'

                # Check for future date
                today = datetime.date.today()
                tdiff = dt_new - today
                if tdiff.days > 0:
                    print(f'Warning serial date {dts_new} is in future')

            else:
                print(f'Warning Non standard serial {serial}.')
                print(' Attempting repair => YYYMMDDnn')
                serial_new = canonical_serial()
                new_num = int(serial_new)
                if new_num < serial_number:
                    # needs to be larger than old
                    print('Serial starts with year that is too large')
                    print('  Unable to make standard format.')
                    print('  Will simply increment')
                    serial_new = str(serial_number + 1)
        else:
            if serial_len > 10 or serial_number >= 4294967295:
                print('Error: Illegel serial too large')
                print(' Forcing into canonical YYYMMDDnn format')
                serial_new = canonical_serial()
            else:
                print('Warning: serial too short')
                print(' changing to canonical YYYMMDDnn format')
                serial_new = canonical_serial()
    else:
        # Invalid format
        print(f'Error: Invalid serial {serial}.')
        print('  Must be numbers only (10)')
        print('  Forcing into canonical YYYMMDDnn format')
        serial_new = canonical_serial()

    return serial_new


def zone_get_new_serial(zone_rows: list[str], setdate: bool = True
                        ) -> tuple[str, str]:
    """
    Given list of rows of the zonefile
    Identify the serial and return old and new serial
    """
    new_serial = ''
    serial = serial_from_rows(zone_rows)
    if serial:
        new_serial = make_new_serial(serial, setdate=setdate)
    return (serial, new_serial)


def zone_update_serial(zone: list[str], setdate: bool = True
                       ) -> list[str]:
    """
    Given list of zonefile rows
    Find and update serial and return updated zone_rows
    """
    (serial, new_serial) = zone_get_new_serial(zone, setdate=setdate)
    zone_updated = update_serial_to_new(zone, serial, new_serial)
    return zone_updated


def update_serial_to_new(zone_rows: list[str], serial: str,
                         new_serial: str) -> list[str]:
    """
    Given list of zonefile rows
     - Find and increment serial number
     - return updated rows.
       Ensure we update the actual serial so
        - ignore comment rows or anything after a comment
        - trigger on SOA - then replace once
    """
    soa_found = False
    serial_updated = False
    zone_updated: list[str] = []

    for row in zone_rows:
        if serial_updated or row.startswith(';'):
            zone_updated.append(row)
            continue

        row_split = row.split(';', 1)
        text = row_split[0]

        if not soa_found:
            if 'soa' in text or 'SOA' in text:
                soa_found = True

        if soa_found:
            if serial in text:
                serial_updated = True
                new_text = row.replace(serial, new_serial)
                zone_updated.append(new_text)
            else:
                zone_updated.append(row)
        else:
            zone_updated.append(row)

    return zone_updated

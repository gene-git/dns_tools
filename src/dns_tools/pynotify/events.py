# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Wrap libc inotify 
 see man inotify et al for details
"""
# pylint: disable=invalid-name
import os
from dataclasses import dataclass,field
from select import select
import struct
from .class_mask import InotifyMask

#
# Inotify event C-struct
# {int wd, uint32 mask, uint32 cookie, uint32 len_name, char name[] }
#
#
@dataclass
class InotifyEvent:
    """
    one inotify event
    """
    wd : int = -1
    mask : int = -1
    event_types : list[str] = field(default_factory=list)
    path : str = ''
    file : str = ''

def mask_to_event_types(mask:int):
    """
    From mask => return list of event types
    """
    event_types = InotifyMask.mask_to_events(mask)
    return event_types

def _read_inotify_events(inotify):
    """
    read one or more event(s) up to max number of events
    If more than that max, we are called from select loop
    so will be called to process more if any left to read.
    Event "name" field is filename with max len = NAME_MAX (255)
    So, to read 1 event need at most :
        max_event_size = hdr + NAME_MAX +1 (for null terminator)
    Idea is we keep a buffer of whatever we have read and process
    All events - if buffer has leftover but not enough for an event, it
    means there's more to read - let select loop call us again to read more.
    """
    # pylint: disable=too-many-locals

    buf = inotify.buf
    fd = inotify.fd

    # ignoring the name part:
    hdr_fmt = 'iIII'
    hdr_size = struct.calcsize(hdr_fmt)

    # size depends on filenames in event so cannot be exact
    # allow up to some number and handle any partial buffer
    event_size_max = hdr_size + 256
    max_to_read = 50
    events_size = max_to_read * event_size_max

    events = []
    try:
        chunk = os.read(fd, events_size)
    except OSError:
        return events

    buf += chunk
    #
    # Make list of all events found in buf
    #
    while True:
        #
        # Check have enough for 1 event
        #
        len_buf = len(buf)
        if len_buf < hdr_size:
            inotify.buf = buf
            return events

        #
        # determine any filename size from header
        #
        header = struct.unpack(hdr_fmt, buf[:hdr_size])
        [wd, mask, _cookie, len_name] = header

        len_event = hdr_size + len_name
        if len_buf < len_event:
            # partial - wait till next time
            inotify.buf = buf
            return events

        #
        # Process an event
        #
        file = buf[hdr_size:len_event]

        event = InotifyEvent()
        event.wd = wd
        event.path = inotify.watch_path[wd]
        event.mask = mask
        #
        # c strings are null terminated
        #
        file = file.rstrip(b'\0')
        if file:
            event.file = file.decode()

        event.event_types = mask_to_event_types(mask)
        events.append(event)

        #
        # Remove processed event from buffer and
        # save whatever remains.
        #
        if len_buf > len_event:
            inotify.buf = buf[len_event:]
        else:
            inotify.buf = b''

        buf = inotify.buf
    return events

def get_inotify_events(inotify):
    """
    wait for events
     = provide iterater until fd is closed
     - fd is closed when the inotify event says so.
     - if timeout < 0, wait forever
    """
    if len(inotify.watch_wd) == 0:
        return []

    timeout = inotify.timeout
    done = False
    while not done:
        if len(inotify.watch_path) == 0:
            done = True
            break
        try:
            if timeout >= 0:
                (fds, _fwr, _ferr) = select([inotify.fd], [], [], timeout)
            else:
                (fds, _fwr, _ferr) = select([inotify.fd], [], [])
        except (IOError, KeyboardInterrupt):
            inotify.rm_all_watches()
            done = True
            break

        # process event(s)
        if not fds:
            return []

        events = _read_inotify_events(inotify)

        #
        # check if watched path deleted
        #
        for event in events:
            if InotifyMask.IN_DELETE_SELF & event.mask and event.path in inotify.watch_wd:
                inotify.rm_watch(event.path)
        yield events
    return []

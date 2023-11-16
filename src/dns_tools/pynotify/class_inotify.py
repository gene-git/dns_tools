# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Wrap libc inotify 
 see man inotify et al for details
"""
# pylint: disable=invalid-name
import os
#from dataclasses import dataclass,field
import ctypes
import ctypes.util
import errno
from .class_mask import InotifyMask
from .events import get_inotify_events

def _load_libc():
    """
    Load the standard c-library
    """
    libc_so = ctypes.util.find_library("c")
    if not libc_so:
        libc_so = 'libc.so.6'
    libc = ctypes.cdll.LoadLibrary(libc_so)
    return libc

class Inotify:
    """
    Python inotify class 
     - uses standard C-lib inotify
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.libc = _load_libc()
        # timeout in secs: 0 => returns immediately (polls), -1 waits forever
        self.timeout = 5

        # fd is handle to this inotify instance
        self.fd = -1
        self.buf = b''

        # Keep track of each watched item by (wd, path)
        self.watch_path = {}
        self.watch_wd = {}

        # Can save one errno via self.save_errno()
        self.errno_code = 0
        self.errno_str = ''

        #
        # Wrap the inotify functions:
        #  - Each (fd, path, mask) -> wd aka a watch descriptor
        #
        self.inotify_add_watch = self.libc.inotify_add_watch
        self.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]

        # fd, wd -> 0 (or -1 for error)
        self.inotify_rm_watch = self.libc.inotify_rm_watch
        self.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]

        #
        # init this inotify instance
        #
        self.fd = self.libc.inotify_init()

    def add_watch(self, path, mask=InotifyMask.IN_ALL_EVENTS):
        """
        add watch on path
         - mask is a bit mask from sys/inotify.h (see hand created inotify_h file)
         - Or together whatever items to watch (m1 | m2 ... )
         - can only inotify file that exists
        """
        #if not os.path.exists(path):
        #    return

        #
        # Speak bytes to C-code
        # - we dont seem to need to null terminate
        # - wd < 0 if file doesn't exist (see errno)
        #
        path_bytes = path.encode()
        wd = self.inotify_add_watch(self.fd, path_bytes, mask)

        #
        # A watch on non-existent path will never do anything - skip it
        #
        if wd >= 0:
            self.watch_wd[path] = wd
            self.watch_path[wd] = path
        else:
            self.save_errno()

    def save_errno(self):
        """ keep the last errno """
        err = ctypes.get_errno()
        self.errno_code = errno.errorcode.get(err)
        self.errno_str = os.strerror(err)

    def rm_watch(self, path):
        """ add watch on path """

        wd = self.watch_wd.get(path)
        if not wd:
            return

        del self.watch_path[wd]
        del self.watch_wd[path]

        self.inotify_rm_watch(self.fd, wd)

    def rm_all_watches(self):
        """
        flush all of them:
        """
        for (wd, _path) in  self.watch_path.items():
            self.inotify_rm_watch(self.fd, wd)
        self.watch_path = {}
        self.watch_wd = {}

    def get_events(self):
        """
        wait for events
         = provide iterater until fd is closed
         - fd is closed when the inotify event says so.
         - if timeout < 0, wait forever
        """
        return get_inotify_events(self)

# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
toml support
 - toml reader is native to 3.11+
"""
import os
import sys
from .tools import open_file

if sys.version_info >= (3,11):
    # 3.11 has tomllib
    try:
        import tomllib as toml
    except ImportError:
        pass
else:
    import tomli as toml

def read_toml_file(fpath):
    """
    read toml file and return a dictionary
    """
    this_dict = None
    if os.path.exists(fpath):
        fobj = open_file(fpath, 'r')
        if fobj:
            data = fobj.read()
            fobj.close()
            this_dict = toml.loads(data)
    return this_dict

#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Tool to push into production
  - work staging to production staging
  - production staging to live production
 gc - 2022
"""
#import pdb
from lib import DnsProd

def main():
    """
    - work staging to production staging
    - production staging to live production
    """
    #pdb.set_trace()
    prod = DnsProd()
    if not prod.okay:
        return

    if prod.opts.to_production:
        prod.to_production()

    if prod.opts.dns_restart:
        prod.dns_restart()

if __name__ == '__main__':
    main()

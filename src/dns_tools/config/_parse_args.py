# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
 Each operation has own command line arguments.

 Keep all options here so they are all in one place and
 makes it easier to avoid any conflicts.
"""
from typing import (Any)
import argparse

type Opt = tuple[str | tuple[str, str], dict[str, Any]]


def parse_args(desc: str, avail_options: list[Opt]) -> dict[str, Any]:
    """
    Run argparse parse_args on list of options.

    Args:
        desc (str):
        Description for options.

        avail_opts (list[Opt]):
        list of available command line options.

    Returns:
        dict[key: str, value: Any]:
        The result of parse_args on the options.
    """
    #
    # Install available options into parser
    #
    par = argparse.ArgumentParser(description=desc)

    for opt in avail_options:
        opt_list, kwargs = opt
        if isinstance(opt_list, str):
            par.add_argument(opt_list, **kwargs)
        else:
            par.add_argument(*opt_list, **kwargs)

    #
    # Parse and return dictionary
    #
    parsed_dict: dict[str, Any] = {}
    parsed = par.parse_args()
    if parsed:
        parsed_dict = vars(parsed)
    return parsed_dict

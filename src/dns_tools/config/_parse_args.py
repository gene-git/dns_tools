# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Each operation has own command line arguments.

 Keep all options here so they are all in one place and
 makes it easier to avoid any conflicts.
"""
from typing import (Any, List, Dict, Tuple)
import argparse

type Opt = Tuple[str | Tuple[str, str], Dict[str, Any]]


def parse_args(desc: str, avail_options: List[Opt]) -> Dict[str, Any]:
    """
    Run argparse parse_args on list of options.

    Args:
        desc (str):
        Description for options.

        avail_opts (List[Opt]):
        List of available command line options.

    Returns:
        Dict[key: str, value: Any]:
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
    parsed_dict: Dict[str, Any] = {}
    parsed = par.parse_args()
    if parsed:
        parsed_dict = vars(parsed)
    return parsed_dict

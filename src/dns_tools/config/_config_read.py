# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Read options from config file.

"""
from typing import (Any)
import os
from utils import read_toml_file


def read_config() -> dict[str, Any]:
    """
    Read config settings.

    Config is a toml file found by searching a directory path
    for the first found:

    - conf.d/config
    - /etc/dns_tools/config

    Config "can" be any legal toml. In practice it is limited to:

    - dict[str, X]
    - x : str, List[str], dict[str, dict[str, str]]

    """
    config: dict[str, Any] = {}
    conf_file = 'conf.d/config'
    confs = [f'./{conf_file}', f'/etc/dns_tools/{conf_file}']

    for conf in confs:
        if os.path.exists(conf) and os.access(conf, os.R_OK):
            print(f'Config file : {conf}')
            this_conf = read_toml_file(conf)
            config = this_conf
            break

    return config

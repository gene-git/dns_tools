# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Always use normalized / absoulte paths
"""
from utils import normalize_one_path

from ._config import Config


def normalize_paths(conf: Config):
    """
    Normalize paths.

     Call after both:
        - command line options handled
        - config options are checked

     - relative paths are relative to work_dir
     - make all paths absolute

    """
    conf.work_dir = normalize_one_path(None, conf.work_dir)

    conf.key_dir = normalize_one_path(conf.work_dir, conf.key_dir)

    if conf.internal:
        conf.internal.normalize_paths(conf.work_dir)

    if conf.external:
        conf.external.normalize_paths(conf.work_dir)

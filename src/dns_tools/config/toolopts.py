# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Initialize options for dns-tool.

Config file + command line options.
"""
# pylint: disable=duplicate-code
from typing import (List, Tuple)

from ._toolopts_base import ToolOptsBase
from ._config_checks import (config_warnings_errors)
from ._normalize_paths import normalize_paths


class ToolOpts(ToolOptsBase):
    """
    Sub class with methods.
    """
    def __init__(self):
        super().__init__()
        self.normalize_paths()

    def config_warnings_errors(self) -> Tuple[List[str], List[str]]:
        """
        Check for valid inputs
        """
        return config_warnings_errors(self)

    def normalize_paths(self):
        """
        Call after all command line options
        and after passing all checks
        """
        normalize_paths(self)

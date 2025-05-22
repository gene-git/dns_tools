# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-prod
"""
# pylint: disable=duplicate-code

from ._prodopts_base import ProdOptsBase
from ._config_checks import (config_warnings_errors)
from ._normalize_paths import normalize_paths


class ProdOpts(ProdOptsBase):
    """
    Sub class provides methods.
    """
    def __init__(self):
        super().__init__()
        self.normalize_paths()

    def config_warnings_errors(self) -> tuple[list[str], list[str]]:
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

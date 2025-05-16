# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-prod
"""
# pylint: disable=duplicate-code, too-few-public-methods
from config import ProdOpts


class DnsProdBase:
    """
    Production base class.

    Takes care of pushing to production.
    Actions/methods are in DnsProd subclass
    """
    def __init__(self):

        self.opts = ProdOpts()
        self.okay = self.opts.okay

        #
        # warnings inform
        # errors are fatal
        #
        self.warnings_errors()

    def warnings_errors(self):
        """
        Check for input errors
        """
        msg = self.opts.prnt.msg
        (warnings, errors) = self.opts.config_warnings_errors()

        if warnings and len(warnings) > 0:
            msg('Warnings:\n', fg='warn')
            msg(warnings)

        if errors and len(errors) > 0:
            self.okay = False
            msg('Errors:\n', fg='error')
            msg(errors)

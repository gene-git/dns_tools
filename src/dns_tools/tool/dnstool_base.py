# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
DNS tool base class
"""
# pylint: disable=duplicate-code, too-few-public-methods
from typing import (Dict)
from config import ToolOpts

from keys import DnsKeys


class DnsToolBase:
    """
    Tool base class.

    Actions/methods are in DnsTool subclass
    """
    def __init__(self):

        self.opts = ToolOpts()
        self.okay = self.opts.okay

        #
        # warnings inform
        # errors are fatal
        #
        self.warnings_errors()

        #
        # if sign - get keys for each domain
        # keys maps(domain) to DnsKeys
        #
        self.keys: Dict[str, DnsKeys] = {}
        opts = self.opts
        if opts.domains:
            for dom in opts.domains:
                self.keys[dom] = DnsKeys(dom, opts.key_dir)

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

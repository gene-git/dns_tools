# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Error and Warning checks
"""
from typing import (List, Tuple)

from utils import get_my_hostname

from ._config import Config
from ._config_utils import (directory_check, str_variable_check)


def config_warnings(conf: Config) -> List[str]:
    """
    Returns list of warnings (or none)

    Args:
        conf (Config):

    Returns:
        List[warnings: str]
        Possibly empty list of warnings
    """
    warnings: List[str] = []

    if conf.euid != 0:
        warnings.append('Not running as root\n')

    #
    # All done
    #
    return warnings


def config_warnings_errors(conf: Config) -> Tuple[List[str], List[str]]:
    """
    Returns list of errors and warnings.

    Args:
        conf (Config):

    Returns:
        Tuple[List[warnings: str], List[errors: str]):
        Possibly empty lists of warnings and errors.
    """
    errors: List[str] = []
    warnings: List[str] = config_warnings(conf)

    #
    # Directories
    #
    (okay, error) = directory_check(conf.work_dir)
    if not okay:
        errors.append('work_dir: ' + error + '\n')

    (okay, error) = directory_check(conf.key_dir)
    if not okay:
        errors.append('key_dir: ' + error + '\n')

    (okay, error) = directory_check(conf.production_zone_dir)
    if not okay:
        errors.append('production_zone_dir: ' + error + '\n')

    #
    # Signing server
    #
    (okay, error) = _check_sign_server(conf.sign_server)
    if not okay:
        errors.append(error)

    #
    # DNS servers must have one
    #
    has_dns_server = False
    if conf.external and conf.external.staging_zone_dir:
        has_dns_server = True
        (okay, error) = conf.external.check()
        if not okay:
            warnings.append('dns.external: ' + error + '\n')
    # else:
    #     errors.append('dns.external missing' + '\n')

    if conf.internal and conf.internal.staging_zone_dir:
        has_dns_server = True
        (okay, error) = conf.internal.check()
        if not okay:
            warnings.append('dns.internal: ' + error + '\n')

    if not has_dns_server:
        errors.append('dns server(s): need external, internal or both.')

    #
    # Key algo checks
    #
    (okay, error) = conf.key_opts.check()
    if not okay:
        errors.append(error)

    #
    # All done
    #
    return (warnings, errors)


def _check_sign_server(sign_server: str) -> Tuple[bool, str]:
    """
    Check we're running on the signing server
    """

    #
    # check sign_server is set
    #
    (okay, error) = str_variable_check(sign_server)
    if not okay:
        return (False, 'sign_server: ' + error + '\n')

    #
    # Now make sure we are running on it
    #
    (host, fqdn) = get_my_hostname()
    if sign_server in (host, fqdn):
        return (True, '')

    error = 'Must run on signing server {sign_server}'
    error += ' not {fqdn}'
    return (False, error + '\n')

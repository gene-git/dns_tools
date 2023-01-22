# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
tools to help push things to production
"""
from .run_prog import run_prog

def restart_one_dns_server(dns_host, dns_restart_cmd, test, verb):
    """
    Restart nsd
     - dns_host not set -> on current machine
     - dns_host set - use ssh to start on dns_host
    """
    okay = True
    pargs = dns_restart_cmd.split()
    if dns_host:
        pargs = ['/usr/bin/ssh', '-T', dns_host] + pargs

    [retc, _output, errors] = run_prog(pargs, test=test, verb=verb)
    if retc != 0:
        okay = False
        print(f'  ** Failed to run {pargs}')
        if errors:
            print(errors)
    return okay

def restart_dns_servers(prod):
    """
    Restart the internal and external dns servers
    """
    okay = True
    opts = prod.opts
    test = opts.test
    verb = opts.verb

    dns_restart_cmd = prod.opts.dns_restart_cmd
    if not dns_restart_cmd:
        print('Error - missing dns_restart_cmd')
        return False

    # internal
    dns_server = opts.internal.dns_server
    dns_host = dns_server
    if dns_server == opts.sign_server:
        dns_host = opts.sign_server
        dns_server = None

    print(f'Restarting dns server on {dns_host}')
    oki = restart_one_dns_server(dns_server, dns_restart_cmd, test, verb)
    okay &= oki

    # external
    dns_server = opts.external.dns_server
    dns_host = dns_server
    if dns_server == opts.sign_server:
        dns_host = opts.sign_server
        dns_server = None

    print(f'Restarting dns server on {dns_host}')
    oki = restart_one_dns_server(dns_server, dns_restart_cmd, test, verb)
    okay &= oki

    return okay

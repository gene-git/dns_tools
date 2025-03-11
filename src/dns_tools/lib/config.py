# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Read options from config files:
    1) ./conf.d/config
    2) /etc/dns_tools/conf.d/config
"""
import os
from .toml import read_toml_file
from .tools import get_my_hostname

def read_config():
    """
    Read config settings
    """
    config = None
    conf_file = 'conf.d/config'
    confs = [f'./{conf_file}', f'/etc/dns_tools/{conf_file}']

    for conf in confs:
        if os.path.exists(conf) and os.access(conf, os.R_OK):
            print(f'Config file : {conf}')
            this_conf = read_toml_file(conf)
            config = this_conf
            break

    return config

def load_config_into_opts(opts):
    """
    Read config and save at option attributes
    """
    conf = read_config()
    if conf:
        for (key,val) in conf.items():
            if key == 'internal':
                for (skey, sval) in val.items():
                    setattr(opts.internal, skey, sval)
            elif key == 'external':
                for (skey, sval) in val.items():
                    setattr(opts.external, skey, sval)
            else:
                setattr(opts, key, val)

def _dir_check(prnt, what, adir, local):
    """ check dir """
    okay = True

    if not adir:
        okay = False
        prnt.msg(f'Missing {what}\n', fg_col='error')

    elif local and not (os.path.exists(adir) and os.path.isdir(adir)):
        okay = False
        prnt.msg(f'Invalid {what} : {adir}\n', fg_col='error')

    return okay

def _variable_check(prnt, what, host):
    """ variable string check - just make sure exists """

    okay = True
    if not host:
        okay = False
        prnt.msg(f'Missing {what}\n', fg_col='error')
    return okay

def _int_ext_check(prnt, what, int_ext):
    """
    check internal / external
     external is required but not internal
    """
    okay = True
    if not int_ext :
        okay = False
        prnt.msg(f'Missing {what} info\n', fg_col='error')
        return okay

    if not int_ext.dns_server:
        okay = False
        prnt.msg(f'Missing {what}.dns_server\n', fg_col='error')

    if not int_ext.staging_zone_dir:
        okay = False
        prnt.msg(f'Missing {what}.staging_zone_dir\n', fg_col='error')

    return okay


def _validate_on_sign_server(prnt, sign_server):
    """
    Tool must be run on signing server.
    We require config contain a signing server for self protection.
    Checks current host is the signing server
    """
    (host, fqdn) = get_my_hostname()
    if sign_server in (host, fqdn) :
        okay = True
    else:
        prnt.msg(f'Error : must run on signing server {sign_server} not {fqdn}\n',
                 fg_col='error')
        okay = False
    return okay


def _key_algo_check(prnt, algo):
    '''
    Check input algo is one we support
    '''
    if not algo:
        return False

    algos = ['ECDSAP256SHA256', 'ECDSAP384SHA384', 'ED25519', 'ED448']
    if algo.upper() not in algos:
        prnt.msg(f'Error : Unsupported key algorithm {algo}')
        prnt.msg(f'      : Must be one of {algos}')
        return False
    return True

def config_check(prnt, opts):
    """
    Check that required options have values
    opts : DnsOpts
    """
    okay = True
    #
    # Checks for both dns-tool and dns-prod
    #

    # global dirs
    oki = _dir_check(prnt, 'work_dir', opts.work_dir, True)
    okay &= oki

    oki = _dir_check(prnt, 'key_dir', opts.key_dir, True)
    okay &= oki

    oki = _dir_check(prnt, 'production_zone_dir', opts.production_zone_dir, False)
    okay &= oki

    oki = _variable_check(prnt, 'sign_server', opts.sign_server)
    okay &= oki

    oki = _variable_check(prnt, 'dns_restart_cmd', opts.dns_restart_cmd)
    okay &= oki

    # external
    oki = _int_ext_check(prnt, 'external', opts.external)
    okay &= oki

    # internal - can be missing but if present must provide work_dir/server
    if opts.internal:
        oki = _int_ext_check(prnt, 'internal', opts.internal)
        okay &= oki

    if not opts.domains and not opts.print_keys:
        prnt.msg('Warning no domains provided\n', fg_col='warn')
        okay = False

    # check running on signing server
    oki = _validate_on_sign_server(prnt, opts.sign_server)
    okay &= oki

    # Check both ksk and zsk have supported key algorithm
    oki = _key_algo_check(prnt, opts.ksk_opts.algo)
    okay &= oki

    oki = _key_algo_check(prnt, opts.zsk_opts.algo)
    okay &= oki

    # warn if not root
    if opts.euid != 0:
        prnt.msg('Warning: not running as root\n', fg_col='warn')

    if not okay:
        prnt.msg('Error in input\n', fg_col='error')
    return okay

def config_paths_normalize(opts):
    """
    Handle normalizeing paths
     - relative paths are relative to work_dir
    """

    opts.work_dir = os.path.normpath(opts.work_dir)
    opts.work_dir = os.path.abspath(opts.work_dir)

    if not os.path.isabs(opts.key_dir):
        opts.key_dir = os.path.join(opts.work_dir, opts.key_dir)
    opts.key_dir = os.path.normpath(opts.key_dir)
    opts.key_dir = os.path.abspath(opts.key_dir)

    if opts.internal:
        opts.internal.set_abs_paths(opts.work_dir)
        if not opts.internal.check_staging():
            print('Error - invalid internal staging dir')
            opts.okay = False

    if opts.external:
        opts.external.set_abs_paths(opts.work_dir)
        if not opts.external.check_staging():
            print('Error - invalid external staging dir')
            opts.okay = False

def prod_opts_check(prnt, opts):
    """
    Check that required options have values
    opts : ProdOpts
    """
    okay = True

    # global dirs
    oki = _dir_check(prnt, 'work_dir', opts.work_dir, True)
    okay &= oki

    oki = _dir_check(prnt, 'key_dir', opts.key_dir, True)
    okay &= oki

    oki = _dir_check(prnt, 'production_zone_dir', opts.production_zone_dir, False)
    okay &= oki

    oki = _variable_check(prnt, 'sign_server', opts.sign_server)
    okay &= oki

    #oki = _variable_check(prnt, 'dns_restart_cmd', opts.dns_restart_cmd)
    #okay &= oki

    # external
    oki = _int_ext_check(prnt, 'external', opts.external)
    okay &= oki

    # internal - can be missing but if present must provide work_dir/server
    if opts.internal:
        oki = _int_ext_check(prnt, 'internal', opts.internal)
        okay &= oki

    # check running on signing server
    oki = _validate_on_sign_server(prnt, opts.sign_server)
    okay &= oki

    # warn if not root
    if opts.euid != 0:
        prnt.msg('Warning: not running as root\n', fg_col='warn')

    if not okay:
        prnt.msg('Error in input\n', fg_col='error')
    return okay

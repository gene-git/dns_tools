# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
tools to push things to production
"""
from .tools import rsync_copy
from .tools import rel_from_abs_path

def staging_zones_to_production(prod):
    """
    Copy zone files
     - from work_dir staging to production
    """
    okay = True
    opts = prod.opts
    prnt = prod.prnt
    test = opts.test
    verb = opts.verb
    work_dir = opts.work_dir

    #
    # double check owner/perms
    #
    prod.zone_perms()
    rsync_opts = ['--owner']
    if prod.opts.euid != 0:
        rsync_opts = []
        prnt.msg('Warning: Must be root to use rsync --owner option\n', fg_col='warn')

    rsync_opts += ['-a', '--mkpath']
    if opts.verb:
        rsync_opts += ['-v']

    #
    # common to internal/external
    #
    work_host = None
    prod_dir = opts.production_zone_dir
    if prod_dir[-1] == '/':
        prod_dir[-1] = ''

    # ----------------------------------------------
    # internal
    #  - work staging_zone_dir -> production_zone_dir
    #
    # if signing server (where work_dir / staging zones) same as internal server
    # copy is local. otherwise remote
    #
    if opts.int_zones:
        work_stage = opts.internal.staging_zone_dir
        if work_stage[-1] != '/':
            work_stage += '/'
        work_stage_rel = rel_from_abs_path(work_stage, work_dir)

        prod_host = None
        prod_host_str = ''
        if opts.sign_server != opts.internal.dns_server:
            prod_host = opts.internal.dns_server
            prod_host_str = f'{prod_host}:'

        print(f'Pushing {work_stage_rel} to {prod_host_str}{prod_dir}')
        oki = rsync_copy(work_host, work_stage, rsync_opts, prod_host, prod_dir, test, verb)
        okay &= oki

    # ----------------------------------------------
    # external
    #  - work stage -> prod stage
    #
    if opts.ext_zones:
        work_host = None
        work_stage = opts.external.staging_zone_dir
        if work_stage[-1] != '/':
            work_stage += '/'
        work_stage_rel = rel_from_abs_path(work_stage, work_dir)

        prod_host = None
        prod_host_str = ''
        if opts.sign_server != opts.external.dns_server:
            prod_host = opts.external.dns_server
            prod_host_str = f'{prod_host}:'

        print(f'Pushing {work_stage_rel} to {prod_host_str}{prod_dir}')
        oki = rsync_copy(work_host, work_stage, rsync_opts, prod_host, prod_dir, test, verb)
        okay &= oki

    return okay

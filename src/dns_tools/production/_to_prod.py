# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
tools to push things to production
"""
# pylint: disable=too-many-locals
from utils import rsync_copy
from utils import rel_from_abs_path


def staging_zones_to_production(prod):
    """
    Copy zone files
     - from work_dir staging to production
    """
    okay = True
    opts = prod.opts
    test = opts.test
    verb = opts.verb
    work_dir = opts.work_dir
    msg = opts.prnt.msg

    #
    # double check owner/perms
    #
    prod.zone_perms()
    rsync_opts = ['--owner']
    if prod.opts.euid != 0:
        rsync_opts = []
        text = 'Warning: Must be root to use rsync --owner\n'
        msg(text, fg='warn')

    rsync_opts += ['-a', '--mkpath']
    if opts.verb:
        rsync_opts += ['-v']

    #
    # common to internal/external
    #
    work_host = ''
    prod_dir = opts.production_zone_dir
    if prod_dir[-1] == '/':
        prod_dir[-1] = ''

    # ----------------------------------------------
    # internal
    #  - work staging_zone_dir -> production_zone_dir
    #
    # signing server is where work_dir / staging zones reside.
    # if sign_server == internal server
    # copy is local. otherwise remote
    #
    if opts.int_zones:
        work_stage = opts.internal.staging_zone_dir
        if work_stage[-1] != '/':
            work_stage += '/'
        work_stage_rel = rel_from_abs_path(work_stage, work_dir)

        prod_host = ''
        if opts.sign_server != opts.internal.dns_server:
            prod_host = opts.internal.dns_server

        msg(f'Pushing {work_stage_rel} to {prod_host}{prod_dir}\n')
        oki = rsync_copy(work_host, work_stage, rsync_opts,
                         prod_host, prod_dir, test, verb)
        okay &= oki

    # ----------------------------------------------
    # external
    #  - work stage -> prod stage
    #
    if opts.ext_zones:
        work_host = ''
        work_stage = opts.external.staging_zone_dir
        if work_stage[-1] != '/':
            work_stage += '/'
        work_stage_rel = rel_from_abs_path(work_stage, work_dir)

        prod_host = ''
        if opts.sign_server != opts.external.dns_server:
            prod_host = opts.external.dns_server

        print(f'Pushing {work_stage_rel} to {prod_host}{prod_dir}')
        oki = rsync_copy(work_host, work_stage, rsync_opts,
                         prod_host, prod_dir, test, verb)
        okay &= oki

    return okay

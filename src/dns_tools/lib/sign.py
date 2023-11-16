# SPDX-License-Identifier: MIT
# Copyright (c) 2023, Gene C
"""
 Sign zone file

 signed zone file is stored in signed/data/domain-basename-datetime
 and a link is placed in signed/domain.signed -> actual file.
 datetime is 1 sec accuracy to permit multiple signs per day if needed - perhaps 1 min is ok
"""
# pylint: disable=invalid-name, too-many-arguments
import os
import datetime
import re

from .run_prog import run_prog
from .tools import make_dir_if_needed
from .tools import make_symlink

def _expire_to_dt_string(expire_in):
    """
    Map input expire in form '90d' into formatted datetime string
    """
    expiry = None

    if not expire_in:
        expire_in = '90d'

    units = re.sub(r'[\-\d+-]*', '', expire_in)
    delta = expire_in.replace(units,'')
    delta = int(delta)

    now = datetime.datetime.now()
    if units.startswith('d'):
        dt = now + datetime.timedelta (days = delta)

    elif units.startswith('m'):
        dt = now + datetime.timedelta (months = delta)

    elif units.startswith('y'):
        dt = now + datetime.timedelta (years = delta)

    elif units.startswith('h'):
        dt = now + datetime.timedelta (hours = delta)

    elif units.startswith('w'):
        dt = now + datetime.timedelta (days = 7*delta)

    elif units.startswith('M'):
        dt = now + datetime.timedelta (days = 30*delta)

    expiry = dt.strftime('%Y%m%d%H%M%S')

    return expiry

#
# etc_nsd/
#       zones/
#           same structure as staging/zones
#
#       staging/zones/
#           domain          # zone file
#           domain.signed/
#               link_name -> data/<date-time>
#               data/
#                   <date-time>             # prepend KSKs and ZSKs - or use DS DNSKEY
#
def _signed_path(tool, staging, domain, link_file):
    """
    Add link zone -> data/<date-time> and return
    path to data/<date-time> so can be written
    Would be better to write file before making the link
    """
    start_dir = os.getcwd()

    dom_signed_dir = f'{domain}.signed'
    link_dir = os.path.join(staging, dom_signed_dir)
    signed_dir = os.path.join(link_dir, 'data')
    if not tool.opts.test:
        make_dir_if_needed(signed_dir)

    dt_string = tool.opts.now

    signed_file = dt_string
    signed_file_rel = os.path.join('data', signed_file)
    signed_path = os.path.join(signed_dir, signed_file)

    #
    # Do symlink here
    #
    os.chdir(link_dir)
    if not tool.opts.test:
        make_symlink(signed_file_rel, link_file)
    os.chdir(start_dir)

    signed_path = os.path.normpath(signed_path)
    signed_path = os.path.abspath(signed_path)

    return signed_path

def _base_name_to_hash_vers (base_name):
    """
     Given basename of form:  K<domain>.+<type>+<id>.extension
     extract +<type>+<id>

     base_name.key is a link - what link points to is xxx/K<dom>.+nnn+mmm.key
     So we look up what link points to and take base name of that to derive
     the Ids we want.
    """
    link = f'{base_name}.key'
    path = os.readlink(link)
    file = os.path.basename(path)
    word = file.split('+')
    type_id = f'+{word[1]}+{word[2]}'
    type_id = type_id.split('.')[0]     # remove .key
    return type_id


def get_signing_key_base_names(tool, domain):
    """
    Retrieve list of keys to be used to sign this domain
    """
    dom_keys = tool.keys[domain]
    ksk_key = dom_keys.ksk
    zsk_key = dom_keys.zsk

    ksk_keys = []
    zsk_keys = []

    if tool.opts.ksk_opts.sign_curr:
        ksk_keys.append(ksk_key.curr.key_base)

    if tool.opts.ksk_opts.sign_next:
        ksk_keys.append(ksk_key.next.key_base)

    if tool.opts.zsk_opts.sign_curr:
        zsk_keys.append(zsk_key.curr.key_base)

    if tool.opts.zsk_opts.sign_next:
        zsk_keys.append(zsk_key.next.key_base)

    return (ksk_keys, zsk_keys)


def zone_sign(tool, staging, domain, zonefile, ksk_keys, zsk_keys, zone_signed_link):
    """
    Sign zone file with 1 or more KSK and 1 or more ZSK keys
     signoptions
      -n        - NSEC3
      -p        - allow opt-out => insecure delegations allowed after zone signed (turn off?)
      -b        - add comments
      -s        - add salt
    """
    # pylint: disable=R0914
    opts = tool.opts
    start_dir = os.getcwd()
    os.chdir(tool.opts.work_dir)
    expire_in = tool.opts.expire

    zone_signed_file = _signed_path(tool, staging, domain, zone_signed_link)

    expiry = _expire_to_dt_string(expire_in)
    salt = os.urandom(16)
    salt = salt.hex()
    prog = '/usr/bin/ldns-signzone'

    pargs = [prog, '-n', '-p', '-b', '-s', salt, '-e', expiry]
    pargs += ['-f', zone_signed_file, zonefile]
    pargs += ksk_keys + zsk_keys     # xSK_KEYS are arrays of keys

    [retc, _output, errors] = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        print(f'  ** Failed to run {prog}')
        if errors:
            print(errors)
    os.chdir(start_dir)

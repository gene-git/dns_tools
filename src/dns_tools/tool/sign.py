# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Sign zone file

signed zone file: is signed/data/domain-basename-datetime.
Link: signed/domain.signed -> actual file.

datetime is 1 sec accuracy to permit multiple signs
per day if needed - 1 min may be sufficient.


 etc_nsd/
       zones/
           same structure as staging/zones

       staging/zones/
           domain          # zone file
           domain.signed/
               link_name -> data/<date-time>
               data/
                   <date-time>  # prepend KSK/ZSK or use DS DNSKEY

"""
# pylint: disable=invalid-name, too-many-arguments
import os
import datetime
import re

from pyconcurrent import run_prog

from dns_tools.utils import make_dir_if_needed
from dns_tools.utils import make_symlink

from .dnstool_base import DnsToolBase


def _expire_to_dt_string(expire_in: str) -> str:
    """
    Map input expire in form '90d' into formatted datetime string.

    Returns:
        str:
        Format is YYYYMMddHHMMSS
    """
    if not expire_in:
        expire_in = '90d'

    units = re.sub(r'[\-\d+-]*', '', expire_in)
    delta_str = expire_in.replace(units, '')
    delta = int(delta_str)

    now = datetime.datetime.now()
    if units.startswith('d'):
        dt = now + datetime.timedelta(days=delta)

    elif units.startswith('m'):
        dt = now + datetime.timedelta(days=delta*30)     # approximation

    elif units.startswith('y'):
        dt = now + datetime.timedelta(days=delta*365)    # approximation

    elif units.startswith('h'):
        dt = now + datetime.timedelta(hours=delta)

    elif units.startswith('w'):
        dt = now + datetime.timedelta(days=7*delta)

    elif units.startswith('M'):
        dt = now + datetime.timedelta(days=30*delta)

    else:
        dt = now + datetime.timedelta(seconds=delta)

    expiry = dt.strftime('%Y%m%d%H%M%S')

    return expiry


def _signed_path(tool: DnsToolBase, staging: str,
                 domain: str, link_file: str) -> str:
    """
    Add link: zone -> data/<date-time>
    Return path to data/<date-time> where data
    is to be written.
    Might be better to write file before making the link
    """
    opts = tool.opts
    start_dir: str = os.getcwd()

    dom_signed_dir = f'{domain}.signed'
    link_dir = os.path.join(staging, dom_signed_dir)
    signed_dir = os.path.join(link_dir, 'data')

    if not opts.test:
        make_dir_if_needed(signed_dir)

    dt_string = tool.opts.now

    signed_file = dt_string
    signed_file_rel = os.path.join('data', signed_file)
    signed_path = os.path.join(signed_dir, signed_file)

    #
    # Do symlink here
    #
    os.chdir(link_dir)
    if not opts.test:
        make_symlink(signed_file_rel, link_file)
    os.chdir(start_dir)

    signed_path = os.path.normpath(signed_path)
    signed_path = os.path.abspath(signed_path)

    return signed_path


def _base_name_to_hash_vers(base_name: str) -> str:
    """
     Given basename of form:
        K<domain>.+<type>+<id>.extension
     extract +<type>+<id>.

     base_name.key is a link which points to xxx/K<dom>.+nnn+mmm.key
     So we look up the link target and take base name of that to derive
     the Ids we want.
    """
    link = f'{base_name}.key'
    path = os.readlink(link)
    file = os.path.basename(path)
    word = file.split('+')
    type_id = f'+{word[1]}+{word[2]}'
    type_id = type_id.split('.', maxsplit=1)[0]     # remove .key
    return type_id


def get_signing_key_base_names(tool: DnsToolBase, domain: str
                               ) -> tuple[list[str], list[str]]:
    """
    Retrieve list of keys to be used to sign this domain
    """
    opts = tool.opts
    dom_keys = tool.keys[domain]
    ksk_key = dom_keys.ksk
    zsk_key = dom_keys.zsk

    ksk_keys = []
    zsk_keys = []

    #
    # KSK
    #
    key_opts = opts.key_opts
    if key_opts.ksk.sign_curr:
        ksk_keys.append(ksk_key.curr.key_base)

    if key_opts.ksk.sign_next:
        ksk_keys.append(ksk_key.next.key_base)

    #
    # ZSK
    #
    if key_opts.zsk.sign_curr:
        zsk_keys.append(zsk_key.curr.key_base)

    if key_opts.zsk.sign_next:
        zsk_keys.append(zsk_key.next.key_base)

    return (ksk_keys, zsk_keys)


def zone_sign(tool: DnsToolBase, staging: str, domain: str,
              zonefile: str, ksk_keys, zsk_keys, zone_signed_link):
    """
    Sign zone file with 1 or more KSK and 1 or more ZSK keys.

    sign options
      -n        - NSEC3
      -p        - allow opt-out => insecure delegations allowed
                  after zone signed (should we turn this off?)
      -b        - add comments
      -s        - add salt
    """
    # pylint: disable=too-many-positional-arguments,too-many-locals
    opts = tool.opts
    msg = opts.prnt.msg
    start_dir = os.getcwd()
    expire_in = opts.expire

    os.chdir(opts.work_dir)

    zone_signed_file = _signed_path(tool, staging, domain, zone_signed_link)

    expiry = _expire_to_dt_string(expire_in)
    salt_binary = os.urandom(16)
    salt = salt_binary.hex()

    pargs = ['/usr/bin/ldns-signzone']
    pargs += ['-n', '-p', '-b', '-s', salt, '-e', expiry]
    pargs += ['-f', zone_signed_file, zonefile]
    pargs += ksk_keys + zsk_keys     # ?SK_KEYS are arrays of keys

    (retc, _output, errors) = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        msg(f'  ** Failed to run {pargs[0]}\n')
        if errors:
            msg(errors)

    os.chdir(start_dir)

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Handle generating keys
"""
# pylint: disable=invalid-name,too-many-locals
from typing import (List)
import os

from config import ToolOpts
from utils import run_prog
from utils import (make_dir_if_needed, make_symlink, open_file)

from ._keyinfo_base import KeyInfoBase
from ._keyfile_extensions import keyfile_extensions


def _dns_key_make(opts: ToolOpts, key_info: KeyInfoBase) -> str:
    """
    link name is curr or next (taken from key_info.which)

    Returns:
        str:
        key_basename - if all well (dummy in test mode)
        Empty string ('') if not.
    """
    cwd = os.getcwd()

    domain = key_info.domain
    this_key_dir = key_info.this_key_dir
    link_base = key_info.key_base
    ktype = key_info.ktype
    msg = opts.prnt.msg

    exts = keyfile_extensions(key_info.ktype)

    msg(f'      Making {ktype} key for {domain}\n')

    #
    # key goes in data/K<domain>+xx+yyy/key, private, ...]
    #  link this_key_dir -> data/xxx
    #
    data = 'data'
    key_dir_data = os.path.join(this_key_dir, data)
    if not opts.test:
        make_dir_if_needed(key_dir_data)

    #
    # Make the keys x.key x.private (x.ds for KSK)
    #
    pargs = ['/usr/bin/ldns-keygen', '-a', 'ED25519']
    if ktype == 'ksk':
        pargs += ['-k']
    pargs += [domain]

    #
    # NB --> we must chdir to key data dir
    #
    os.chdir(key_dir_data)

    (retc, output, errors) = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        msg(f' Error: Failed to run {pargs[0]}\n', fg='error')
        if errors:
            print(errors)
        return ''

    #
    # test mode has nothing more to do
    #
    if opts.test:
        return 'test-key-basename'
    #
    # ldns-keygen prints the basename for the key files: K<name>+<alg>+<id>
    # which we keep as key_id
    #
    key_basename = output.strip()

    #
    # extract set of DS into .all.ds file
    #
    if ktype == 'ksk' and not opts.test:
        _ds_all = _make_all_ds(opts, domain, key_basename)
        if not _ds_all:
            msg(' ksk error making all DS key files')
            return ''
    #
    # Make links key_dir/curr.xx -> data/K<dom>....key etc
    #
    os.chdir(this_key_dir)
    for ext in exts:
        src = os.path.join(data, key_basename + ext)
        lnk = link_base + ext
        if not opts.test:
            make_symlink(src, lnk)

    os.chdir(cwd)
    return key_basename


def _make_dummy_zone():
    """
    For different DS records we use a dummy zone and
    then ldns-keys2ds to extract DS records.
    """
    dumz = """
; $ORIGIN ; skipped
$TTL 1800
@       IN      SOA     master.example.com.    email.example.com. (
    2022010101
    3600
    900
    1209600
    1800
    )
@       IN      NS      master.example.com.
@       IN      A       1.1.1.1
; end dummy
"""

    return dumz


def _make_all_ds(opts: ToolOpts, domain, key_basename: str) -> List[str]:
    """
     Make all DS keys extracted from signed dummy zone file
     Stay in domain key dir
     NB = we fake this and use the KSK for both KSK and ZSK
          since we're only doing this to extract DS
    """
    ds_all: List[str] = []
    msg = opts.prnt.msg

    msg(f'    Making DS for {domain}\n')

    #
    # write dummy zone with no ORIGIN
    #
    dummy_zone = _make_dummy_zone()
    dummy_file = f'./dummy-{domain}.zone'
    dummy_file_signed = f'{dummy_file}.signed'
    fobj = open_file(dummy_file, 'w')
    if fobj:
        fobj.write(dummy_zone)
        fobj.close()
    else:
        msg('Error writing dummy zone in _make_all_ds()', fg='error')
        return ds_all

    #
    # Sign dummy file with our KSK and use same KSK for ZSK
    # signed file will be in
    #
    origin = f'{domain}.'
    ksk = key_basename
    zsk = ksk

    pargs = ['/usr/bin/ldns-signzone']
    pargs += ['-p', '-n', '-o', origin, dummy_file, zsk, ksk]

    (retc, _output, errors) = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        msg(f' Error ** Failed to run {pargs[0]}\n', fg='error')
        if errors:
            print(errors)
        return ds_all

    #
    # extact DS
    # hash:
    # 1   SHA-1   MANDATORY   [RFC3658]
    # 2   SHA-256 MANDATORY   [RFC4509]
    # 3   GOST R 34.11-94     DEPRECATED  [RFC5933][Change the status of
    #                         GOST Signature Algorithms in DNSSEC in the
    #                         IETF stream to Historic]
    # 4   SHA-384 OPTIONAL    [RFC6605]
    # 5   GOST R 34.11-2012   OPTIONAL [RFC9558] RU equivalent to SHA-256
    # 6   SM3 OPTIONAL        [RFC9563] CN equivalent to SHA-256
    # 7-255 - unassigned
    #
    # ldns-key2ds -n:
    #   Write the result DS Resource Record to stdout instead of a file
    #
    hashes = ['-1', '-2', '-4']
    for hsh in hashes:
        pargs = ['/usr/bin/ldns-key2ds', '-n', hsh, dummy_file_signed]
        (retc, ds_basename, errors) = run_prog(pargs, test=opts.test)
        if retc != 0:
            msg(f' Error ** Failed to run {pargs[0]}\n', fg='error')
            if errors:
                print(errors)
        ds_all.append(ds_basename)

    #
    # remove dummy files
    #
    os.unlink(dummy_file)
    os.unlink(dummy_file_signed)

    #
    # write it out
    #
    ds_file = f'{key_basename}.all.ds'
    fobj = open_file(ds_file, 'w')
    if fobj:
        for ds in ds_all:
            fobj.write(ds)
        fobj.close()
    return ds_all


def generate_key(opts: ToolOpts, key_info: KeyInfoBase) -> str:
    """
     Generate key of type ktype (ksk or zsk) for key_info.domain
    """
    msg = opts.prnt.msg

    if key_info.ktype == 'ksk':
        top = '***************** WARNING ******************'
        bot = '********************************************'

        msg(f'\n  {top}\n', fg='warn')
        msg('      changing KSK (key signing key \n', fg='warn')
        msg('      Upload DS to registrar\n', fg='warn')
        msg(f'  {bot}\n', fg='warn')

    key_basename = _dns_key_make(opts, key_info)
    return key_basename

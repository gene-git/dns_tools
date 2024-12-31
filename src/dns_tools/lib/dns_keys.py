# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Handle generating keys
"""
# pylint: disable=invalid-name,too-many-locals
import os
from .run_prog import run_prog
from .tools import make_dir_if_needed
from .tools import make_symlink
from .tools import open_file

def _dns_key_make (tool, dnskey, kinfo):
    """
    link name is curr or next (taken from kinfo.which)
    """
    cwd = os.getcwd()

    domain = dnskey.domain
    this_key_dir = dnskey.this_key_dir
    link_base = kinfo.key_base
    exts = dnskey.exts
    ktype = dnskey.ktype
    opts = tool.opts
    msg = tool.prnt.msg

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
    # NB --> we must to key data dir
    #
    os.chdir(key_dir_data)

    [retc, output, errors] = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        msg(f' Error: Failed to run {pargs[0]}', fg_col='error')
        if errors:
            print(errors)
        return None

    #
    # test mode has nothing more to do
    #
    if opts.test:
        return None
    #
    # ldns-keygen prints the basename for the key files: K<name>+<alg>+<id>
    # which we keep as key_id
    #
    key_basename = output.strip()

    #
    # extract set of DS into .all.ds file
    #
    if ktype == 'ksk' and not tool.opts.test:
        _ds_all = _make_all_ds(tool, domain, key_basename)

    #
    # Make links key_dir/curr.xx -> data/K<dom>....key etc
    #
    os.chdir(this_key_dir)
    for ext in exts:
        src = os.path.join(data, key_basename + ext)
        lnk = link_base + ext
        if not tool.opts.test:
            make_symlink(src, lnk )

    os.chdir(cwd)
    return key_basename

def _make_dummy_zone():
    """
    To get different DS records we create a dummy zone and use ldns-keys2ds to extract DS records
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

def _make_all_ds(tool, domain, key_basename):
    """
     Make all DS keys extracted from signed dummy zone file
     Stay in domain key dir
     NB = we fake this and use the KSK for both KSK and ZSK
          since we're only doing this to extract DS
    """
    ds_all = []
    opts = tool.opts
    msg = tool.prnt.msg

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
        msg('Error writing dummy zone in _make_all_ds()', fg_col='error')
        return ds_all

    #
    # Sign dummy file with our KSK and use same KSK for ZSK
    # signed file will be in
    #
    origin = f'{domain}.'
    ksk = key_basename
    zsk = ksk

    pargs = ['/usr/bin/ldns-signzone', '-p', '-n', '-o', origin, dummy_file, zsk, ksk]

    [retc, _output, errors] = run_prog(pargs, test=opts.test, verb=opts.verb)
    if retc != 0:
        msg(f' Error ** Failed to run {pargs[0]}\n', fg_col='error')
        if errors:
            print(errors)

    #
    # extact DS
    # hash: -1 = sha1
    #       -2 = sha256
    #       -4 = sha384
    #       -g = gost (unsupported in our ldns)
    # ldns-key2ds -n: Write the result DS Resource Record to stdout instead of a file
    #
    hashes = ['-1', '-2', '-4']
    for hsh in hashes:
        pargs = ['/usr/bin/ldns-key2ds', '-n', hsh, dummy_file_signed]
        [retc, this_ds_basename, errors] = run_prog(pargs, test=tool.opts.test)
        if retc != 0:
            msg(f' Error ** Failed to run {pargs[0]}\n', fg_col='error')
            if errors:
                print(errors)
        ds_all.append(this_ds_basename)

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
        for ds in ds_all :
            fobj.write(ds)
        fobj.close()
    return ds_all

def get_key_id_from_keyfile (kinfo):
    """
    Get existing key_id = what which.key link  points to (minus the trailing .key)
     Returns linkname and key basename or None if link doesn't exist
    """
    key_link = kinfo.key_link
    this_key_dir = kinfo.this_key_dir
    key_id = None

    if os.path.islink(key_link):
        targ_file = os.readlink(key_link)
        file = os.path.basename(targ_file)
        targ_path = os.path.join(this_key_dir, targ_file)

        if os.path.isfile(targ_path):
            key_id = file[0:-4]                 # strip trailing .key

    return key_id

def generate_new_key (tool, dnskey, kinfo):
    """
     Generate key of type ktype (ksh or zsk) for dnskey.domain
    """
    msg = tool.prnt.msg

    if dnskey.ktype == 'ksk':
        msg('  ***************** WARNING ******************\n', fg_col='warn')
        msg('      changing KSK (key signing key \n', fg_col='warn')
        msg('      Upload DS to registrar \n', fg_col='warn')
        msg('  ********************************************\n', fg_col='warn')
    key_basename = _dns_key_make(tool, dnskey, kinfo)
    return key_basename

# dns_tools - Coming Soon -

DNS server tools for DNSSEC etc

DNSSEC can be a little tricky especially rolling the keys. We procide the tools 
to simplify and automate this as much as possible. 

## Installation

On Arch can simply build using the PKGBUILD provided in packaging dir and available in the AUR.

To build it manually, clone the repo and do:

        rm -f dist/*
        poetry build --format wheel
        root_dest="/"
        ./scripts/do-install $root_dest

  If running as non-root then set root\_dest a user writable directory

### Dependencies

- Run Time :
  - python (3.9 or later)
  - ldns
  - If python < 3.11 : tomli (aka python-tomli)

- Building Package:
  - git
  - poetry (aka python-poetry)
  - wheel (aka python-wheel)
  - pip (aka python-pip)
  - rsync

## Interesting, New or Coming Soon

### New

## Using the tools

### dns-tool

This tool handles all key operations (create, roll etc) as well as using the keys
to sign dns zone files.

### dns-prod-push

This tool make it simple to push signed and unsigned dns zone files from the signing server to the
production area for each primary dns server.

### dns-serial-bump

A standalone tool to bump the serial number in a dns zone file.

### Quick reminder that DNSSEC utilizes 2 kinds of keys

 - Zone Signing Key (ZSK)  
   This is used to sign dns zone files. It is advisable to update this periodically, 
   perhaps every 1 to 3 months.  The mechanism to update the key requires some care
   and is known as *rolling* the keys. The tools make this straightforward. More on this later.

 - Key Signing Key (KSK)  
   This signs the zone signing key - and its this key that must be registered with
   the domain registrar for the root servers. The requirment ensures that there 
   is an appropriate chain of trust from the root dns servers on down. 
   Most, if not all registars now support DNSSEC - Google Domains does for example. 
   This requirement means there is a manual step whenver the KSK changes, which is updating
   the root server with the new information.  KSK should be rolled occasionally,
   in spite of the manual step, perhaps every 1-3 years, and the corresponding DS 
   (Delegation Signer) record for the new KSK should be uploaded to the domain registrar.

### Key Rolling  
   The typical approach to doing this is accomplished in 2 basic steps. 

   - Phase 1  
     Create a new key, called *next*, then sign the zone files using this key as well as
     the current key (we call this *curr* for short). With the records now double signed
     the existing key remains valid.

   - Phase 2  
     After a period sufficiently longer than the TTL for the zone, say 2 x TTL, then
     rename the *next* key to be the *curr* key. Resign using just this key.
     This gives time for DNS servers to catch up with the new key before the old one is removed. 

Rolling KSK and ZSK is basically the same, but for KSK, the DS records
must be uploaded to the domain registrar. In Phase 1 both old and new DS should be uploaded
and in Phase 2 just the new (now current) KSK DS.  The tool creates the DS records
but uploading them to registrar must be done manually.

### Example Usage

The tool supports 2 primary servers - an internal DNS server and the external server. 
The internal server may also serve additional unsigned zones, typically RFC1918 and 
their reverse zones. The external prinary is how the outside world views DNS 
for the domain.  As usual once a primary dns server is updated, it's secondaries
will get updated as usual automatically via IXFR/AXFR.

The tool is driven by a simple config file which is first looked for in 
current directory under *./conf.d/config* and if not available there it
should be in */etc/dns_tools/conf.d/config*. 
The config file holds the information about where all the relevant files are kept
and the command to use to restart the dns servers. 

Copy the config file and edit it for your new needs:

        cd /etc/dns_tools
        cp conf.d/config.sample conf.d/config
        
Edit the config file to suit your needs. Set the *work_dir* to wherever you 
want to keep the internal/external zone files and the keys. 
The sample config uses */etc/dns_tools* for the working directory.
Relative directory names are always relative to the working directory.

The *work_dir* holds all the data and is the source for all key and zone information.
Signed and unsigned zone files are pushed from the working dir to each of the
DNS servers.  Internal and external dns zone files are kept in their own directories.
e.g.

    *<work_dir>/internal/staging/zones*

The *ldns* package has standalone tools which used to handle key generation
and to sign the zone files.

With that background information, and under the assumption that the domain registrar
already has the ksk required information then to roll ZSK using dns\_tools would be simply:

        /usr/bin/dns-tool --zsk_roll_1
        /usr/bin/dns-prod-push --dns_restart --to_production

and after couple hours or similar time, the second phase would be accomplished using:

        /usr/bin/dns-tool --zsk_roll_2
        /usr/bin/dns-prod-push --dns_restart --to_production

And of course in practice each of these would be run from cron - I run them monthly. 
Sample crons are provided. 

To get things started simply create the KSK and ZSK keys and then upload the DS key info
to the domain registrar. To generate a new set of keys simply run:

        /usr/bin/dns-tool --gen_ksk_curr --gen_zsk_curr

All the keys will be under the *keys* directory. For each domain, the info needed 
for the domain registrar will be found in the file:

        keys/<domain>/ksk/curr.all.ds

### testing

For convenience each tool supports a test mode engaged using the *-t, --test* option.
When run in test mode, actions are printed instead of actually being done.

For testing, I also find it convenient to change the production dns zone directores 
to something like */tmp/dns* - and then run the tests without *-t*. This does everything 
as asked, but instead of pushing to the real dns servers, the files are pushed to the
test production directory. When doing this, you can drop the *--dns_restart* option 
so as to skip restarting the dns servers - which is not needed obviously.

## KSK Keys and DS to root servers

When you create KSK keys there will also be DS keys generated automatically. 
Actually these come in different hash types:

 - 1 : sha1   
       shouldn't be used
 - 2 : sha256   
       the default and saved in curr.ds
 - 4 : sha512  
 - g : gost (we do not generate this)  

These are saved into *<work_dir>/keys/<domain>/ksk/* directory.
In addition to *curr.ds*, there is *curr.all.ds* which contains sha1, sha256 and sha512.
Choose one or more of these to upload to your domain registrar.  

Its good to get this uploaded and available from the root servers soon as you've your 
KSK keys are ready and before you push any signed zones out. This is the only manual step.
And if/when you roll your ksk, then it needs to be repeated with the new key info.

Everthing else should be handled automatically by the tool.

## Updating dns zone files

Whenever you update any zone files, they must be resigned. Make any zone file changes 
in the zone staging directories. i.e.

        *<work_dir>/internal/staging/zones*
        *<work_dir>/external/staging/zones*

You don't need to bump serial number, the tool will do it for you, though its benign to do so.
When you're done with the changes then to resign and push just run:

        /usr/bin/dns-tool --sign
        /usr/bin/dns-prod-push --dns_restart --to_production


or use the convenience wrapper script for these 2 commands by running:

        /etc/dns_tool/resign.sh
        
## Overview of Options

### dns-tool

Handles key generation, zone signing and key rolls.

While there are many options, majority are more for testing or speical needs. The main options
are *test*, *print_keys*, *sign*, *zsk_toll_1*, *zsk_roll_2* 

 - *-h, --help*   
   show this help message and exit

 - *-t, --test*    
   Test mode - print but dont do

 - *-v, --verb*   
   More verbosity

 - *--serial_bump*   
   Bump all serials. Not usually needed as happens auotmatically

 - *-keep, --keep_include*   
   Keep temp file which has $INCLUDE expanded

 - *--sign*   
   Short hand for sign with curr keys (ksk and zsk)

 - *--print_keys*  
   Print keys (curr and next)

 - *-skc, --sign_ksk_curr*   
   Sign with curr ksk

 - *-skn, --sign_ksk_next*   
   Sign with next ksk

 - *-szc, --sign_zsk_curr*   
   Sign with curr zsk

 - *-szn, --sign_zsk_next*  
   Sign with next zsk

 - *--gen_zsk_curru*  
   Generate ZSK for curr

 - *--gen_zsk_next*  
   Generate ZSK for next

 - *--gen_ksk_curr*  
  Generate KSK for curr

 - *--gen_ksk_next*    
   Generate KSK for next

 - *--zsk_roll_1*    
   ZSK Phase 1 roll - old and new

 - *--zsk_roll_2*    
   ZSK Phase 2 roll - new only

 - *--ksk_roll_1*    
   KSK Phase 1 roll - old and new - NB must add to degistrar

 - *--ksk_roll_2*    
   KSK Phase 2 roll - new only

### dns-prod-push

Tool to push signed and unsigned zones to the dns server(s)

 - *-h, --help*  
   show this help message and exit

 - *-int_ext what*   
   What to push. One of : internal, external or both (both)

 - *--to_production*   
   Copy zone files from work staging area to live production area

 - *--dns_restart*  
   Restart the dns server after update zones using the config variable:  
   dns_restart_cmd. For example for nsd, set this to:
    dns_restart_cmd = "/usr/bin/systemctl restart nsd"  

 - *-t, --test*   
   Test mode - print but dont do

 - *-v, --verb*   
   More verbosity


### dns-serial-bump

Tool to bump the serial number of a DNS zone file. To use it:

        dne-searial-bump <zonefile>

## Contributing

## License

`dns_tools` was created by Gene C. It is licensed under the terms of the MIT license.

 - SPDX-License-Identifier: MIT
 - Copyright (c) 2023, Gene C

## Credits


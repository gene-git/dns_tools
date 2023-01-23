# dns_tools

DNS server tools - aka DNSSEC made easy.

DNSSEC can be a little tricky especially rolling the keys. We provide the tools 
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

 - Added FAQ to bottom of README

## Using the tools

It provides the following set of tools.

### dns-tool

This tool handles all DNSSEC related operations including key creation and rolling, and 
using those keys to sign the dns zone files. 


### dns-prod-push

This tool make it simple to push signed and/or unsigned dns zone files from the signing server to the
production area for each primary dns server. the DNS primary server(s) should be on same machine
or reachable via ssh. It also restarts those servers when appropriate.

### dns-serial-bump

A standalone tool to check the validity and bump the serial number in the SOA of a dns zone file.

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
   This requirement means there is a manual step whenever the KSK changes, which is updating
   the root servers with the new information.  KSK should be rolled occasionally,
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

N.B. :

 - Must run on signing server.  
   The tools must be run on the signing server which is defined in the config file.  
   To minimize chance of an accident, the code will refuse to run if that is not the case.

 - Run as root.    
   2 operations require effective root user:
   - Changing the ownership permisions of staging zones to *dns_user* and *dns_group*.
   - Preserving ownership when files rsync --owner to dns server(s)

 - Zone serial numbers should be in canonical format for serial bump to work properly.  
   i.e. yyymmddnn where yyymmdd is date and nn is a 2 digit counter from 01 to 99
   If not code will do best it can to migrate to canonical format if possible.
   It will warn of non-standard or invalid serials and replace them with
   valid serials. A valid serial is all numbers and must be expressable as 
   32 bits. You can use the *dns-serial-bump --check zonefile* to check
   for valid serial.

The tool supports 2 primary servers - an internal DNS server and the external server. 
The internal server may also serve additional unsigned zones, typically RFC1918 and 
their reverse zones. There can be unsigned zones for external server too of course 
and if there are, they will be pushed along with all the other signed zones.

The external prinary is how the outside world views DNS for each domain.  
As usual once a primary dns server is updated, it's secondaries
will get updated automatically via IXFR/AXFR.

The tool is driven by a straightforward config file which is first looked for in 
current directory under *./conf.d/config* and if not available there it
should be in */etc/dns_tools/conf.d/config*. 

The config file holds the information about where all the relevant files are kept
and the command to use to restart the dns servers, the DNS server hosts and so on. 

Copy the sample config file and edit it for your needs:

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

        <work_dir>/keys/<domain>/ksk/curr.all.ds

By default all the domains in the config are processed. To process a one or more specific
domains just put them on the command line. Domains listed on command line will
override the config file.

### testing

For convenience each tool supports a test mode engaged using the *-t, --test* option.
When run in test mode, actions are printed instead of actually being done.

When running in test mode nothing is done, which can lead to things seemingly 
being strange. For example, when testing rolling or generation of *next* keys,
the code later checks for any missing keys. Now in test mode they can be missing
since they were not actually created when they would normally be. So
now you can see messages about keys being generated a second time. 
They wont be in non-test mode of course as nothing would be missing.

For testing, I also find it convenient to change the production dns zone directores 
to something like */tmp/dns* - and then run the tests without *-t*. This does everything 
as asked, but instead of pushing to the real dns servers, the files are pushed to the
test production directory. When doing this, you can drop the *--dns_restart* option 
so as to skip restarting the dns servers - which is not needed obviously.

## KSK Keys and DS to root servers

When you create KSK keys there will also be DS keys generated automatically. 
Actually these come in different hash types:

 - 1 : sha1   - deprecated and shouldn't be used
 - 2 : sha256 - the default and saved in curr.ds
 - 4 : sha512 - slower but somewhat more secure hash 
 - g : gost (we do not generate this)  

These are saved into *\<work_dir\>/keys/\<domain\>/ksk/* directory.
In addition to *curr.ds*, *curr.all.ds* contains sha1, sha256 and sha512.
Choose one or more of these to upload to your domain registrar.   

Its good to get this uploaded and available from the root servers soon as your 
KSK keys are ready and before you push any signed zones out. This is the only manual step.
And if/when you roll your ksk, then it needs to be repeated with the new DS key info.

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

 - positional arguments:  
   one or more domains here will override config file.

 - *-h, --help*   
   show this help message and exit

 - *--theme*  
   Output color theme for tty. One of : dark, light or none

 - *-t, --test*    
   Test mode - print but dont do

 - *-v, --verb*   
   More verbosity

 - *--serial_bump*   
   Bump all serials. Not usually needed as happens auotmatically
   This implies *--sign* so that signed zones stay consistent.

 - *--keep_include*   
   Keep temp file which has $INCLUDE expanded

 - *--sign*   
   Short hand for sign with curr keys (ksk and zsk)

 - *--sign_ksk_next*   
   Sign with next ksk

 - *--sign_zsk_next*  
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

 - *--print_keys*  
   Print keys (curr and next)

### dns-prod-push

Tool to push signed and unsigned zones to the dns server(s)

 - positional arguments:  
   one or more domains here will override config file.

 - *-h, --help*  
   show help message and exit

 - *--theme*  
   Output color theme for tty. One of : dark, light or none

 - *--int_ext what*   
   What to push. One of : internal, external or both (default is both)

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

        dne-serial-bump [-c] <zonefile>

 - positional arguments  
   One or more zonefiles with SOA containing a serial number.

 - *-h, --help*  
   show help message and exit

 - *-c, --check*  
   Check and show current and updated serial number for each zonefile. When check is enabled
   zonefiles do not have their serial number updated.
   Without *check* option each zonefile will also be updated with new serial.

## FAQ

### Why is name not dnssec_tools?

This is a good question. I did give some thought to this and ended up with the more generic name.

My thinking is this. Since the tool is really about managing DNS zones in one place and 
not just about keys/signing I went with the more generic name along with adding DNSSEC as a keyword.

There are three basic parts to the tools:

 - Check the validity and increment the serial number in the SOA section of zonefile.
 - Push zone files to primary DNS servers (internal and external facing servers) and 
   restart them.
 - Generate and manage KSK and ZSK keys and use them to sign zones.

While all of them are needed to provide automation of key rolls, the first two items above are
not specific to DNSSEC.

## License

`dns_tools` was created by Gene C. It is licensed under the terms of the MIT license.

 - SPDX-License-Identifier: MIT
 - Copyright (c) 2023, Gene C


Changelog
=========

**[3.5.0] ----- 2025-02-26** ::

	    ksk/zsk key algorithms are now settable from config/command line.
	      Supported algos are: ECDSAP256SHA256, ECDSAP384SHA384, ED25519 and ED448.
	      Default remains ED25519.
	      Some lint picking
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.4.5] ----- 2024-12-31** ::

	    Add git signing key to Arch Package
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.4.4] ----- 2024-12-31** ::

	    typo
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.4.3] ----- 2024-12-31** ::

	    Git tags are now signed.
	    Update SPDX tags
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.4.2] ----- 2024-09-07** ::

	    More rst tweaks


**[3.4.1] ----- 2024-09-07** ::

	    update Docs/Changelog.rst Docs/dns_tools.pdf
	    Fix up restructred test formatting in README
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.4.0] ----- 2024-06-02** ::

	    Improve exception handling with setting file permissions
	    update requirements.txt to show dep on lockmgr
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.3.0] ----- 2024-03-30** ::

	    Lockfile now attached to uid
	    update readme
	    update Docs/Changelog.rst
	    update project version
	    use max(a,b) instead of if(a>b) etc
	    Now uses separate lockmgr package instead of local copy
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.1.1] ----- 2023-12-26** ::

	    Remove tomli from depends() in PKGBUILD as not needed for python >= 3.11
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.1.0] ----- 2023-11-26** ::

	    Switch python backend build to hatch
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[3.0.0] ----- 2023-11-16** ::

	    Some lint cleanups.
	    Add lock to ensure only one dns-tool runs at a time.
	    NB The inotify code, used to wait on lock, uses inotify in libc
	      This returns a struct inotify_event and the size of this struct is important.
	      Best I know on every (linux) system the struct size is:
	        (int, uint_32_t, uint_32_t, uint_32_t, ...)
	      If you find a system where they are different (see man inotify) let me know!
	    update Docs/Changelog.rst Docs/dns_tools.pdf


**[2.6.0] ----- 2023-11-12** ::

	    resign.sh accept --serial-bump, -s, --serial_bump
	    Do not expand $INCLUDE when in a comment line before signing
	    update Docs/Changelog.rst


**[2.5.0] ----- 2023-11-06** ::

	    scripts/resign.sh now has optional argument --serial-bump
	    resign.sh now takes optional domain list.
	      If none provided then does all domeains in /etc/dns_tool/conf.d/config as previously
	    update readme for resign.sh changes
	    fix typo in comment
	    update Docs/Changelog.rst


**[2.4.0] ----- 2023-09-27** ::

	    Reorg and rework documentation.
	    Now simple to generate html and pdf docs using sphinx
	    update CHANGELOG.md


**[2.3.2] ----- 2023-05-18** ::

	    Update build info in README
	    update CHANGELOG.md


**[2.3.1] ----- 2023-05-18** ::

	    PKGBUILD - add dependency on python installer module
	    update CHANGELOG.md


**[2.3.0] ----- 2023-05-18** ::

	    install: switch from pip to python installer package. This adds optimized bytecode
	    update CHANGELOG.md


**[2.2.4] ----- 2023-05-18** ::

	    PKGBUILD: add python-build to makedepends
	    update CHANGELOG.md


**[2.2.3] ----- 2023-05-18** ::

	    PKGBUILD: build wheel back to using python -m build instead of poetry
	    update CHANGELOG.md


**[2.2.2] ----- 2023-05-17** ::

	    Simplify Arch PKGBUILD and more closely follow arch guidelines
	    update CHANGELOG.md


**[2.2.1] ----- 2023-04-16** ::

	    update 2.2.1 with few more notes about KSK and root servers
	    Add few more lines about root servers and KSK
	    update CHANGELOG.md


**[2.2.0] ----- 2023-02-10** ::

	    Fix typo in rsync - this case is not used here
	    update CHANGELOG.md


**[2.1.0] ----- 2023-02-04** ::

	    rel_from_abs_path now uses os.path.relpath() instead of our own function
	    Improve message about checking to ensure required keys are available
	    Small readme changes
	    more readme changes
	    readme tweaks
	    update CHANGELOG.md


**[2.0.2] ----- 2023-01-24** ::

	    Add note to change primary to point to signed zone files
	    readme whitespace markdown fix
	    more polishing of readme
	    tweak readme
	    Add FAQ to readme
	    update CHANGELOG.md


**[2.0.1] ----- 2023-01-22** ::

	    Remove "coming soon" from readme
	    fix PKGBUILD
	    update CHANGELOG.md


**[2.0.0] ----- 2023-01-22** ::

	    Initial release
	    updated readme
	    improve readme
	    updated readme
	    readme update
	    Initial Commit



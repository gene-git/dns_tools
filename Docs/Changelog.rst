Changelog
=========

Tags
====

.. code-block:: text

	2.0.0 (2023-01-22) -> 5.1.1 (2026-01-04)
	109 commits.

Commits
=======


* 2026-01-04  : **5.1.1**

.. code-block:: text

              - fix type
              - update Docs/Changelog

* 2026-01-04  : **5.1.0**

.. code-block:: text

              - **Version 5.0.0**
            
                * Code Reorg
                * Switch packaging from hatch to uv
                * Testing to confirm all working on python 3.14.2
                * License GPL-2.0-or-later
 2025-06-26   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-26  : **4.10.1**

.. code-block:: text

              - update arch PKGBUILD
              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-26  : **4.10.0**

.. code-block:: text

              - Use run_prog from pyconcurrent if available otherwise use local copy.
                Sync local copy of run_prog from pyconcurrent
 2025-06-22   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-22  : **4.9.0**

.. code-block:: text

              - run_prog: Sync local copy with latest from pycocurrent
 2025-06-20   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-20  : **4.8.0**

.. code-block:: text

              - Pull local copy of latest run_prog from pycocurrent
 2025-06-16   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-15  : **4.7.0**

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-15  : **4.6.0**

.. code-block:: text

              - run_prog: Use non-blocking IO with the select() loop
 2025-06-10   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-10  : **4.5.0**

.. code-block:: text

              - Enhance run_prog to pass env.
                pytest now uses the run_prog from src via a symlink
 2025-06-08   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-08  : **4.4.1**

.. code-block:: text

              - remove debug
              - bug: dns-prod-push int-ext option defaulted off instead of both
                Improved code which runs external programs.
 2025-05-27   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-27  : **4.3.0**

.. code-block:: text

              - Fix option parser for dns-prod-push --int-ext
 2025-05-21   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-21  : **4.2.0**

.. code-block:: text

              - Use builtin types where possible. e.g. typing.List -> list
 2025-05-19   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-19  : **4.0.5**

.. code-block:: text

              - test fixup
              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-19  : **4.0.4**

.. code-block:: text

              - Arch PKGBUILD: move pytest to checkdepends instead of makedepends
 2025-05-16   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-16  : **4.0.3**

.. code-block:: text

              - Arch PKGBUILD add missed dependency on lockmgr
              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-16  : **4.0.2**

.. code-block:: text

              - Typo in Arch PKGBUILD
              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-16  : **4.0.0**

.. code-block:: text

              - Code now complies with: PEP-8, PEP-257, PEP-484 and PEP-561
                Refactor & clean ups (pretty big changes). Split into multiple modules.
                Add test suite using pytest
            
                  Our testing is clean but, given the large code changes, please
                  let us know if you find any issues.
            
                Command line long args can now use either hyphen or underscores
                    e.g. dns-tool treats *--zsk-roll-1* and *--zsk_roll_1* exactly the same.
                ;
 2025-03-11   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2025-03-11  : **3.7.0**

.. code-block:: text

              - Fix push to production options checker - bug introduced by changes to config/opts classes
              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2025-03-11  : **3.6.0**

.. code-block:: text

              - Remove dumb debugging breakpoints left in by mistake - so sorry
 2025-03-07   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2025-03-07  : **3.5.1**

.. code-block:: text

              - Small README changes
 2025-02-26   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2025-02-26  : **3.5.0**

.. code-block:: text

              - ksk/zsk key algorithms are now settable from config/command line.
                  Supported algos are: ECDSAP256SHA256, ECDSAP384SHA384, ED25519 and ED448.
                  Default remains ED25519.
                  Some lint picking
 2024-12-31   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-12-31  : **3.4.5**

.. code-block:: text

              - Add git signing key to Arch Package
              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-12-31  : **3.4.4**

.. code-block:: text

              - typo
              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-12-31  : **3.4.3**

.. code-block:: text

              - Git tags are now signed.
                Update SPDX tags
 2024-09-07   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-09-07  : **3.4.2**

.. code-block:: text

              - More rst tweaks

* 2024-09-07  : **3.4.1**

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf
              - Fix up restructred test formatting in README
 2024-06-02   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-06-02  : **3.4.0**

.. code-block:: text

              - Improve exception handling with setting file permissions
 2024-03-30   ⋯

.. code-block:: text

              - update requirements.txt to show dep on lockmgr
              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2024-03-30  : **3.3.0**

.. code-block:: text

              - Lockfile now attached to uid
              - update readme
              - update Docs/Changelog.rst
              - update project version
              - use max(a,b) instead of if(a>b) etc
              - Now uses separate lockmgr package instead of local copy
 2023-12-26   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2023-12-26  : **3.1.1**

.. code-block:: text

              - Remove tomli from depends() in PKGBUILD as not needed for python >= 3.11
 2023-11-26   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2023-11-26  : **3.1.0**

.. code-block:: text

              - Switch python backend build to hatch
 2023-11-16   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2023-11-16  : **3.0.0**

.. code-block:: text

              - Some lint cleanups.
                Add lock to ensure only one dns-tool runs at a time.
                NB The inotify code, used to wait on lock, uses inotify in libc
                  This returns a struct inotify_event and the size of this struct is important.
                  Best I know on every (linux) system the struct size is:
                    (int, uint_32_t, uint_32_t, uint_32_t, ...)
                  If you find a system where they are different (see man inotify) let me know!
 2023-11-12   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/dns_tools.pdf

* 2023-11-12  : **2.6.0**

.. code-block:: text

              - resign.sh accept --serial-bump, -s, --serial_bump
                Do not expand $INCLUDE when in a comment line before signing
 2023-11-06   ⋯

.. code-block:: text

              - update Docs/Changelog.rst

* 2023-11-06  : **2.5.0**

.. code-block:: text

              - scripts/resign.sh now has optional argument --serial-bump
                resign.sh now takes optional domain list.
                  If none provided then does all domeains in /etc/dns_tool/conf.d/config as previously
                update readme for resign.sh changes
                fix typo in comment
 2023-09-27   ⋯

.. code-block:: text

              - update Docs/Changelog.rst

* 2023-09-27  : **2.4.0**

.. code-block:: text

              - Reorg and rework documentation.
                Now simple to generate html and pdf docs using sphinx
 2023-05-18   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-05-18  : **2.3.2**

.. code-block:: text

              - Update build info in README
              - update CHANGELOG.md

* 2023-05-18  : **2.3.1**

.. code-block:: text

              - PKGBUILD - add dependency on python installer module
              - update CHANGELOG.md

* 2023-05-18  : **2.3.0**

.. code-block:: text

              - install: switch from pip to python installer package. This adds optimized bytecode
              - update CHANGELOG.md

* 2023-05-18  : **2.2.4**

.. code-block:: text

              - PKGBUILD: add python-build to makedepends
              - update CHANGELOG.md

* 2023-05-18  : **2.2.3**

.. code-block:: text

              - PKGBUILD: build wheel back to using python -m build instead of poetry
 2023-05-17   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-05-17  : **2.2.2**

.. code-block:: text

              - Simplify Arch PKGBUILD and more closely follow arch guidelines
 2023-04-16   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-04-16  : **2.2.1**

.. code-block:: text

              - update 2.2.1 with few more notes about KSK and root servers
              - Add few more lines about root servers and KSK
 2023-02-10   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-02-10  : **2.2.0**

.. code-block:: text

              - Fix typo in rsync - this case is not used here
 2023-02-04   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-02-04  : **2.1.0**

.. code-block:: text

              - rel_from_abs_path now uses os.path.relpath() instead of our own function
                Improve message about checking to ensure required keys are available
                Small readme changes
 2023-01-24   ⋯

.. code-block:: text

              - more readme changes
              - readme tweaks
              - update CHANGELOG.md

* 2023-01-24  : **2.0.2**

.. code-block:: text

              - Add note to change primary to point to signed zone files
 2023-01-23   ⋯

.. code-block:: text

              - readme whitespace markdown fix
              - more polishing of readme
              - tweak readme
              - Add FAQ to readme
 2023-01-22   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-01-22  : **2.0.1**

.. code-block:: text

              - Remove "coming soon" from readme
                fix PKGBUILD
              - update CHANGELOG.md

* 2023-01-22  : **2.0.0**

.. code-block:: text

              - Initial release
 2023-01-21   ⋯

.. code-block:: text

              - updated readme
              - improve readme
              - updated readme
 2023-01-20   ⋯

.. code-block:: text

              - readme update
              - Initial Commit



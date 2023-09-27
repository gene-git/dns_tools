Changelog
=========

[2.4.0] ----- 2023-09-27
 * update project version  
 * change pyproject.toml to use rst for readme  
 * Reorg and rework documentation.  
 * Now simple to generate html and pdf docs using sphinx  
 * update CHANGELOG.md  

[2.3.2] ----- 2023-05-18
 * update project version  
 * update CHANGELOG.md  

[2.3.1] ----- 2023-05-18
 * update project version  
 * install: switch from pip to python installer package. This adds optimized bytecode  
 * update CHANGELOG.md  
 * update project version  
 * update CHANGELOG.md  

[2.2.4] ----- 2023-05-18
 * update project version  
 * PKGBUILD: add python-build to makedepends  
 * update CHANGELOG.md  

[2.2.3] ----- 2023-05-18
 * update project version  
 * PKGBUILD: build wheel back to using python -m build instead of poetry  
 * update CHANGELOG.md  

[2.2.2] ----- 2023-05-17
 * update project version  
 * Simplify Arch PKGBUILD and more closely follow arch guidelines  
 * update CHANGELOG.md  

[2.2.1] ----- 2023-04-16
 * update project version  
 * Add few more lines about root servers and KSK  
 * update CHANGELOG.md  

[2.2.0] ----- 2023-02-10
 * update project version  
 * Fix typo in rsync - this case is not used here  
 * update CHANGELOG.md  

[2.1.0] ----- 2023-02-04
 * update project version  
 * Improve message about checking to ensure required keys are available  
 * more readme changes  
 * readme tweaks  
 * rel_from_abs_path now uses os.path.relpath() instead of our own function  
 * update CHANGELOG.md  

[2.0.2] ----- 2023-01-24
 * update project version  
 * Add note to change primary to point to signed zone files  
 * tiny readme tweak  
 * readme whitespace markdown fix  
 * more polishing of readme  
 * tweak README  
 * update CHANGELOG.md  

[2.0.1] ----- 2023-01-22
 * update project version  
 * remove coming soon from readme  
 * fix PKGBUILD  
 * update CHANGELOG.md  

[2.0.0] ----- 2023-01-22
 * update project version  
 * Enhance dns serial finder to handle both multiline and single line SOA  
 * Improve output messages - color, typos, test mode  
 * update CHANGELOG.md  

[1.17.0] ----- 2023-01-22
 * update project version  
 * Better missing key check messages  
 * update CHANGELOG.md  

[1.16.0] ----- 2023-01-22
 * update project version  
 * serial finder regex use group(serial) in place of group(1)  
 * Fix typo in dns-serial-bump  
 * Add comments on serial numbers  
 * Add comments on serial numbers  
 * remove old dns serial code  
 * update CHANGELOG.md  

[1.15.0] ----- 2023-01-22
 * update project version  
 * Refactor serial code.  
 * Replace serial increment code with more sophisticated version which identifes  
 * and handles (best it can) non-standard serials or invalid serials  
 * dns serial numbers should be in canonical format  
 * update CHANGELOG.md  

[1.14.0] ----- 2023-01-21
 * update project version  
 * readme comment on serial_bump implying sign  
 * If serial_bump then must also sign to keep things consistent  
 * When bumping serial - original now saved in zones.prev instead of zones/prev.  
 * Since we rsync zones we dont want these backups sent to dns server  
 * Tidy up options more - share more code across dns-tool/dns-prod-push  
 * update CHANGELOG.md  

[1.13.0] ----- 2023-01-21
 * update project version  
 * update readme with color theme info  
 * colorize output  
 * update CHANGELOG.md  

[1.12.0] ----- 2023-01-21
 * update project version  
 * remove some short options, more readme tidy up  
 * typo in readme  
 * update CHANGELOG.md  

[1.11.0] ----- 2023-01-21
 * update project version  
 * Check and warn if not root.  
 * Clean up signing output  
 * Warn if not root for zone file perms, and rsync --owner  
 * update CHANGELOG.md  

[1.10.0] ----- 2023-01-21
 * update project version  
 * Code clean ups  
 * Add check that tools are running on signing server - this is required  
 * update CHANGELOG.md  

[1.9.0] ----- 2023-01-20
 * update project version  
 * lint picking  
 * Improve output of dns server restart section  
 * tweak output of prod push  
 * update CHANGELOG.md  

[1.8.0] ----- 2023-01-20
 * update project version  
 * improve output for dns-prog-push  
 * update CHANGELOG.md  

[1.7.1] ----- 2023-01-20
 * update project version  
 * tidy scripts some  
 * lint picking - remove trailing whitespace  
 * update CHANGELOG.md  

[1.7.0] ----- 2023-01-20
 * update project version  
 * Tweak zone_perm() output  
 * Less verbose without --verb option  
 * bug fix in key write - closed file inside look - duh  
 * Tidy options and ensure --sign_ksk_next --sign_zsk_next work  
 * update CHANGELOG.md  

[1.6.0] ----- 2023-01-20
 * update project version  
 * typo in readme  
 * tweak readme  

[1.5.1] ----- 2023-01-19
 * update README  
 * update CHANGELOG.md  

[1.5.0] ----- 2023-01-18
 * update project version  
 * typo systemct -> systemctl  
 * Another bug/typo after changing external.server to external.dns_server  
 * bug/typo  
 * update CHANGELOG.md  

[1.4.1] ----- 2023-01-18
 * update project version  
 * Keep dns_restart separate request in dns-prod-push  
 * Simplify --dns_server_restart to --dns_restart.  
 * update CHANGELOG.md  

[1.4.0] ----- 2023-01-18
 * update project version  
 * update readme with changed options  
 * Add dns_restart_cmd config  
 * Simplify :  
 * - Eliminate prod staging  
 * - work_dir now uses staging_zone_dir (internal and external)  
 * - production now uses production_zone_dir  
 * - push now uses option: to_production  
 * more readme changes  
 * update CHANGELOG.md  

[1.3.0] ----- 2023-01-16
 * update project version  
 * More readme additions  
 * update CHANGELOG.md  

[1.2.0] ----- 2023-01-16
 * update project version  
 * script tidy ups  
 * Add CHANGELOG  
 * Simplify boolean expression  
 * Add input checker  
 * Announce which config file used  
 * Add to README  
 * debug off  
 * bug fixes  
 * Start writing up README  
 * fix /etc/dns_tools not dns_tool  
 * update CHANGELOG.md  

[1.1.0] ----- 2023-01-16
 * typo in conf path /etc/dns_tools not dns_tool  
 * update CHANGELOG.md  
 * update project version  
 * Update to config search path  
 * Add /etc/dns_tool{scripts,conf.d}  
 * Config looked for in ./conf.d/config then /etc/dns_tool/conf.d/config  
 * some tidy up and fix missing_keys  
 * Installer now handles packaging, cron and config sample  
 * Add packaging  
 * Add sample config  
 * Ensure test mode for sign and key actions as well as push  
 * update CHANGELOG.md  

[1.0.0] ----- 2023-01-15
 * update project version  
 * fix standalone dns-serial-bump - now works  
 * fix installer  
 * update CHANGELOG.md  

[0.9.0] ----- 2023-01-15
 * update project version  
 * fix int_ext option in prod push  
 * install scripts in /usr/share/dns_tool  
 * prod tool new option: int_ext = int, ext or both  
 * update installer script  
 * debug off  
 * fixes  
 * Add permision/ownership set for work staging  
 * Add prod-push along with class_prod to  
 * - push from work staging to production staging (internal and external)  
 * - push from production staging to live productions (internal and external)  
 * - dns server restart capability (internal and external)  
 * begin work on class prod to help move things into production  
 * Can create certs and roll them. Can sign as well  
 * initial commit  


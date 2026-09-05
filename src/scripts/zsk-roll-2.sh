#!/usr/bin/bash
#
# Called from cron running on signing server
#
# This does following in work dir:
# - moves next key to curr 
# - sign with that curr key
# - push :
#    - from work staging to production (internal and external)
# - restart dns server 
#

echo "ZSK Roll - Phase 1" 
/usr/bin/dns-tool --zsk_roll_2

echo "Push work staging zones to production - and restart dns server"
/usr/bin/dns-prod-push --dns_restart --to_production


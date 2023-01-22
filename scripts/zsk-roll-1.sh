#!/usr/bin/bash
#
# Called from cron must be run on signing server
#
# This does following in work dir:
# - Creates second zsk key (next)
# - resign zones with both curr and next keys 
# - push from work staging zones (internal and external) to production 
# - restart dns server
#

echo "ZSK Roll - Phase 1" 
/usr/bin/dns-tool --zsk_roll_1

echo "Push work staging zones to production - and restart dns server"
/usr/bin/dns-prod-push --dns_restart --to_production

#!/usr/bin/bash
#
# This does following in work dir:
# - resign zones with curr keys
# - push staging zonefiles (internal and external) to production 
# - restart dns server
#

echo "Resign all" 
/usr/bin/dns-tool --sign

echo "Push work staging zones to prduction - and restart dns server"
/usr/bin/dns-prod-push --dns_restart --to_production


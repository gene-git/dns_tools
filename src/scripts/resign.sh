#!/usr/bin/bash
#
# This does following in work dir:
# - resign zones with curr keys
# - push staging zonefiles (internal and external) to production 
# - restart dns server
# Usage:
#       resign.sh [--serial_bump] [domain1 domain2 ... ]
# All args are optional:
#   - --serial_bump : bumps serial before signing
#   - Limit to domains given as arguments - 
#     If no domains on command line, then all domains
#     in /etc/dns_tools/conf.d/config are bumped/signed/
#

domains=()
while [[ $# -gt 0 ]]; do
  case $1 in
    -s|--serial_bump|--serial-bump)
      serial_bump="--serial_bump"
      shift
      ;;
    *)
      domains+=("$1")
      shift
      ;;
  esac
done

echo "Signing all: $serial_bump ${domains[@]}" 
/usr/bin/dns-tool $serial_bump --sign ${domains[@]}

echo "Push staging zones to production - and restart dns server"
/usr/bin/dns-prod-push --dns_restart --to_production


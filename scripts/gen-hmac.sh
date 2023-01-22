#!/usr/bin/bash
#
# Make a key for nsd shared secret - hmac-sha256
#
#
ktype="sha256"

hash=$(dd if=/dev/random of=/dev/stdout count=1 bs=32 2>/dev/null | openssl base64)

printf "name:  \"%s\"\n" '<your-name>'
printf "algorithm: hmac-%s\n" $ktype
printf "secret: \"%s\"\n" $hash


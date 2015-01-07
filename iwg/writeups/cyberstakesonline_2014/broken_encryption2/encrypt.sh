#!/bin/sh
printf "encrypt\n$1\n" | cat tok - | nc shell.cyberstakesonline.com 50091 \
   | tail -n1 | cut -d' ' -f2

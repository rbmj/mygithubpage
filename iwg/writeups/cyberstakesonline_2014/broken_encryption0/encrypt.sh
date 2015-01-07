#!/bin/sh
echo 0123456789$1 | cat tok - | nc shell.cyberstakesonline.com 50364 | tail -n1 | cut -f3 -d' ' | fold -w32

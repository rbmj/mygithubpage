#!/usr/bin/env python
import subprocess

# echo 0123456789$1 | cat tok - | nc 127.0.0.1 50364 | tail -n1 | cut -f3 -d' ' | fold -w32
def encrypt(str):
        return filter(None, subprocess.check_output(['./encrypt.sh', str]).split('\n'))

lastblock = '1' + '0'*15
flag = ''

alphabet = '`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\QWERTYUIOP{}|asdfghjkl;\'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?\t \n'

for i in range(1, 72):
        blocks = {}
        for c in alphabet:
                wouldencrypt = c + lastblock
                wouldencrypt = wouldencrypt[:-1]
                blocks[encrypt(wouldencrypt)[1]] = c
        encrypted = encrypt("A"*(13 + (i % 16)))[-1*(i // 16 + 1)]
        c = blocks[encrypted]
        lastblock = c + lastblock
        lastblock = lastblock[:-1]
        flag = c + flag

print(flag)

#!/usr/bin/env python

from Crypto.Cipher import ARC2
import itertools

def mitmFilter(plain, cipher, key):
    enc = ARC2.new(key[0], ARC2.MODE_ECB).encrypt(plain)
    dec = ARC2.new(key[1], ARC2.MODE_ECB).decrypt(cipher)
    return enc == dec

def mitmPair(plain, cipher, key):
    c = ARC2.new(key, ARC2.MODE_ECB)
    enc = c.encrypt(plain)
    dec = c.decrypt(cipher)
    return (enc, dec, key)

#alphabet H
hexchars = '0123456789abcdef'
keysize = 3 # bytes

#get keyspace K1 for sincle RC2 H^6
keyspace = (''.join(x).decode('hex') for x in
               itertools.product(hexchars, repeat=keysize*2))

plain = raw_input("Plaintext> ").decode('hex')
cipher = raw_input("Ciphertext> ").decode('hex')

pairs = (mitmPair(plain, cipher, key) for key in keyspace)
encDict = {}
decDict = {}
for pair in pairs:
    encDict[pair[0]] = pair[2]
    decDict[pair[1]] = pair[2]
keyspace = [(encDict[m], decDict[m])
            for m in encDict.viewkeys() & decDict.viewkeys()]

# while we have not narrowed the key
while len(keyspace) != 1:
    print("Keyspace of {} remaining keys".format(len(keyspace)))
    plain = raw_input("Plaintext> ").decode('hex')
    cipher = raw_input("Ciphertext> ").decode('hex')
    keyspace = [key for key in keyspace if mitmFilter(plain, cipher, key)]

key = keyspace[0]
print("Found key {}{}".format(key[0].encode('hex'), key[1].encode('hex')))
c1 = ARC2.new(key[0], ARC2.MODE_ECB)
c2 = ARC2.new(key[1], ARC2.MODE_ECB)

while True:
    cipher = raw_input("Ciphertext> ").decode('hex')
    print("Plaintext: {}".format(c1.decrypt(c2.decrypt(cipher))))

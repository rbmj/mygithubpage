#!/usr/bin/env python

import subprocess
import string

def encrypt(str):
        return filter(None, subprocess.check_output(['./encrypt.sh', str]))

def getPad(s):
	pad = chr(128)
	pad_len = 1
	base_len = len(encrypt(s + pad))
	x = base_len
	while x == base_len:
		pad = pad + chr(128+pad_len)
		x = len(encrypt(s + pad))
		pad_len = pad_len + 1
	return pad
		

def encryptWithPad(s, pad):
	return encrypt(s + pad[len(s):])

alphabet = list(string.printable)
alphabet.remove('%')
alphabet.remove('\n')

def main():
	#msgpad = ''.join([chr(128+x) for x in range(41)]) # max pad
	candidates = ['key'] # seed string
	newcandidates = []
	smallest = None
	for i in range(70):
		for candidate in candidates:
			msgpad = getPad(candidate)
			for c in alphabet:
				plain = candidate + c
				cipher = encrypt(plain + msgpad[1:])
				if smallest is None:
					smallest = len(cipher)
					newcandidates = [plain]
				elif len(cipher) < smallest:
					smallest = len(cipher)
					newcandidates = [plain]
				elif len(cipher) == smallest:
					newcandidates.append(plain)
		candidates = newcandidates
		newcandidates = []
		smallest = None
		print(candidates)

if __name__ == '__main__':
	main()


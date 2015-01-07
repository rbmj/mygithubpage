#!/usr/bin/env python

import subprocess
import string

def encrypt(str):
        return filter(None, subprocess.check_output(['./encrypt.sh', str]))

alphabet = list(string.printable)
alphabet.remove('%')
alphabet.remove('\n')

def main():
	candidates = ['key'] # seed string
	newcandidates = []
	smallest = None
	for i in range(70):
		for candidate in candidates:
			for c in alphabet:
				plain = candidate + c
				cipher = encrypt(plain)
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


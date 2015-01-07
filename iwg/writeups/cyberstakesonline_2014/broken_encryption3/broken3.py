#!/usr/bin/env python

import socket
import string
import sys
alphabet = list(string.printable)
alphabet.remove('\n')

def splitN(line, n):
	return [line[i:i+n] for i in range(0, len(line), n)]

def guess(guess_str, n):
	pad = "A"*(15 - (n % 16))
	token = "828C2EE84B\n"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('shell.cyberstakesonline.com', 50103))

	# recieve auth token prompt
	s.recv(1024)
	s.send(token)
	# recieve authenticated message
	s.recv(1024)
	# receive prompt
	s.recv(1024)
	s.send("A"*16 + pad + '\n')
	#print(list("A"*16 + pad))
	c1 = splitN(s.recv(1024).split('\n')[2], 32)
	block_num = n // 16
	old_iv = c1[block_num].decode('hex')
	ciphertext = c1[block_num + 1].decode('hex')
	new_iv = c1[-1].decode('hex')
	payload = ''.join(chr(ord(o) ^ ord(n) ^ ord(g))
		for (o, n, g) in zip(old_iv, new_iv, guess_str))
	if '\n' in payload:
		pass #print("ERROR: PAYLOAD HAS NEWLINE FOR c=%s" % guess[-1])
	s.send(payload + '\n')
	#print(list(payload))
	c2 = splitN(s.recv(1024).split('\n')[2], 32)
	ciphertext_guess = c2[0].decode('hex')
	s.close()
	return ciphertext_guess == ciphertext


def main():
	last_fifteen = "A"*15
	flag = ''
	start = 0
	if len(sys.argv) > 1:
		flag = sys.argv[1]
		last_fifteen = "A"*15 + flag
		last_fifteen = last_fifteen[-15:]
		start = len(flag)
	for i in range(start, 16*4):
		matched = False
		while not matched:
			for c in alphabet:
				if guess(last_fifteen + c, i):
					last_fifteen = (last_fifteen + c)[1:]
					flag = flag + c
					matched = True
					break
	print(flag)

if __name__ == '__main__':
	main()


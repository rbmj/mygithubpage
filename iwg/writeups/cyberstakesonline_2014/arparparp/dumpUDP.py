#!/usr/bin/env python
# File dumpUDP.py
import scapy.all as scapy
import sys

pcap_file = sys.argv[1]
mac = sys.argv[2]

print(''.join(
    p[scapy.UDP].load
        for p in scapy.PcapReader(pcap_file)
        if p[scapy.Ether].src == mac and scapy.UDP in p
    )
)


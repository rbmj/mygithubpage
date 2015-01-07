ARPARPARP
=========

Find the secret message the arp-spoofers are trying to block. pcap 
available here (link).

Hints:
 - Wireshark and Scapy are both appropriate tools for this job
 - One of the senders is trying to give you the key; filter out the rest

Writeup
--------

Opening up the pcap in wireshark, you can see that there are multiple
different MAC addresses all claiming the ip address 192.168.2.10 trying
to send data to 192.168.2.9.  The data is transfered using UDP.  So, we'll
write a quick script that will let us dump all the UDP data from a given
MAC address:

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

Now, we can just check what each MAC is sending:

    $ ./dumpUDP.py arparparp.pcap 54:be:f7:51:9b:01
    `=n!t~]WJ$#j3yOCp<2`A&1c+28c
    $ ./dumpUDP.py arparparp.pcap 54:be:f7:51:9b:02
    "AU&?BtL6NDG;N>@caeD?C)!nUhLMi
    $ ./dumpUDP.py arparparp.pcap 54:be:f7:51:9b:03
    Your key is db3lmtz26s540twf

Found it!

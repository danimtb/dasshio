#!/usr/bin/env python3

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff
from scapy.all import ARP


def arp_display(pkt):
    if pkt[ARP].psrc == '0.0.0.0':
        print(pkt[ARP].hwsrc)

# start sniffing
print('Happy sniffing! MAC addresses:')
sniff(prn=arp_display, filter='arp', store=0, count=0)

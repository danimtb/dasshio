#!/usr/bin/env python3

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff
from scapy.all import ARP
import requests


def arp_display(pkt):
    #if pkt[ARP].psrc == '0.0.0.0':
    r = requests.get("http://api.macvendors.com/" + pkt[ARP].hwsrc)
    print(r.text)
    print(pkt[ARP].hwsrc, pkt[ARP].psrc, pkt[ARP].pdst)

# start sniffing
print('Happy sniffing! MAC addresses:')
sniff(prn=arp_display, filter='arp', store=1, count=0)

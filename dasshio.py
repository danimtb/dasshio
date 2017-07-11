#!/usr/bin/env python3

import json
import logging
import os
import requests
from scapy.all import sniff
from scapy.all import ARP
import sys


def arp_display(pkt):
    mac = pkt[ARP].hwsrc.lower()
    if mac in [button['address'].lower() for button in config['buttons']]:
        idx = [button['address'].lower() for button in config['buttons']].index(mac)
        button = config['buttons'][idx]

        logging.info(button['name'])
        print(button['name'], mac, "pressed!")
        print("REQUEST!!!", button['url'])
        r = requests.post(button['url'], json=json.loads(button['body']), headers=json.loads(button['headers']))
        logging.info('Status Code: {}'.format(r.status_code))


# create basepath
path = os.path.dirname(os.path.realpath(__file__))

# log events in stdout and log file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setFormatter(format)
logger.addHandler(stdoutHandler)

fileHandler = logging.FileHandler(path + '/dasshio.log', 'w')
fileHandler.setFormatter(format)
logger.addHandler(fileHandler)

# read config file
print("Opening json file...")
with open(path + '/data/options.json', mode='r') as data_file:
    config = json.load(data_file)

# start sniffing
print("Starting sniffing...")
sniff(prn=arp_display, filter='arp', store=0, count=0)

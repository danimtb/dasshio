#!/usr/bin/env python3

import json
import logging
import os
import requests
from scapy.all import sniff
from scapy.all import ARP
from scapy.all import UDP
from scapy.all import IP
from scapy.all import DHCP
from scapy.all import Ether
import sys
import time
import signal
import re

def signal_handler(signal, frame):
    sys.exit(0)

def arp_display(pkt):
    mac = ""

    try:
        mac = pkt[ARP].hwsrc.lower()
    except:
        mac = pkt[Ether].src.lower()

    for button in config['buttons']:
        if mac == button['address'].lower():

            idx = [button['address'].lower() for button in config['buttons']].index(mac)
            button = config['buttons'][idx]

            logging.info(button['name'] + " button pressed!")
            logging.info("Request: " + button['url'])
            
            try:
                request = requests.post(button['url'], json=json.loads(button['body']), headers=json.loads(button['headers']))
                logging.info('Status Code: {}'.format(request.status_code))
                
                if request.status_code == requests.codes.ok:
                    logging.info("Successful request")
                else:
                    logging.error("Bad request")
            except:
                logging.exception("Unable to perform  request: Check url, body and headers format. Check API password")

            return True

# Catch SIGINT/SIGTERM Signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
    
# Remove Scapy IPv6 warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Create basepath
path = os.path.dirname(os.path.realpath(__file__))

# Log events to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
stdoutHandler.setFormatter(formater)

logger.addHandler(stdoutHandler)

# Read config file
logging.info("Reading config file: /data/options.json")

with open(path + '/data/options.json', mode='r') as data_file:
    config = json.load(data_file)

# Check config parameters
cpt = 0
error = 0
for button in config['buttons']:
    cpt = cpt + 1
    if ('address' not in button) or (not button['address']) or (not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", button['address'].lower())):
        logging.info("Parameter error for button " + str(cpt) + " : address is not valid")
        error = error + 1
    for value in ('name', 'url'):
        if (value not in button) or (not button[value]) or (button[value] == 'null'):
            logging.info("Parameter error for button " + str(cpt) + " : " + value + " is null")
            error = error + 1
    for value in ('body', 'headers'):
        if (value not in button) or (not button[value]):
            button[value] = '{}'
if error != 0:
    logging.info("Exiting ...")
    sys.exit(0)
    
while True:
    # Start sniffing
    logging.info("Starting sniffing...")
    sniff(stop_filter=arp_display, filter='arp or (udp and src port 68 and dst port 67 and src host 0.0.0.0)', store=0, count=0)
    logging.info("Packet captured, waiting 20s ...")
    time.sleep(20)

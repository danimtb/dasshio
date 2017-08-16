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

    for button in config['buttons']:
        if mac == button['address'].lower() and guard[button['address']] == False:

            guard[button['address']] = True

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
            finally:
                guard[button['address']] = False


# Create basepath
path = os.path.dirname(os.path.realpath(__file__))

# Log events to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdoutHandler.setFormatter(formater)

logger.addHandler(stdoutHandler)


# Read config file
logging.info("Reading config file: /data/options.json")

with open(path + '/data/options.json', mode='r') as data_file:
    config = json.load(data_file)

#Create Guard dict to avoid multiple requests with a single press and set to false for all buttons
guard = dict()

for button in config['buttons']:
    guard[button['address']] = False

# Start sniffing
logging.info("Starting sniffing...")
sniff(prn=arp_display, filter='arp', store=0, count=0)

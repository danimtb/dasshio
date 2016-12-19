#!/usr/bin/env python3

# http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/
# crontab -e
# @reboot   source /PATH/TO/REPO/.venv/bin/activate && python /PATH/TO/REPO/button.py

# Exit daemon:
# find number: ps aux | grep "button.py"
# kill process: sudo kill 61604

import json
import logging
from daemonize import Daemonize
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff
from scapy.all import ARP
import requests
import os

def arp_display(pkt):
    mac = pkt[ARP].hwsrc
    if mac in [button['address'] for button in config['buttons']]:
        idx = [button['address'] for button in config['buttons']].index(mac)
        button = config['buttons'][idx]

        logging.info(button['name'])
        r = requests.post(button['url'], json=button['body'], headers=button['headers'])
        logging.info('status code: {}'.format(r.status_code))

def main():
    sniff(prn=arp_display, filter='arp', store=0, count=0)

# create basepath
path = os.path.dirname(os.path.realpath(__file__))

# log events in log file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
fh = logging.FileHandler(path + '/button.log', 'w')

# read config file
with open(path + '/config.json', mode='r') as data_file:
    config = json.load(data_file)

# start sniffing
daemon = Daemonize(
    app='dashbutton',
    pid='{}/button.pid'.format(path),
    action=main)
daemon.start()

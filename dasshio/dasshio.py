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

    for button in config["buttons"]:
        if mac == button["address"].lower():

            idx = [button["address"].lower()
                   for button in config["buttons"]].index(mac)
            button = config["buttons"][idx]

            logging.info(button["name"] + " button pressed!")

            url_request = ""

            if "url" in button:
                url_request = button["url"]
            else:
                url_request = "http://hassio/homeassistant/api/services/{0}/{1}".format(
                    button["domain"].lower(), button["service"].lower())

            logging.info("Request: " + url_request)

            try:
                if "url" in button:
                    request = requests.post(url_request, json=json.loads(
                        button["body"]), headers=json.loads(button["headers"]))
                else:
                    request = requests.post(url_request, json=json.loads(
                        button["service_data"]), headers={'x-ha-access': os.environ.get('HASSIO_TOKEN')})

                logging.info("Status Code: {}".format(request.status_code))

                if request.status_code == requests.codes.ok:
                    logging.info("Successful request")
                else:
                    logging.error("Bad request")
            except:
                logging.exception(
                    "Unable to perform  request: Check [url], [body], [headers] and API password or\
                     [domain], [service] and [service_data] format.")

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

with open(path + "/data/options.json", mode="r") as data_file:
    config = json.load(data_file)

# Check config parameters
button_counter = 0
error = False

for button in config["buttons"]:
    button_counter = button_counter + 1
    if ("address" not in button) or (not button["address"]) or (not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", button["address"].lower())):
        logging.error("Parameter error for button " +
                     str(button_counter) + ": [address] is not valid")
        error = True

    if ("name" not in button) or (not button["name"]) or (button["name"] == "null"):
        logging.error("Parameter error for button " +
                     str(button_counter) + ": [name] is null")
        error = True

    if not ("url" and "body" and "headers") in button and not ("domain" and "service" and "service_data") in button:
        logging.error("Parameter error for button " + str(button_counter) + ": No config [url], [body], [headers] or [domain], [service], [service_data] provided")
        error = True

    if ("url" and "body" and "headers") in button:
        for value in ("url", "body", "headers"):
            if (value not in button) or (not button[value]):
                if value is "url":
                    logging.error("Parameter error for button " + str(button_counter) + ": No [url] provided")
                    error = True
                button[value] = "{}"

    if ("domain" and "service" and "service_data") in button:
        for value in ("domain", "service", "service_data"):
            if (value not in button) or (not button[value]):
                if value is "domain" or "service":
                    logging.error("Parameter error for button " +
                                  str(button_counter) + ": No [domain] or [service] provided")
                    error = True
                button[value] = "{}"

if error:
    logging.info("Exiting...")
    sys.exit(0)


while True:
    # Start sniffing
    logging.info("Starting sniffing...")
    try:
        sniff(stop_filter=arp_display,
              filter="arp or (udp and src port 68 and dst port 67 and src host 0.0.0.0)",
              store=0,
              count=0)
    except(OSError):
        pass
    timeout = config["timeout"]
    logging.info("Packet captured, waiting " + str(timeout) + "s ...")
    time.sleep(timeout)

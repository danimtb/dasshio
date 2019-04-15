#!/usr/bin/env python3

import json
import logging
import os
import re
import requests
import signal
import sys
import time

from datetime import datetime
from scapy.all import ARP
from scapy.all import DHCP
from scapy.all import Ether
from scapy.all import IP
from scapy.all import UDP
from scapy.all import sniff


BASE_URL = os.environ.get("HA_BASE_URL") or "http://hassio/homeassistant"


def signal_handler(signal, frame):
    logger.warning("Caught signal: %s" % signal)
    logger.info("Exiting...")
    sys.exit(0)


def arp_display(pkt):
    mac = ""
    current_time = datetime.utcnow()
    button_timeout = int(config["timeout"]) if "timeout" in config else 10
    request_timeout_secs = int(config["request_timeout_secs"]) if "request_timeout_secs" in config else 2

    try:
        mac = pkt[ARP].hwsrc.lower()
    except:
        mac = pkt[Ether].src.lower()

    for button in config["buttons"]:
        button_address = button["address"].lower()
        if mac == button_address:
            logger.info(button["name"] + " button pressed!")

            url_request = ""

            if "url" in button:
                url_request = button["url"]
            else:
                url_request = BASE_URL + "/api/services/{0}/{1}".format(
                    button["domain"].lower(), button["service"].lower())

            try:
                if "url" in button:
                    request = requests.post(url_request,
                        json=json.loads(
                        button["body"]), headers=json.loads(button["headers"]),
                        timeout=request_timeout_secs
                    )
                    logger.info("Request: " + url_request + " - body: " + button["body"])
                else:
                    auth_header = "Bearer " + os.environ.get('HASSIO_TOKEN')
                    request = requests.post(url_request,
                        json=json.loads(button["service_data"]),
                        headers={'Authorization': auth_header},
                        timeout=request_timeout_secs
                    )
                    logger.info("Request: " + url_request + " - body: " + button["service_data"])

                logger.info("Status Code: {}".format(request.status_code))

                if request.status_code == requests.codes.ok:
                    logger.info("Successful request")
                else:
                    logger.error("Bad request")
            except:
                logger.exception(
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

logFormatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
stdoutHandler.setFormatter(logFormatter)

logger.addHandler(stdoutHandler)

# Read config file
logger.info("Reading config file: /data/options.json")

with open(path + "/data/options.json", mode="r") as data_file:
    config = json.load(data_file)

# Check config parameters
button_counter = 0
error = False

for button in config["buttons"]:
    button_counter = button_counter + 1
    if ("address" not in button) or (not button["address"]) or (not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", button["address"].lower())):
        logger.error("Parameter error for button " +
                     str(button_counter) + ": [address] is not valid")
        error = True

    if ("name" not in button) or (not button["name"]) or (button["name"] == "null"):
        logger.error("Parameter error for button " +
                     str(button_counter) + ": [name] is null")
        error = True

    if not ("url" and "body" and "headers") in button and not ("domain" and "service" and "service_data") in button:
        logger.error("Parameter error for button " + str(button_counter) + ": No config [url], [body], [headers] or [domain], [service], [service_data] provided")
        error = True

    if ("url" and "body" and "headers") in button:
        for value in ("url", "body", "headers"):
            if (value not in button) or (not button[value]):
                if value is "url":
                    logger.error("Parameter error for button " + str(button_counter) + ": No [url] provided")
                    error = True
                button[value] = "{}"

    if ("domain" and "service" and "service_data") in button:
        for value in ("domain", "service", "service_data"):
            if (value not in button) or (not button[value]):
                if value is "domain" or "service":
                    logger.error("Parameter error for button " +
                                  str(button_counter) + ": No [domain] or [service] provided")
                    error = True
                button[value] = "{}"

if error:
    logger.info("Exiting...")
    sys.exit(0)


logger.info("Starting...")
while True:
    # Start sniffing
    logger.info("Starting sniffing...")
    try:
        sniff(stop_filter=arp_display,
              filter="arp or (udp and src port 68 and dst port 67 and src host 0.0.0.0)",
              store=0,
              count=0)
    except OSError as err:
        logger.warning("OS error: {0}".format(err))
        pass
    except Exception as e:
        logger.exception("Caught exception in sniff: %s" % e)
        pass
    except SystemExit:
        raise
    except:
        logger.exception("Unexpected exception")
        raise
    finally:
        logger.info("Finishing sniffing")

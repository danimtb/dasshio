#!/usr/bin/env python3

import json
import logging
import os
import re
import requests
import signal
import sys
import time
import datetime
import socket
import struct
import binascii
import json

BASE_URL = os.environ.get("HA_BASE_URL") or "http://hassio/homeassistant"

def signal_handler(signal, frame):
    logger.warning("Caught signal: %s" % signal)
    logger.info("Exiting...")
    sys.exit(0)

def arp_display(mac):
    if mac == "":
        return
    current_time = datetime.datetime.now(datetime.timezone.utc)

    # logger.info(mac)
    for button in config["buttons"]:
        button_address = button["address"].lower().replace(":","")
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
            logging.info("Button pressed! Waiting %s seconds..." % str(timeout))
            time.sleep(timeout)
            logging.info("Listening again...")
            return True

# Catch SIGINT/SIGTERM Signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
logger.info("Reading config file:" + path + "/data/options.json")

with open(path + "/data/options.json", mode="r") as data_file:
    config = json.load(data_file)
timeout = int(config["timeout"]) if "timeout" in config else 10
request_timeout_secs = int(config["request_timeout_secs"]) if "request_timeout_secs" in config else 2

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

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
logger.info("Starting sniffing...")
while True:
    try:
        packet = rawSocket.recvfrom(2048)
        ethernet_header = packet[0][0:14]
        ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
        # skip non-ARP packets
        ethertype = ethernet_detailed[2]
        if ethertype != b'\x08\x06':
            continue
        arp_header = packet[0][14:42]
        arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
        source_mac = str(binascii.hexlify(arp_detailed[5]), 'utf-8')
        source_ip = socket.inet_ntoa(arp_detailed[6])
        dest_ip = socket.inet_ntoa(arp_detailed[8])
        arp_display(source_mac)
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

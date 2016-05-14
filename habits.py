import json
import sys
import time
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scapy.all import *

AMAZON_DASH_MAC_ADDRESS = 'YOUR_DASH_MAC_ADDY_HERE';  # Make sure letters in the address are lower-case
GDOCS_OAUTH_JSON       = 'google-sheets-creds.json'
GDOCS_SPREADSHEET_NAME = 'YOUR_SPREADSHEET_NAME'
# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30

def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        json_key = json.load(open(oauth_key_file))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)

        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

def record_exercise():
    # data = {
    #     "Timestamp": time.strftime("%Y-%m-%d %H:%M"),
    #     "Measurement": 'You did a fitness'
    # }

    time = datetime.datetime.now()
    activity = "You did a fitness"
    worksheet.append_row((time, activity))

def arp_display(pkt):
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    if pkt.haslayer(ARP): # Needed for Raspberry Pi
        if pkt[ARP].op == 1: #who-has (request)
            if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
                if pkt[ARP].hwsrc == AMAZON_DASH_MAC_ADDRESS: # Bounty
                    print "Pushed Bounty"
                    record_exercise()
                else:
                    print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

# print sniff(prn=arp_display, filter="arp", store=0, count=0)

print('Logging Amazon Dash Button presses to {0}.'.format(GDOCS_SPREADSHEET_NAME))
print('Press Ctrl-C to quit.')
worksheet = None

# Login if necessary.
if worksheet is None:
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

# # Append the data in the spreadsheet, including a timestamp
# try:
#     worksheet.append_row((datetime.datetime.now(), "exercise"))
#     # record_exercise(worksheet)
# except:
#     # Error appending data, most likely because credentials are stale.
#     # Null out the worksheet so a login is performed at the top of the loop.
#     print('Append error, logging in again')
#     worksheet = None

print sniff(prn=arp_display, filter="arp", store=0, count=0) # Another Raspberry Pi specific thing - count=0 so that it doesn't quit

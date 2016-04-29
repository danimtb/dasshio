# Amazon Dash Hack with the Raspberry Pi

Sources & Inspiration:
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)
- [Reddit Home Automation](https://www.reddit.com/r/homeautomation/comments/3gy2u7/help_with_python_and_scapy_amazon_button_on_pi/)
- [Start script on boot](https://alwaystinkering.wordpress.com/2015/09/22/amazon-dash-button-automation/)
- [Using Python and Scapy to sniff for ARP on Pi](http://unix.stackexchange.com/questions/223255/using-python-and-scapy-to-sniff-for-arp-on-pi)
- [Access google sheets in python using Gspread](http://www.indjango.com/access-google-sheets-in-python-using-gspread/)
- [**Adafruit Humidity Sensor logging to Google Spreadsheet**](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging?view=all)

## Stuff to install on Raspberry Pi's Debian

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install tcpdump python-scapy
```

## Initial 'Listen' script from the initial article
Customized so it can work on Raspberry Pi. Fixes the "IndexError: Layer [ARP] not found" error. Main edits are line 3, `if pkt.haslayer(ARP):` and last line, `count=0` so that it runs forever.

```
from scapy.all import *

def arp_display(pkt):
  if pkt.haslayer(ARP):
    if pkt[ARP].op == 1: #who-has (request)
      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
        print "ARP Probe from: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=0)
```

## Let's try posting directly to Google Sheets without Cloudstich shenanigans

```py
import json
import sys
import time
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scapy.all import *

AMAZON_DASH_MAC_ADDRESS = '';
GDOCS_OAUTH_JSON       = ''
GDOCS_SPREADSHEET_NAME = ''
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
    worksheet.append_row(time, activity)

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


```

## Notes about going DIY

- It's a bit harder, as you might imagine, but quite valuable in picking up some python and knowledge about how to fix code that is outdated or no longer supported, and adapting to API updates
- Google changed their oauth2client.client since the Adafruit docs were written about logging info to Google Sheets, so need to update cpde fpr that as well. (`from oauth2client.client import SignedJwtAssertionCredentials` to `from oauth2client.service_account import ServiceAccountCredentials` [Discussion](https://github.com/burnash/gspread/pull/356) and [Updated docs](https://github.com/burnash/gspread/pull/356/files)
- Will need to [update Raspberry Pi to Python 2.7.3 to  2.7.9](http://raspberrypi.stackexchange.com/questions/26286/update-python-version-on-raspbian) to get rid of gspread InsecurePlatformWarning
  - `wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz`
  - [Source](http://stackoverflow.com/questions/29134512/insecureplatformwarning-a-true-sslcontext-object-is-not-available-this-prevent)
- Had to reinstall a bunch of things after building Python 2.7.9 from source...  python-pkg-resources
- Easier to just [update Raspberry Pi Debian Wheezy to Jessie](http://raspberrypi.stackexchange.com/questions/27858/upgrade-to-raspbian-jessie) - It has Python 2.7.9 by default
```sh
sudo apt-get install --reinstall python-pkg-resources

```

```
gunzip Python-2.7.9.tgz
tar -xvf Python-2.7.9.tar
cd Python-2.7.9/
./configure
make
sudo make install
python -V # check version to see that it took
```

## Running a Python Script on boot

<http://raspberrypi.stackexchange.com/questions/4123/running-a-python-script-at-startup>

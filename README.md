# Amazon Dash Hack with the Raspberry Pi

Sources & Inspiration:
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)
- [Reddit Home Automation](https://www.reddit.com/r/homeautomation/comments/3gy2u7/help_with_python_and_scapy_amazon_button_on_pi/)
- [Start script on boot](https://alwaystinkering.wordpress.com/2015/09/22/amazon-dash-button-automation/)
- [Using Python and Scapy to sniff for ARP on Pi](http://unix.stackexchange.com/questions/223255/using-python-and-scapy-to-sniff-for-arp-on-pi)
- [Access google sheets in python using Gspread](http://www.indjango.com/access-google-sheets-in-python-using-gspread/)
- [**Adafruit Humidity Sensor logging to Google Spreadsheet**](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging?view=all)

## Why Use the Raspberry Pi?

The Amazon Dash Button hack typically works using a python script that listens for the button's [ARP Probe](https://en.wikipedia.org/wiki/Address_Resolution_Protocol#ARP_probe). If you want to use the button long-term, you'll want to script to auto-start and be running constantly, and since I'm a techno-hippie, I'd like to use as little power as possible. Enter, the Raspberry Pi, which only uses 2-5 Watts.

## Stuff to install on Raspberry Pi's Debian

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install tcpdump python-scapy
```

Get Python Pip and install gspread and oauth2client:

```sh
sudo apt-get update
sudo apt-get install python-pip
sudo pip install gspread oauth2client
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

### Run the script

```sh
sudo python habits.py
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

## Running a Python Script on-boot with a cron job

Source: [Running A Python Script At Boot Using Cron](http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/)

### Install Crontab on OSMC

```sh
sudo apt-get update
sudo apt-get install cron
```

### Edit root's crontab

```sh
sudo crontab -e
```

Add this to the end of it (no need for sudo since it's already root's crontab): `@reboot python /home/osmc/scripts/habits.py &`

### Check that root is actually running the script

```sh
ps aux | grep /home/osmc/scripts/habits.py
```

Look for `root       252 10.9  2.3  20260 18008 ?        S    16:08   0:03 python /home/osmc/scripts/habits.py`

If you need to kill the script/job, run `sudo kill 252`

[Other options](http://raspberrypi.stackexchange.com/questions/4123/running-a-python-script-at-startup)

## Blocking Amazon Dash Phone Notifications

You'll probably receive annoying notifications on your phone asking you to complete the setup process. To prevent these notifications, you'll need to block the Amazon Dash Button from reaching the internet by tweaking your router settings.

# Amazon Dashbutton Hack with Python daemon

Sources & Inspiration:
- [Raspberry Pi script](https://github.com/vancetran/amazon-dash-rpi)
- [Maddox Dashbutton Repo](https://github.com/maddox/dasher)
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)

## Installation

```sh
git clone https://github.com/JulianKahnert/amazon-dashbutton.git
cd amazon-dashbutton
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Now you have everything you need to run this daemon. Some changes in `config.json` (compatible with [Maddox Dasher config](https://github.com/maddox/dasher)) should do the rest.

More requirements:
```sh
# macOS
brew install libnet

# linux
apt install libnet

# FreeBSD
pkg install libnet
```

## Test setup
Test your workflow with the `find_button.py` sniffing script.
```sh
source .venv/bin/activate
python find_button.py
```

## Run the daemon

```sh
source .venv/bin/activate
python button.py
```

## Stop the daemon

```sh
ps aux | grep "button.py"

# find process ID (pid)
ps aux | grep "button.py"

# kill the process
sudo kill 52324
```

### Start after reboot
... add a crontab

```sh
crontab -e

# add the following line as a cronjob (change "/PATH/TO/REPO/")
@reboot   source /PATH/TO/REPO/.venv/bin/activate && python /PATH/TO/REPO/button.py
```

## Blocking Amazon Dash Phone Notifications

You'll probably receive annoying notifications on your phone asking you to complete the setup process. To prevent these notifications, you'll need to block the Amazon Dash Button from reaching the Internet by tweaking your router settings.

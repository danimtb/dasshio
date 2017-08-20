# Dasshio - Amazon Dash Buttons Hass.io add-on

[Hass.io add-on](https://home-assistant.io/addons/) to easily use [Amazon Dash Buttons](https://en.wikipedia.org/wiki/Amazon_Dash) with [Home Assistant](https://home-assistant.io).

## Description: How dasshio works
This is a python script used to scan wifi devices connected to your network  (using ARP). If a device matches any MAC address of the options, it will perform a HTTP POST request to the url given with headers and body indicated.

## Usage
You can use this add-on to do whatever you like following the description above. However, the purpose of dasshio is to "integrate" [Amazon's Dash buttons](https://en.wikipedia.org/wiki/Amazon_Dash) in Home Assistant in an easy way with [Hass.io.](https://home-assistant.io/hassio/).

See [RESTful API Post Services](https://home-assistant.io/developers/rest_api/#post-apiservicesltdomainltservice) documentation to see what you can do.

Examples:

- Set a Dash Button to toggle **room_light** light:
  - url: *http://home_assistant_IP:8123/api/services/light/toggle*
  - body: "*{\"entity_id\": \"light.room_light\"}*"
- Set a Dash Button to activate a **welcome_home** script:
  - url: *http://home_assistant_IP:8123/api/services/script/welcome_home*
  - body: ""
 
 Have a look at [Service calls](https://home-assistant.io/docs/scripts/service-calls/) to know what services you can use and what you can do with them.


## How to install this Hass.io add-on
To install this add-on, please, follow Home Assistant documentation on how to [Install Third-party Add-ons](https://home-assistant.io/hassio/installing_third_party_addons/)

## Options example
Here it is an example of a Dash Gillette used to toggle a light. Note you can add as many buttons as you like inside the "buttons" array.

 - name: name of your device
 - address: MAC of tour device
 - url: Url to perform the HTPP Post request (http or https). Check [Home Assistant RESTful API](https://home-assistant.io/developers/rest_api/).
 - headers: HTTP Post headers (Useful for Home Assistant API password -see example-).
 - body: HTTP Post Body (Normally the *entity_id* in Home Assistant)

[*/data/options.json*](https://home-assistant.io/developers/hassio/addon_config/#options--schema)
```
{
  "buttons": [
  {
    "name": "Gillette",
    "address": "AC:63:BE:77:C4:0D",
    "url": "http://home_assistant_IP:8123/api/services/light/toggle",
    "headers": "{\"x-ha-access\": \"your_password\"},
    "body": "{\"entity_id\": \"light.room_light\"}"
  },
  {
    "name": "Bounty",
    "address": "AC:63:BE:77:C4:0C",
    "url": "http://home_assistant_IP:8123/api/services/script/welcome_home",
    "headers": "{\"x-ha-access\": \"your_password\"},
    "body": ""
  }]
}
```

**WARNING**: As headers and body sections have to be strings, it is necessary to use slashes ( */* ) berore double quotes ( *"* ) to escape them. Like this:  *\"*

## How to find the MAC address of your Dash
At the moment, the best way to do this is to access your Wifi Router and check the MAC addresses of the historial of connected devices. Then, copy and paste the MAC in a service like [MA:CV:en:do:rs](https://macvendors.com/) to find the Vendor of that device. The Amazon Dash button vendor should be: *Amazon Technologies Inc.*

---------------------
### Credit
- [amazon-dashbutton](https://github.com/JulianKahnert/amazon-dashbutton) (Thanks to [JulianKahnert](https://github.com/JulianKahnert) in [Issue#1](https://github.com/danimtb/dasshio/issues/1))

### Sources & Inspiration:
- [Raspberry Pi script](https://github.com/vancetran/amazon-dash-rpi)
- [Maddox Dashbutton Repo](https://github.com/maddox/dasher)
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)

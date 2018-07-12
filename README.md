# Dasshio - Amazon Dash Buttons Hass.io add-on

[Hass.io add-on](https://home-assistant.io/addons/) to use [Amazon Dash Buttons](https://en.wikipedia.org/wiki/Amazon_Dash) in [Home Assistant](https://home-assistant.io).

## Description: How dasshio works

This is a python script used to scan Wi-Fi devices connected to your network (using ARP and UDP). If a device matches any MAC address of the options, it will perform a HTTP POST request to the Home Assistant API.

## Usage

The purpose of Dasshio is to "integrate" [Amazon's Dash buttons](https://en.wikipedia.org/wiki/Amazon_Dash) in Home Assistant in an easy way with [Hass.io](https://home-assistant.io/hassio/).

See [RESTful API Post Services](https://home-assistant.io/developers/rest_api/#post-apiservicesltdomainltservice) documentation to see what you can do.

Examples:

- Set a Dash Button to toggle **room_light** light:
  - domain: *light*
  - service: *toggle*
  - service_data: *{\\"entity_id\\": \\"light.room_light\\"}*
- Set a Dash Button to activate a **welcome_home** script:
  - domain: *script*
  - service: *welcome_home*
  - service_data: *{}*

Have a look at [Service calls](https://home-assistant.io/docs/scripts/service-calls/) to know what services you can use and what you can do with them.

## How to install this Hass.io add-on

To install this add-on, please, follow Home Assistant documentation on how to [Install Third-party Add-ons](https://home-assistant.io/hassio/installing_third_party_addons/)

## Options example: domain, service, service_data

Here it is an example of a Dash Gillette button used to toggle a light and a Dash Bounty to call a script. Note you can add as many buttons as you like inside the "buttons" array.

- name: name of your device
- address: MAC of your device
- domain: Home Assistant domain (`light`, `switch`, `script`, `automation`...). Check [Home Assistant RESTful API](https://home-assistant.io/developers/rest_api/).
- service: Home Assistant service.
- service_data: Home Assistant service data to call the service (Optional).

[*/data/options.json*](https://home-assistant.io/developers/hassio/addon_config/#options--schema)

```json
{
  "timeout": 20,
  "buttons": [
  {
    "name": "Gillette",
    "address": "AC:63:BE:77:C4:0D",
    "domain": "light",
    "service": "toggle",
    "service_data": "{\"entity_id\": \"light.room_light\"}"
  },
  {
    "name": "Bounty",
    "address": "AC:63:BE:77:C4:0C",
    "domain": "script",
    "service": "welcome_home",
    "service_data": "{}"
  }]
}
```

**Note**: Dasshio uses `http://hassio/homeassistant/api/services/{domain}/{service}` as the base url to route requests over the Hassio local network between the containers. This is the prefered method as it means the requests don't have to leave the machine Hassio is running on (See [Hass.io Addon Communication](https://home-assistant.io/developers/hassio/addon_communication/#home-assistant)).

**WARNING**: As headers and body sections have to be strings, it is necessary to use backslashes ( *\\* ) before double quotes ( *"* ) to escape them. Like this:  *\\"*

## Options: url, body, headers

Another possibility would be to use Dasshio to perform a HTTP Post request to an URL outside Home Assistant. To do so you can use the configuration below.

- name: name of your device
- address: MAC of your device
- url: Url to perform the HTPP Post request (http or https). Check [Home Assistant RESTful API](https://home-assistant.io/developers/rest_api/).
- headers: HTTP Post headers (Useful for Home Assistant API password -see example-).
- body: HTTP Post Body (Normally the *entity_id* in Home Assistant)

[*/data/options.json*](https://home-assistant.io/developers/hassio/addon_config/#options--schema)

```json
{
  "timeout": 20,
  "buttons": [
  {
    "name": "Gillette",
    "address": "AC:63:BE:77:C4:0D",
    "url": "http://httpbin.org/post",
    "headers": "{}",
    "body": "{\"payload\": \"This is an HTTP Post request!\"}"
  },
  {
    "name": "Bounty",
    "address": "AC:63:BE:77:C4:0C",
    "url": "http://hassio/homeassistant/api/services/script/welcome_home",
    "headers": "{}",
    "body": "{}"
  }]
}
```

**Note**: As described above, you can still use `http://hassio/homeassistant/api` to route requests over the Hassio local network and perform API calls to Home Assistant. You can see [Hass.io Addon Communication](https://home-assistant.io/developers/hassio/addon_communication/#home-assistant) for more information.

## Options: timeout

By default Dasshio waits 20 seconds after a button press before resuming, this is to avoid detecting duplicate button presses. This option allows you to change this delay, if you want more responsive buttons then decrease this value and increase it if you experience duplicate presses.

## How to find the MAC address of your Dash

At the moment, the best way to do this is to hold down the button for 6 seconds, disconnect from the current Wi-Fi and connect to the *Amazon ConfigureMe* SSID.  If prompted, "stay connected" and open web page **192.168.0.1**. You will see your button’s ‘about’ page with the MAC and the additional information.

Alternatively, you can access your Wi-Fi Router and check the MAC addresses in the history of connected devices. Then, copy and paste the MAC in a service like [MA:CV:en:do:rs](https://macvendors.com/) to find the Vendor of that device. The Amazon Dash button vendor should be: *Amazon Technologies Inc.*

---------------------

### Credit

- [amazon-dashbutton](https://github.com/JulianKahnert/amazon-dashbutton) (Thanks to [JulianKahnert](https://github.com/JulianKahnert) in [Issue#1](https://github.com/danimtb/dasshio/issues/1))

### Sources & Inspiration:

- [Raspberry Pi script](https://github.com/vancetran/amazon-dash-rpi)
- [Maddox Dashbutton Repo](https://github.com/maddox/dasher)
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)

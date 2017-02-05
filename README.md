# Amazon Dashbutton Hack with Python daemon in docker


## Installation

```sh
docker run -d --name="dashbutton" -v $(pwd)/config.example.json:/app/config.json juka/amazon-dashbutton
```

## Test setup
Test your workflow with the `find_button.py` sniffing script.
```sh
docker exec -it dashbutton python find_button.py
```

# Sources & Inspiration:
- [Raspberry Pi script](https://github.com/vancetran/amazon-dash-rpi)
- [Maddox Dashbutton Repo](https://github.com/maddox/dasher)
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)

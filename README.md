# Amazon Dashbutton Hack with Python daemon in docker


## Installation
Generate your own `config.json` file ([example](https://github.com/JulianKahnert/amazon-dashbutton/blob/master/config.example.json)) and run this command afterwards:

```sh
docker run -d --name="dashbutton" --net=host -v $(pwd)/config.json:/app/config.json juka/amazon-dashbutton
```

## Find MAC addresses of dashbuttons
Run this command, to sniff buttons in your network:

```sh
docker exec -it dashbutton python find_button.py
```

## Compose example
Edit your local `config.json` file ([example](https://github.com/JulianKahnert/amazon-dashbutton/blob/master/config.example.json)) and generate a `docker-compose.yaml`, e.g.:

```
version: "2"
services:
  dashbutton:
    container_name: dashbutton
    image: juka/amazon-dashbutton:latest
    restart: always
    network_mode: "host"
    volumes:
      - ./config.json:/app/config.json
```

# Sources & Inspiration:
- [Raspberry Pi script](https://github.com/vancetran/amazon-dash-rpi)
- [Maddox Dashbutton Repo](https://github.com/maddox/dasher)
- [General Amazon Dash Hack](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.n6fhd3z40)

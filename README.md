# Dasshio - Amazon Dash Buttons hassio addon

## Options example

```
{
  "buttons": [
  {
    "name": "Gillette",
    "address": "AC:63:BE:96:C4:0D",
    "url": "http://home_assistant_IP:8123/api/services/light/toggle",
    "headers": "{\"x-ha-access\": \"your_password\"}",
    "body": "{\"entity_id\": \"light.luz_ambiente\"}"
  }]
}
```

## Credit
* [amazon-dashbutton](https://github.com/JulianKahnert/amazon-dashbutton)

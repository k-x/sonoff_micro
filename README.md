# SonoffMicroSwitch

A very simple class for switching [Sonoff Micro USB Smart Adaptor](https://sonoff.tech/product/diy-smart-switches/micro/) on and off
using RESTful API (HTTP POST requests).

Partially based on https://github.com/mattsaxon/pysonofflan (encrypt and decrypt functions).

## Usage

```python
from micro import SonoffMicroSwitch

device_id = "100xxxxxxx"
api_key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

switch = SonoffMicroSwitch(device_id, api_key)

# Get state right after initialization of the switch:
if switch.is_on():
    print("Switch is ON")

if switch.is_off():
    print("Switch is OFF")

# The class does not listen for state changes initiated by other software!
# If you need to update current state use:
switch.update()
# and then one of the is_*() methods

# Available actions:
switch.turn_on()
switch.turn_off()
switch.toggle()
```

## Getting the API key

The easiest way to get the API key is to add the Micro Switch to Home Assistant using https://github.com/AlexxIT/SonoffLAN –
the key will be saved to a config file.

## Support

This script is provided as is and no support is provided. 
In case it doesn’t meet your demands, feel free to fork and modify it.

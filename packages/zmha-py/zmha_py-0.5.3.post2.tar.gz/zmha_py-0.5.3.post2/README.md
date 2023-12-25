# ZMHA-Py

A loose Python wrapper of [ZoneMinder](https://www.zoneminder.org)'s API for the [Home Assistant Integration](https://www.home-assistant.io/integrations/zoneminder/)

[![Python package](https://github.com/nabbi/zmha-py/actions/workflows/python-tox.yml/badge.svg)](https://github.com/nabbi/zmha-py/actions/workflows/python-tox.yml)


## Acknowledgments

[zmha-py](https://github.com/nabbi/zmha-py) forked from [rohankapoorcom/zm-py](https://github.com/rohankapoorcom/zm-py) latest release [0.5.2](https://pypi.org/project/zm-py/) Oct 17, 2020.
The goal is to restore Home Assistant functionality with the current ZoneMinder 1.36 deployments by providing bug fixes and refactoring with upstream's API changes.

zm-py is based on code that was originally part of [Home Assistant](https://www.home-assistant.io).
As time goes on additional functionality will be added to this API client.

Historical sources and authorship information is available as part of the Home Assistant project:

- [ZoneMinder Platform](https://github.com/home-assistant/home-assistant/commits/dev/homeassistant/components/zoneminder.py)
- [ZoneMinder Camera](https://github.com/home-assistant/home-assistant/commits/dev/homeassistant/components/camera/zoneminder.py)
- [ZoneMinder Sensor](https://github.com/home-assistant/home-assistant/commits/dev/homeassistant/components/sensor/zoneminder.py)
- [ZoneMinder Switch](https://github.com/home-assistant/home-assistant/commits/dev/homeassistant/components/switch/zoneminder.py)

## Installation

### PyPI

```bash
$ pip install zmha-py
```

## Usage

```python
from zoneminder.zm import ZoneMinder

SERVER_HOST = "{{host}}:{{port}}"
USER = "{{user}}"
PASS = "{{pass}}"
SERVER_PATH = "{{path}}"

zm_client = ZoneMinder(
    server_host=SERVER_HOST, server_path=SERVER_PATH, username=USER, password=PASS, verify_ssl=False
)

#Zoneminder authentication
zm_client.login()


#Get all monitors
monitors = zm_client.get_monitors()

for monitor in monitors:
    print(monitor)

>>> Monitor(id='monitor_id', name='monitor_name', controllable='is_controllable')


#Move camera down
controllable_monitors = [m for m in monitors if m.controllable]

for monitor in controllable_monitors:
    zm_client.move_monitor(monitor, "right")
```

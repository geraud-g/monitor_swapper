# 💻 MonitorSwapper

A simple script for easily switching monitor input sources between computers from the system tray.

## Install
Install from the requirements.
``` bash
pip install -r requirements.txt
```


## Usage
### 1 - Get info
If you don't have it already, you can get the model of your computers from `get_monitor_info.py`:
```
python get_monitor_info.py
```
### 2 - Edit conf
Edit the conf part in `monitor_swapper.py`.
- The Hotkeys values are parsed by [keyboard](https://pypi.org/project/keyboard/)
- The InputSource is from [monitorcontrol](https://pypi.org/project/monitorcontrol/) and the list is available [here](https://github.com/newAM/monitorcontrol/blob/acff60bdfb75ff7592105175b362b76fecc60f7d/monitorcontrol/monitorcontrol.py#L41C4-L41C4).


```python
# Shortcut to swap to computer one
HOTKEY_SET_SOURCES_COMPUTER_ONE = "CTRL + ALT + PRINT_SCREEN"
# Shortcut to swap to computer two
HOTKEY_SET_SOURCES_COMPUTER_TWO = "CTRL + ALT + SCRLK"
# Shortcut to swap to computer two and set computer one to sleep
HOTKEY_SET_SOURCES_COMPUTER_TWO_AND_SLEEP = "CTRL + ALT + BREAK"

CONF_SCREENS = {
    "MODEL_SCREEN_1": {  # Model from `get_monitors_info.py`

        Computer.One: InputSource.DP1,
        Computer.Two: InputSource.HDMI2,
    },
    "MODEL_SCREEN_2": {  # Model from `get_monitors_info.py`
        Computer.One: InputSource.HDMI1,
        Computer.Two: InputSource.HDMI2
    },
}
```

### Run the script
You can then launch the script like any other from the command line:
``` shell
python monitor_swapper.py
```

Optionally, you can build it with pyinstaller from the .spec file:
```bash
pyinstaller --clean --onefile --noconsole --add-data "monitor.ico:." --icon monitor.ico monitor_swapper.py
```


## Misc
The icon is from [flaticon.com](https://www.flaticon.com/free-icon/monitor_9351909)

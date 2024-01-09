import os
import sys
from enum import Enum

import keyboard
from monitorcontrol import InputSource, get_monitors
from PIL import Image
from pystray import Icon, Menu, MenuItem


class Computer(Enum):
    One = 1  # Desktop
    Two = 2  # Laptop


###############################################################################
# CONFIG
###############################################################################
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
        Computer.Two: InputSource.HDMI2,
    },
}


###############################################################################
# CODE
###############################################################################
def set_monitors_source(computer: Computer):
    """
    Set the input source of all monitors for the given computer.
    """
    for monitor in get_monitors():
        with monitor:
            name = monitor.get_vcp_capabilities()["model"]
            monitor.set_input_source(CONF_SCREENS[name][computer])


def swap_to_computer_one(icon: Icon):
    icon.monitor_manager.set_monitors_source(Computer.One)


def swap_to_computer_two(icon: Icon):
    icon.monitor_manager.set_monitors_source(Computer.Two)


def swap_to_computer_two_and_sleep(icon: Icon):
    icon.swap_to_computer_two()
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def exit_app(icon: Icon):
    icon.visible = False
    icon.stop()


def setup(self):
    self.visible = True
    keyboard.add_hotkey(
        HOTKEY_SET_SOURCES_COMPUTER_ONE, lambda: self.swap_to_computer_one()
    )
    keyboard.add_hotkey(
        HOTKEY_SET_SOURCES_COMPUTER_TWO, lambda: self.swap_to_computer_two()
    )
    keyboard.add_hotkey(
        HOTKEY_SET_SOURCES_COMPUTER_TWO_AND_SLEEP,
        lambda: self.swap_to_computer_two_and_sleep(),
    )


def resource_path(relative_path):
    """Helper function to retrieve files from PyInstaller's tmp folder"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    image = Image.open(resource_path("monitor.ico"))
    icon = Icon(
        "Monitor Swapper",
        icon=image,
        menu=Menu(
            MenuItem(
                "Swap to Comp 1",
                swap_to_computer_one,
            ),
            MenuItem(
                "Swap to Comp 2",
                swap_to_computer_two,
            ),
            MenuItem(
                "Swap to Comp 2 + Set Comp 1 to sleep",
                swap_to_computer_two_and_sleep,
            ),
            Menu.SEPARATOR,
            MenuItem("Quit", exit_app),
        ),
    )
    icon.run(setup)
    image.close()


if __name__ == "__main__":
    main()

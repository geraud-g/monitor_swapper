import os
import sys
from enum import Enum

import keyboard
from monitorcontrol import InputSource
from monitorcontrol import Monitor as MonitorControlMonitor
from monitorcontrol import get_monitors
from PIL import Image
from pystray import Icon, Menu, MenuItem


class Computer(Enum):
    One = "Desktop"
    Two = "Laptop"


###############################################################################
# CONFIG
###############################################################################
# Shortcut to swap to computer one
HOTKEY_SET_SOURCES_COMPUTER_ONE = "CTRL + ALT + F9"
# Shortcut to swap to computer two
HOTKEY_SET_SOURCES_COMPUTER_TWO = "CTRL + ALT + F10"

CONF_SCREENS = {
    "SCREEN_1": {  # Model from `get_monitors_info.py`
        Computer.One: InputSource.DP1,
        Computer.Two: InputSource.HDMI2,
    },
    "SCREEN_2": {  # Model from `get_monitors_info.py`
        Computer.One: InputSource.HDMI1,
        Computer.Two: InputSource.HDMI2,
    },
}


###############################################################################
# CODE
###############################################################################
class Monitor:
    def __init__(self, monitor: MonitorControlMonitor):
        self.monitor = monitor
        with monitor:
            vcp_capabilities = monitor.get_vcp_capabilities()
            self.model = vcp_capabilities["model"]
            self.current_input_source = monitor.get_input_source()
            self.inputs = vcp_capabilities["inputs"]
            self.luminance = monitor.get_luminance()

    def set_source(self, source: InputSource):
        with self.monitor:
            print(f"Set {self.model} to {source}")
            self.monitor.set_input_source(source)

    def set_luminance(self, luminance: int):
        with self.monitor:
            print(f"Set {self.model} to {luminance}%")
            self.monitor.set_luminance(luminance)


def set_monitors_source(computer: Computer):
    """
    Set the input source of all monitors for the given computer.
    """
    for monitor in get_monitors():
        with monitor:
            name = monitor.get_vcp_capabilities()["model"]
            monitor.set_input_source(CONF_SCREENS[name][computer])


def swap_to_computer_two_and_sleep():
    set_monitors_source(Computer.Two)
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def exit_app(icon: Icon):
    icon.visible = False
    icon.stop()


###############################################################################
# PYSTRAY
###############################################################################
def resource_path(relative_path):
    """Helper function to retrieve files from PyInstaller's tmp folder"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_monitor_input_menu_item(monitor: Monitor) -> MenuItem:
    return MenuItem(
        "Input",
        Menu(
            *[
                MenuItem(
                    source.name,
                    lambda *args, s=source, m=monitor: m.set_source(s),
                )
                for source in monitor.inputs
            ],
        ),
    )


def get_monitor_brightness_menu_item(monitor: Monitor) -> MenuItem:
    return MenuItem(
        "Brightness",
        Menu(
            *[
                MenuItem(
                    f"{brightness}%",
                    lambda *args, b=brightness, m=monitor: m.set_luminance(b),
                )
                for brightness in [100, 75, 50, 25, 0]
            ]
        ),
    )


def get_monitors_menus(monitors: list[Monitor]) -> list[MenuItem]:
    menus = [MenuItem("--- SCREENS ---", None, enabled=False)]
    for monitor in monitors:
        menus.append(
            MenuItem(
                f"{monitor.model}",
                # Sources
                Menu(
                    get_monitor_input_menu_item(monitor),
                    get_monitor_brightness_menu_item(monitor),
                ),
            )
        )
    return menus


def get_computers_menus() -> list[MenuItem]:
    menus = [
        MenuItem("--- COMPUTERS ---", None, enabled=False),
        MenuItem(
            Computer.One.value,
            Menu(
                MenuItem(
                    "Set as input source",
                    lambda _: set_monitors_source(Computer.One),
                )
            ),
        ),
        MenuItem(
            Computer.Two.value,
            Menu(
                MenuItem(
                    "Set as input source",
                    lambda _: set_monitors_source(Computer.Two),
                ),
                MenuItem(
                    "Set as input source and sleep current",
                    lambda _: swap_to_computer_two_and_sleep(),
                ),
            ),
        ),
    ]
    return menus


def main():
    monitors = [Monitor(monitor) for monitor in get_monitors()]
    keyboard.add_hotkey(
        HOTKEY_SET_SOURCES_COMPUTER_ONE, lambda: set_monitors_source(Computer.One)
    )
    keyboard.add_hotkey(
        HOTKEY_SET_SOURCES_COMPUTER_TWO, lambda: set_monitors_source(Computer.Two)
    )

    image = Image.open(resource_path("monitor.ico"))
    icon = Icon(
        "Monitor Swapper",
        icon=image,
        menu=Menu(
            *get_monitors_menus(monitors),
            Menu.SEPARATOR,
            *get_computers_menus(),
            Menu.SEPARATOR,
            MenuItem("Quit", exit_app),
        ),
    )
    icon.run()
    image.close()


if __name__ == "__main__":
    main()

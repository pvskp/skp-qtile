import psutil
import os
import globals
from libqtile import qtile


def get_current_wireless_interface() -> str:
    interfaces = [iface for iface, stats in psutil.net_if_stats().items() if stats.isup]
    for iface in interfaces:
        if len(iface) > 2:
            if iface[0:2] == "wl":
                return iface
    return ""


def open_htop() -> None:
    qtile.cmd_spawn(f"{globals.TERMINAL} -e htop")


def update_system() -> None:
    qtile.cmd_spawn(f"{globals.TERMINAL} --hold -e sudo pacman -Syu")


def open_nmtui() -> None:
    qtile.cmd_spawn(f"{globals.TERMINAL} -e nmtui")


def execute_in_background(cmd: str):
    os.system(f"{cmd} &")


def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return

        if name in "9":
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()
        else:
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()

    return _inner

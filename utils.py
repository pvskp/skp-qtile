from logging import currentframe
from typing import Optional
import psutil
import os
import globals
from libqtile import qtile
import subprocess

def notify_send(subject: str, msg: str, icon: Optional[str] = None):
    if not icon:
        subprocess.Popen(["notify-send", subject, msg])
        return

    subprocess.Popen(["notify-send", subject, msg, "--icon", icon])

def get_current_screen():
    return qtile.current_screen

def cmd_print_current_screen():
    current_screen_width = get_current_screen().info()['width']
    current_screen_height = get_current_screen().info()['height']
    current_screen_x = get_current_screen().info()['x']
    current_screen_y = get_current_screen().info()['y']
    command = ['flameshot', 'gui', '--region']
    command.append(f'{current_screen_width}x{current_screen_height}+{current_screen_x}+{current_screen_y}')


    qtile.cmd_spawn(" ".join(command))


def change_keyboard_us_intl(event):
    change_keyboard_layout("us", "intl")


def change_keyboard_us(event):
    change_keyboard_layout("us")


def change_keyboard_layout(layout: str, variant: Optional[str] = None):
    keyboard_icon_path = "/usr/share/icons/elementary-xfce/devices/48/input-keyboard.png"
    if not variant:
        subprocess.Popen(["setxkbmap", layout])
        notify_send(
            "Keyboard Layout changed",
            f"Switched to layout '{layout}'",
            keyboard_icon_path,
        )
        return
    subprocess.Popen(["setxkbmap", layout, "-variant", variant])
    notify_send(
        "Keyboard Layout changed",
        f"Switched to layout '{layout}', variant '{variant}'",
        keyboard_icon_path,
    )


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

        qtile.groups_map[name].toscreen()

    return _inner

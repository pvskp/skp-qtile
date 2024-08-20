from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
from globals import CALCURSE, TERMINAL, SHELL
import utils
import distro
from layouts import default as myly


class Nord:
    bg: str = "#2E3440"  ## nord0 in palette
    darker: str = "#22262E"
    transparent: str = "#2E3440b3"  ## nord0 in palette
    fg: str = "#81A1C1"  ## nord0 in palette
    black: str = "#000000"  ## nord0 in palette
    dark_gray: str = "#3B4252"  ## nord1 in palette
    gray: str = "#434C5E"  ## nord2 in palette
    light_gray: str = "#4C566A"  ## nord3 in palette
    light_gray_bright: str = "#616E88"  ## out of palette
    darkest_white: str = "#D8DEE9"  ## nord4 in palette
    darker_white: str = "#E5E9F0"  ## nord5 in palette
    white: str = "#ECEFF4"  ## nord6 in palette
    teal: str = "#8FBCBB"  ## nord7 in palette
    off_blue: str = "#88C0D0"  ## nord8 in palette
    glacier: str = "#81A1C1"  ## nord9 in palette
    blue: str = "#5E81AC"  ## nord10 in palette
    red: str = "#BF616A"  ## nord11 in palette
    orange: str = "#D08770"  ## nord12 in palette
    yellow: str = "#EBCB8B"  ## nord13 in palette
    green: str = "#A3BE8C"  ## nord14 in palette
    purple: str = "#B48EAD"  ## nord15 in palette
    none: str = "NONE"


nord = Nord

distros = {
    "manjaro linux": {
        "icon": " ",
        "color": nord.green,
        "accent": nord.teal,
    },
    "ubuntu": {
        "icon": " ",
        "color": nord.orange,
        "accent": nord.orange,
    },
}

current_distro = distros[distro.name().lower()]

FONT_MONO = "JetBrainsMono Nerd Font"
FONT = "Arimo Nerd Font"

FONTCONFIG = {
    "font": FONT,
    "fontsize": 17,
    # "fontshadow": nord.white
}

# powerline = {"decorations": [PowerLineDecoration(path="back_slash")]}
powerline = {
    "decorations": [
        PowerLineDecoration(path="back_slash"),
    ],
    "padding": 10,
}

powerline = {
    "decorations": [
        RectDecoration(
            colour=nord.gray,
            radius=3,
            filled=True,
            # padding=3,
            # padding_x=0,
            padding_y=3,
            group=False,
            use_widget_background=True,
            line_width=0,
            extrawidth=0,
            # clip=True,
        )
    ]
}

systray_powerline = {
    "decorations": [
        RectDecoration(
            colour=nord.gray,
            radius=3,
            filled=True,
            padding_x=0,
            padding_y=4,
            group=False,
            use_widget_background=True,
            # line_width=10,
            # extrawidth=50,
            # clip=True,
        )
    ]
}

# powerline = {
#     "decorations": [
#         PowerLineDecoration(
#             path=[
#                 (0, 0),
#                 (0.5, 0),
#                 (0.5, 0.25),
#                 (1, 0.25),
#                 (1, 0.75),
#                 (0.5, 0.75),
#                 (0.5, 1),
#                 (0, 1),
#             ]
#         )
#     ]
# }


def separator():
    return widget.Sep(linewidth=10, background=nord.bg, foreground=nord.bg)


def text_separator(separator_size: int = 1, fg: str = nord.bg, bg: str = nord.bg):
    return widget.TextBox(text=" " * separator_size, foreground=fg, background=bg)


def group_box():
    return [
        widget.GroupBox(
            font=FONT_MONO,
            fontsize=20,
            active=nord.white,
            inactive=nord.light_gray_bright,
            highlight_method="text",
            highlight_color=[nord.darkest_white, nord.darkest_white],
            background=nord.gray,
            this_current_screen_border=current_distro["accent"],
            urgent_alert_method="text",
            urgent_text=nord.red,
            this_screen_border=nord.glacier,
            other_current_screen_border=nord.glacier,
            other_screen_border=nord.glacier,
            **powerline,
        ),
    ]


def window_name():
    return [
        widget.WindowName(
            fmt="{}",
            # format=" {state}{name}",
            format="",
            **FONTCONFIG,
            max_chars=40,
            # background=nord.gray,
            # **powerline,
        )
    ]


def systray():
    return [
        widget.Systray(
            background=nord.gray,
            icon_size=20,
            **systray_powerline,
        ),
    ]


def memory():
    return [
        widget.Memory(
            **FONTCONFIG,
            fmt=" 󰍛 {} ",
            foreground=nord.white,
            format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
            measure_mem="G",
            background=nord.gray,
            mouse_callbacks={"Button1": utils.open_htop},
            **powerline,
        )
    ]


def wlan():
    return [
        widget.Wlan(
            **FONTCONFIG,
            fmt=" 󰖩 {} ",
            interface=utils.get_current_wireless_interface(),
            format="{essid}",
            foreground=nord.white,
            background=nord.gray,
            mouse_callbacks={"Button1": utils.open_nmtui},
            **powerline,
        ),
    ]


def volume():
    return [
        widget.Volume(
            **FONTCONFIG,
            fmt=" {} ",
            mute_format="       ",
            unmute_format="  {volume}%",
            foreground=nord.white,
            background=nord.gray,
            **powerline,
        ),
    ]


def check_updates():
    return [
        widget.CheckUpdates(
            **FONTCONFIG,
            distro="Arch_Sup",
            colour_no_updates=nord.white,
            update_interval=600,
            fmt=" {} ",
            mouse_callbacks={"Button1": utils.update_system},
            colour_have_updates=nord.orange,
            background=nord.gray,
            display_format=" {updates}",
            **powerline,
        )
    ]


def battery():
    return [
        widget.Battery(
            **FONTCONFIG,
            foreground=nord.white,
            background=nord.gray,
            charge_char=" 󰁹",
            discharge_char=" 󰁹",
            not_charging_char="󰁹",
            empty="󱟩",
            full_char="󰂅",
            show_short_text=False,
            fmt=" {} ",
            format="{char} {percent:2.0%}",
            **powerline,
        ),
    ]


def clock():
    return [
        widget.Clock(
            **FONTCONFIG,
            fmt=" 󰥔 {} ",
            format="%H:%M",
            foreground=nord.white,
            background=nord.gray,
            **powerline,
        ),
    ]


def date():
    return [
        widget.Clock(
            font="Roboto",
            fontsize=16,
            fmt=" {} ",
            format="%d de %b de %Y",
            foreground=nord.white,
            background=nord.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(CALCURSE)},
            **powerline,
        ),
    ]


def spacer():
    return [
        widget.Spacer(),
    ]


def application_shortcuts():
    return [
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=" ",
            foreground=nord.orange,
            background=nord.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("firefox")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=" ",
            foreground=nord.blue,
            background=nord.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("thunderbird")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text="󰌽 ",
            foreground=nord.green,
            background=nord.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(TERMINAL)},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text="󰹑 ",
            foreground=nord.purple,
            background=nord.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("flameshot gui")},
            # **powerline,
        ),
    ]
    ...


def startmenu():
    return [
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=f"{current_distro['icon']}",
            foreground=current_distro["color"],
            # background=nord.gray,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash -c ~/.config/rofi/wrappers/runner")},
            # **powerline,
        ),
    ]


def bluetooth():
    return [
        widget.Bluetooth(
            default_text="  {connected_devices} ",
            background=nord.gray,
            default_show_battery=True,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("blueman-manager")},
            **powerline,
        ),
    ]


def powermenu():
    return [
        widget.TextBox(
            text=" 󰐦 ",
            font=FONT_MONO,
            fontsize=17,
            background=nord.red,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash -c ~/.config/qtile/rofi/rofi-power")},
            **powerline,
        ),
    ]


def backlight():
    return [
        widget.Backlight(
            font=FONT,
            fmt=" 󰃞 {} ",
            backlight_name="amdgpu_bl1",
            change_command="brightnessctl set {0}%",
            min_brightness=5,
            background=nord.gray,
            **powerline,
        )
    ]


def layouts():
    return myly.get_layout(
        columns_colors=myly.LayoutColumnsColors(
            border_focus=[current_distro["accent"]],
            border_focus_stack=[nord.blue],
            border_normal=[nord.gray],
        ),
        treetab_colors=myly.LayoutTreeTabColors(
            section_fg=nord.purple,
            inactive_bg=nord.gray,
            active_bg=nord.glacier,
            bg_color=nord.darker,
        ),
    )


def floating_layout():
    return myly.get_floating({"border_focus": current_distro["accent"], "border_normal": nord.bg})


def dmenu_theme(prompt: str = ""):
    return {
        "font": "Arimo Nerd Font",
        "fontsize": 14,
        "dmenu_bottom": True,
        "background": nord.bg,
        "selected_background": nord.blue,
        "selected_foreground": nord.white,
        "dmenu_prompt": prompt,
    }


def bars():
    widgets = [
        text_separator(),
        *startmenu(),
        text_separator(),
        *group_box(),
        text_separator(),
        *application_shortcuts(),
        text_separator(),
        *spacer(),
        *date(),
        *spacer(),
        text_separator(),
        *check_updates(),
        text_separator(),
        *systray(),
        # text_separator(),
        # *bluetooth(),
        text_separator(),
        *volume(),
        text_separator(),
        *wlan(),
        text_separator(),
        *memory(),
        text_separator(),
        *backlight(),
        text_separator(),
        *battery(),
        text_separator(),
        *clock(),
        text_separator(),
        *powermenu(),
        text_separator(),
    ]
    bar_margin = 0

    # if primary:
    #     systray_pos = 9
    #     widgets = widgets[0:systray_pos] + systray() + widgets[systray_pos:]

    return bar.Bar(
        widgets,
        32,
        margin=bar_margin,
        border_width=[3, 3, 3, 3],
        border_color=nord.dark_gray,
        background=nord.bg,
    )

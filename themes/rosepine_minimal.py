from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
from globals import CALCURSE, TERMINAL, SHELL
import utils
import distro
from layouts import default as myly


class RosePine:
    bg: str = "#191724"  ## base color in palette
    darker: str = "#1f1d2e"  ## slightly darker than bg
    transparent: str = "#191724b3"  ## base color with transparency
    fg: str = "#e0def4"  ## text color in palette
    black: str = "#000000"  ## black, often used for deep contrast
    dark_gray: str = "#26233a"  ## darker gray in palette
    gray: str = "#403d52"  ## medium gray in palette
    light_gray: str = "#6e6a86"  ## light gray in palette
    light_gray_bright: str = "#908caa"  ## brighter gray, slightly out of palette
    darkest_white: str = "#e0def4"  ## lightest white in palette
    darker_white: str = "#f2e9de"  ## softer white in palette
    white: str = "#f6f1e7"  ## warm white in palette
    teal: str = "#31748f"  ## teal in palette
    off_blue: str = "#9ccfd8"  ## softer blue in palette
    glacier: str = "#c4a7e7"  ## pastel purple in palette
    blue: str = "#524f67"  ## deep muted blue in palette
    red: str = "#eb6f92"  ## red in palette
    orange: str = "#f6c177"  ## orange in palette
    yellow: str = "#f6c177"  ## yellow in palette
    green: str = "#9ccfd8"  ## green in palette
    purple: str = "#c4a7e7"  ## purple in palette
    # widget_bg: str = "#ea9a97"
    widget_bg: str = "#c4a7e7"
    rose: str = "#ea9a97"
    none: str = "NONE"


pine = RosePine

distros = {
    "manjaro linux": {
        "icon": " ",
        "color": pine.green,
        "accent": pine.teal,
    },
    "ubuntu": {
        "icon": " ",
        "color": pine.orange,
        "accent": pine.orange,
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
            colour=pine.widget_bg,
            radius=3,
            filled=True,
            padding_x=0,
            padding_y=4,
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
            colour=pine.widget_bg,
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
    return widget.Sep(linewidth=10, background=pine.bg, foreground=pine.bg)


def text_separator(separator_size: int = 1, fg: str = pine.bg, bg: str = pine.bg):
    return widget.TextBox(text=" " * separator_size, foreground=fg, background=bg)


def group_box():
    return [
        widget.GroupBox(
            font=FONT_MONO,
            fontsize=20,
            active=pine.white,
            inactive=pine.light_gray_bright,
            highlight_method="text",
            highlight_color=[pine.darkest_white, pine.darkest_white],
            background=pine.gray,
            this_current_screen_border=pine.rose,
            urgent_alert_method="text",
            urgent_text=pine.red,
            this_screen_border=pine.glacier,
            other_current_screen_border=pine.glacier,
            other_screen_border=pine.glacier,
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
            # background=nord.widget_bg,
            # **powerline,
        )
    ]


def systray():
    return [
        widget.Systray(
            background=pine.widget_bg,
            icon_size=20,
            **systray_powerline,
        ),
    ]


def memory():
    return [
        widget.Memory(
            **FONTCONFIG,
            fmt=" 󰍛 {} ",
            foreground=pine.black,
            format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
            measure_mem="G",
            background=pine.widget_bg,
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
            foreground=pine.black,
            background=pine.widget_bg,
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
            foreground=pine.black,
            background=pine.widget_bg,
            **powerline,
        ),
    ]


def check_updates():
    return [
        widget.CheckUpdates(
            **FONTCONFIG,
            distro="Arch_Sup",
            colour_no_updates=pine.white,
            update_interval=600,
            fmt=" {} ",
            mouse_callbacks={"Button1": utils.update_system},
            colour_have_updates=pine.orange,
            background=pine.widget_bg,
            display_format=" {updates}",
            **powerline,
        )
    ]


def battery():
    return [
        widget.Battery(
            **FONTCONFIG,
            foreground=pine.black,
            background=pine.widget_bg,
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
            foreground=pine.black,
            background=pine.widget_bg,
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
            foreground=pine.white,
            background=pine.bg,
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
            foreground=pine.orange,
            background=pine.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("firefox")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=" ",
            foreground=pine.blue,
            background=pine.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("thunderbird")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text="󰌽 ",
            foreground=pine.green,
            background=pine.bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(TERMINAL)},
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
            # background=nord.widget_bg,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash -c ~/.config/rofi/wrappers/runner")},
            # **powerline,
        ),
    ]


def bluetooth():
    return [
        widget.Bluetooth(
            default_text="  {connected_devices} ",
            background=pine.widget_bg,
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
            background=pine.red,
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
            background=pine.widget_bg,
            foreground=pine.black,
            **powerline,
        )
    ]


def layouts():
    return myly.get_layout(
        columns_colors=myly.LayoutColumnsColors(
            border_focus=[current_distro["accent"]],
            border_focus_stack=[pine.blue],
            border_normal=[pine.widget_bg],
        ),
        treetab_colors=myly.LayoutTreeTabColors(
            section_fg=pine.purple,
            inactive_bg=pine.widget_bg,
            active_bg=pine.glacier,
            bg_color=pine.darker,
        ),
    )


def floating_layout():
    return myly.get_floating({"border_focus": current_distro["accent"], "border_normal": pine.bg})


def dmenu_theme(prompt: str = ""):
    return {
        "font": "Arimo Nerd Font",
        "fontsize": 14,
        "dmenu_bottom": True,
        "background": pine.bg,
        "selected_background": pine.blue,
        "selected_foreground": pine.white,
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
        border_color=pine.dark_gray,
        background=pine.bg,
    )

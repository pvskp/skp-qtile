from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
from globals import CALCURSE, TERMINAL
import utils
import distro
from layouts import default as myly
import colorschemes

# theme = colorschemes.TokyoNight
theme = colorschemes.Gruvbox


distros = {
    "manjaro linux": {
        "icon": " ",
        "color": theme.blue,
        "accent": theme.blue,
        "backlight_name": "amdgpu_bl1",
    },
    "arch linux": {
        "icon": "󰣇 ",
        "color": theme.foreground_light,
        "accent": theme.foreground_light,
        "backlight_name": "amdgpu_bl1",
    },
    "ubuntu": {
        "icon": " ",
        "color": "#fe8019",
        "accent": theme.accent1,
        "backlight_name": "intel_backlight",
    },
}

current_distro = distros[distro.name().lower()]

FONT_MONO = "JetBrainsMono Nerd Font"
FONT = "JetBrainsMono Nerd Font"


space_multiplier = 1
if not any(term in FONT.lower() for term in ["mono", "nerd"]):
    space_multiplier = 3

space = " "

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
            colour=theme.gray,
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
            colour=theme.gray,
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
    return widget.Sep(linewidth=10, background=theme.background, foreground=theme.background)


def text_separator(separator_size: int = 1, fg: str = theme.background, bg: str = theme.background):
    return widget.TextBox(text=space * separator_size, foreground=fg, background=bg)


def group_box():
    return [
        widget.GroupBox(
            font=FONT_MONO,
            fontsize=20,
            active=theme.foreground,
            inactive=theme.light_gray,
            highlight_method="text",
            highlight_color=[theme.foreground_darker, theme.foreground_darker],
            background=theme.gray,
            this_current_screen_border=current_distro["accent"],
            urgent_alert_method="text",
            urgent_text=theme.red,
            this_screen_border=theme.accent3,
            other_current_screen_border=theme.accent3,
            other_screen_border=theme.accent3,
            **powerline,
        ),
        text_separator(),
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
            background=theme.gray,
            icon_size=20,
            **systray_powerline,
        ),
        text_separator(),
    ]


def memory():
    return [
        widget.Memory(
            **FONTCONFIG,
            fmt=" 󰍛" + space * space_multiplier + "{}" + space,
            foreground=theme.foreground_bright,
            format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
            measure_mem="G",
            background=theme.gray,
            mouse_callbacks={"Button1": utils.open_htop},
            **powerline,
        ),
        text_separator(),
    ]


def wlan():
    return [
        widget.Wlan(
            **FONTCONFIG,
            fmt=" 󰖩 {} ",
            interface=utils.get_current_wireless_interface(),
            format="{essid}",
            foreground=theme.foreground_bright,
            background=theme.gray,
            mouse_callbacks={"Button1": utils.open_nmtui},
            **powerline,
        ),
        text_separator(),
    ]


def volume():
    return [
        widget.Volume(
            **FONTCONFIG,
            fmt=" {} ",
            mute_format="       ",
            unmute_format=" " + space * space_multiplier + "{volume}%",
            foreground=theme.foreground_bright,
            background=theme.gray,
            **powerline,
        ),
        text_separator(),
    ]


def check_updates():
    return [
        widget.CheckUpdates(
            **FONTCONFIG,
            distro="Arch_Sup",
            colour_no_updates=theme.foreground_bright,
            update_interval=600,
            fmt=" {} ",
            mouse_callbacks={"Button1": utils.update_system},
            colour_have_updates=theme.orange,
            background=theme.gray,
            display_format=" {updates}",
            **powerline,
        ),
        text_separator(),
    ]


def battery():
    return [
        widget.Battery(
            **FONTCONFIG,
            foreground=theme.foreground_bright,
            background=theme.gray,
            charge_char=" 󰁹",
            discharge_char=" 󰁹",
            not_charging_char="󰁹",
            empty="󱟩",
            full_char="󰂅",
            show_short_text=False,
            fmt=" {} ",
            format="{char}" + space * space_multiplier + "{percent:2.0%}",
            **powerline,
        ),
        text_separator(),
    ]


def clock():
    return [
        widget.Clock(
            **FONTCONFIG,
            fmt=" 󰥔" + space * space_multiplier + "{}" + space,
            format="%H:%M",
            foreground=theme.foreground_bright,
            background=theme.gray,
            **powerline,
        ),
        text_separator(),
    ]


def date():
    return [
        widget.Clock(
            font="Inter",
            fontsize=16,
            fmt=" {} ",
            format="%d de %b de %Y",
            foreground=theme.foreground_bright,
            background=theme.background,
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
            foreground=theme.orange,
            background=theme.background,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("firefox")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=" ",
            foreground=theme.blue,
            background=theme.background,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("thunderbird")},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text="󰌽 ",
            foreground=theme.green,
            background=theme.background,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(TERMINAL)},
            # **powerline,
        ),
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text="󰹑 ",
            foreground=theme.purple,
            background=theme.background,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("flameshot gui")},
            # **powerline,
        ),
        text_separator(),
    ]


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
        text_separator(),
    ]


def bluetooth():
    return [
        widget.Bluetooth(
            default_text="  {connected_devices} ",
            background=theme.gray,
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
            background=theme.red,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash -c ~/.config/qtile/rofi/rofi-power")},
            **powerline,
        ),
        text_separator(),
    ]


def backlight():
    return [
        widget.Backlight(
            font=FONT,
            fmt=" 󰃞" + space * space_multiplier + "{} ",
            backlight_name=current_distro["backlight_name"],
            change_command="brightnessctl set {0}%",
            min_brightness=5,
            foreground=theme.foreground_bright,
            background=theme.gray,
            **powerline,
        ),
        text_separator(),
    ]


def layouts():
    return myly.get_layout(
        columns_colors=myly.LayoutColumnsColors(
            border_focus=[current_distro["accent"]],
            border_focus_stack=[theme.blue],
            border_normal=[theme.dark_gray],
        ),
        # plasma_colors=myly.LayoutPlasmaColors(
        #     border_focus=current_distro["color"],
        #     border_focus_fixed=nord.gray,
        #     border_normal=nord.glacier,
        #     border_normal_fixed=nord.darker,
        # ),
        treetab_colors=myly.LayoutTreeTabColors(
            section_fg=theme.purple,
            inactive_bg=theme.gray,
            active_bg=theme.accent3,
            bg_color=theme.background_darker,
        ),
    )


def floating_layout():
    return myly.get_floating({"border_focus": current_distro["accent"], "border_normal": theme.background})


def dmenu_theme(prompt: str = ""):
    return {
        "font": "Arimo Nerd Font",
        "fontsize": 14,
        "dmenu_bottom": True,
        "background": theme.background,
        "selected_background": theme.blue,
        "selected_foreground": theme.foreground_bright,
        "dmenu_prompt": prompt,
    }


def bars(primary: bool):
    widgets = [
        text_separator(),
        *startmenu(),
        *group_box(),
        *application_shortcuts(),
        *spacer(),
        *date(),
        *spacer(),
        *check_updates(),
        *volume(),
        *wlan(),
        *memory(),
        *backlight(),
        *battery(),
        *clock(),
        *powermenu(),
    ]
    bar_margin = 0

    if primary:
        widgets = [
            text_separator(),
            *startmenu(),
            *group_box(),
            *application_shortcuts(),
            *spacer(),
            *date(),
            *spacer(),
            *check_updates(),
            *systray(),
            *volume(),
            # *wlan(),
            *memory(),
            *backlight(),
            *battery(),
            *clock(),
            *powermenu(),
        ]

    return bar.Bar(
        widgets,
        32,
        margin=bar_margin,
        border_width=[3, 3, 3, 3],
        border_color=theme.background,
        background=[theme.background],
    )

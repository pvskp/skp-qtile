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
        "accent": theme.group_box_active,
        "backlight_name": "intel_backlight",
    },
}

current_distro = distros[distro.name().lower()]

FONT_MONO = "JetBrainsMono Nerd Font"
FONT = "Arimo Nerd Font"


space_multiplier = 1
if not any(term in FONT.lower() for term in ["mono", "nerd"]):
    space_multiplier = 3

space = " "

FONTCONFIG = {
    "font": FONT,
    "fontsize": 17,
    # "fontshadow": nord.white
}


def separator():
    return widget.Sep(linewidth=10, background=theme.background, foreground=theme.background)


def pipe_separator(separator_size: int = 1, fg: str = theme.foreground, bg: str = theme.background):
    return widget.TextBox(
        text="|",
        foreground=fg,
        background=bg,
    )


def space_separator(separator_size: int = 1, fg: str = theme.background, bg: str = theme.background):
    return widget.TextBox(text=space * separator_size, foreground=fg, background=bg)


def group_box():
    return [
        widget.GroupBox(
            font=FONT_MONO,
            fontsize=20,
            active=theme.foreground,
            inactive=theme.foreground_darker,
            highlight_method="text",
            highlight_color=[theme.foreground_darker, theme.foreground_darker],
            background=theme.background,
            this_current_screen_border=current_distro["accent"],
            urgent_alert_method="text",
            urgent_text=theme.red,
            this_screen_border=theme.accent3,
            other_current_screen_border=theme.accent3,
            other_screen_border=theme.accent3,
        ),
        space_separator(),
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
        )
    ]


def systray():
    return [
        widget.Systray(
            background=theme.background,
            icon_size=20,
        ),
        space_separator(),
    ]


def memory():
    return [
        widget.Memory(
            **FONTCONFIG,
            fmt="󰍛 {}",
            foreground=theme.foreground_bright,
            format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
            measure_mem="G",
            background=theme.background,
            mouse_callbacks={"Button1": utils.open_htop},
        ),
        space_separator(),
    ]


def wlan():
    return [
        widget.Wlan(
            **FONTCONFIG,
            fmt="󰖩 {}",
            interface=utils.get_current_wireless_interface(),
            format="{essid}",
            foreground=theme.foreground_bright,
            background=theme.background,
            mouse_callbacks={"Button1": utils.open_nmtui},
        ),
        space_separator(),
    ]


def volume():
    return [
        widget.Volume(
            **FONTCONFIG,
            fmt="{}",
            mute_format="       ",
            unmute_format="   {volume}%",
            foreground=theme.foreground_bright,
            background=theme.background,
        ),
        space_separator(),
    ]


def check_updates():
    return [
        widget.CheckUpdates(
            **FONTCONFIG,
            distro="Arch_Sup",
            colour_no_updates=theme.foreground_bright,
            update_interval=600,
            fmt="{}",
            mouse_callbacks={"Button1": utils.update_system},
            colour_have_updates=theme.orange,
            background=theme.background,
            display_format=" {updates}",
        ),
        space_separator(),
    ]


def battery():
    return [
        widget.Battery(
            **FONTCONFIG,
            foreground=theme.foreground_bright,
            background=theme.background,
            charge_char=" 󰁹",
            discharge_char=" 󰁹",
            not_charging_char="󰁹",
            empty="󱟩",
            full_char="󰂅",
            show_short_text=False,
            fmt="{}",
            format="{char} {percent:2.0%}",
        ),
        space_separator(),
    ]


def clock():
    return [
        widget.Clock(
            **FONTCONFIG,
            fmt="󰥔 {}",
            format="%H:%M",
            foreground=theme.foreground_bright,
            background=theme.background,
        ),
        space_separator(),
    ]


def date():
    return [
        widget.Clock(
            font="Inter",
            fontsize=16,
            fmt="{}",
            format="%d de %b de %Y",
            foreground=theme.foreground_bright,
            background=theme.background,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(CALCURSE)},
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
        space_separator(),
    ]


def startmenu():
    return [
        widget.TextBox(
            font=FONT,
            fontsize=20,
            text=f"{current_distro['icon']}",
            foreground=current_distro["color"],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash -c ~/.config/rofi/wrappers/runner")},
            # **powerline,
        ),
        space_separator(),
    ]


def bluetooth():
    return [
        widget.Bluetooth(
            default_text="  {connected_devices} ",
            background=theme.background,
            default_show_battery=True,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("blueman-manager")},
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
        ),
        # space_separator(),
    ]


def backlight():
    return [
        widget.Backlight(
            font=FONT,
            fmt="󰃞 {}",
            backlight_name=current_distro["backlight_name"],
            change_command="brightnessctl set {0}%",
            min_brightness=5,
            foreground=theme.foreground_bright,
            background=theme.background,
        ),
        space_separator(),
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
            inactive_bg=theme.background,
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
            space_separator(),
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
            *systray(),
            *powermenu(),
        ]

    return bar.Bar(
        widgets,
        32,
        margin=bar_margin,
        border_width=[0, 0, 0, 0],
        border_color=theme.background,
        background=[theme.background],
    )
from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
import utils
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

FONT = "SpaceMono Nerd Font"

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
            **FONTCONFIG,
            active=nord.white,
            inactive=nord.light_gray_bright,
            highlight_method="text",
            highlight_color=[nord.darkest_white, nord.darkest_white],
            background=nord.gray,
            this_current_screen_border=nord.yellow,
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
            format="󱂬 {state}{name}",
            **FONTCONFIG,
            background=nord.bg,
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
            fmt=" 󰖩  {} ",
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
            fmt="   {} ",
            foreground=nord.white,
            background=nord.gray,
            **powerline,
        ),
    ]


def check_updates():
    return [
        widget.CheckUpdates(
            **FONTCONFIG,
            distro="Arch",
            colour_no_updates=nord.white,
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
            charge_char="󱟠",
            discharge_char="󱟞",
            empty="󱟩",
            full_char="󰂅 ",
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


def startmenu():
    return [
        widget.TextBox(
            **FONTCONFIG,
            text="   ",
            foreground=nord.green,
            background=nord.gray,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    "bash -c ~/.config/rofi/wrappers/runner"
                )
            },
            **powerline,
        ),
    ]


def powermenu():
    return [
        widget.TextBox(
            text=" 󰐦 ",
            **FONTCONFIG,
            background=nord.red,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    "bash -c ~/.config/qtile/rofi/rofi-power"
                )
            },
            **powerline,
        ),
    ]


def layouts():
    return myly.get_layout(
        columns_colors=myly.LayoutColumnsColors(
            border_focus=[nord.black], border_focus_stack=[nord.blue]
        ),
        treetab_colors=myly.LayoutTreeTabColors(
            section_fg=nord.purple,
            inactive_bg=nord.gray,
            active_bg=nord.glacier,
            bg_color=nord.darker,
        ),
    )


# def layouts():
#     return myly.get_layout(
#         columns_colors={
#             "border_focus": [nord.black],
#             "border_focus_stack": [nord.blue],
#         },
#         treetab_colors={
#             "section_fg": nord.purple,
#             "inactive_fg": nord.gray,
#             "active_bg": nord.glacier,
#             "bg_color": nord.black,
#         },
#     )


def floating_layout():
    return myly.get_floating({"border_focus": nord.black})


def bars(primary: bool = False):
    widgets = [
        text_separator(),
        *startmenu(),
        text_separator(),
        *group_box(),
        text_separator(),
        *window_name(),
        text_separator(),
        *check_updates(),
        text_separator(),
        *volume(),
        text_separator(),
        *wlan(),
        text_separator(),
        *memory(),
        text_separator(),
        *battery(),
        text_separator(),
        *clock(),
        text_separator(),
        *powermenu(),
        text_separator(),
    ]
    bar_margin = 0

    if primary:
        systray_pos = 7
        widgets = widgets[0:systray_pos] + systray() + widgets[systray_pos:]

    return bar.Bar(
        widgets,
        35,
        margin=bar_margin,
        border_width=[0, 0, 0, 0],
        border_color=nord.black,
        background=nord.bg,
    )

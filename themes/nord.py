from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
import utils
from layouts import default as myly


class Nord:
    bg: str = "#2E3440"  ## nord0 in palette
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

FONT = "FiraCode Nerd Font"

FONTCONFIG = {
    "font": FONT,
    "fontsize": 17,
    # "fontshadow": nord.white
}

# powerline = {"decorations": [PowerLineDecoration(path="back_slash")]}
powerline = {
    "decorations": [
        PowerLineDecoration(path="back_slash"),
    ]
}

# powerline = {
#     "decorations": [RectDecoration(colour=nord.bg, radius=5, filled=True, group=False)]
# }

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
            active=nord.black,
            inactive=nord.light_gray,
            highlight_method="line",
            highlight_color=[nord.darkest_white, nord.darkest_white],
            background=nord.fg,
            this_current_screen_border=nord.purple,
            this_screen_border=nord.glacier,
            other_current_screen_border=nord.glacier,
            other_screen_border=nord.glacier,
            **powerline,
        ),
    ]


def window_name():
    return [
        widget.WindowName(
            fmt="󱂬 {}",
            **FONTCONFIG,
            background=nord.bg,
            **powerline,
        )
    ]


def systray():
    return [
        widget.Systray(
            background=nord.light_gray,
            **powerline,
        ),
    ]


def memory():
    return [
        widget.Memory(
            **FONTCONFIG,
            fmt="󰍛{}",
            foreground=nord.black,
            background=nord.purple,
            mouse_callbacks={"Button1": utils.open_htop},
            **powerline,
        )
    ]


def wlan():
    return [
        widget.Wlan(
            **FONTCONFIG,
            fmt="󰖩 {}",
            interface=utils.get_current_wireless_interface(),
            format="{essid}",
            foreground=nord.black,
            background=nord.blue,
            mouse_callbacks={"Button1": utils.open_nmtui},
            **powerline,
        ),
    ]


def volume():
    return [
        widget.Volume(
            **FONTCONFIG,
            fmt="  {}",
            foreground=nord.black,
            background=nord.off_blue,
            **powerline,
        ),
    ]


def battery():
    return [
        widget.Battery(
            **FONTCONFIG,
            background=nord.yellow,
            foreground=nord.black,
            charge_char="󱟠",
            discharge_char="󱟞",
            empty="󱟩",
            full_char="󰂅 ",
            fmt="{}",
            format="{char} {percent:2.0%}",
            **powerline,
        ),
    ]


def clock():
    return [
        widget.Clock(
            **FONTCONFIG,
            fmt="󰥔 {}",
            format="%H:%M",
            background=nord.orange,
            foreground=nord.black,
            **powerline,
        ),
    ]


def startmenu():
    return [
        widget.TextBox(
            **FONTCONFIG,
            text="  ",
            foreground=nord.green,
            background=nord.light_gray,
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
            bg_color=nord.bg,
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
        *startmenu(),
        *group_box(),
        *window_name(),
        *volume(),
        *wlan(),
        *memory(),
        *battery(),
        *clock(),
        *powermenu(),
    ]
    bar_margin = 4

    if primary:
        widgets.insert(3, *systray())

    return bar.Bar(
        widgets,
        30,
        margin=bar_margin,
        border_width=[2, 2, 2, 2],
        border_color=nord.black,
    )

from libqtile import layout, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
import colors


nord = colors.Nord


# FONT = "SpaceMono Nerd Font"
FONT = "RobotoMono Nerd Font"
FONTCONFIG = {
    "font": FONT,
    "fontsize": 15,
}

powerline = {
    "decorations": [
        PowerLineDecoration(
            path=[
                (0, 0),
                (0.5, 0),
                (0.5, 0.25),
                (1, 0.25),
                (1, 0.75),
                (0.5, 0.75),
                (0.5, 1),
                (0, 1),
            ]
        )
    ]
}


def separator():
    return widget.Sep(linewidth=10, background=nord.bg, foreground=nord.bg)


def text_separator(separator_size: int = 1, fg: str = nord.bg, bg: str = nord.bg):
    return widget.TextBox(text=" " * separator_size, foreground=fg, background=bg)


def _widget_right_half_triangle(fg: str = nord.fg, bg: str = nord.bg):
    return widget.TextBox(
        text="",
        padding=0,
        fontsize="30",
        foreground=fg,
        background=bg,
    )


def _widget_left_half_circle(fg: str = nord.fg, bg: str = nord.bg):
    return widget.TextBox(
        text="",
        padding=0,
        fontsize="30",
        foreground=fg,
        background=bg,
    )


def _widget_right_half_circle(fg: str = nord.fg, bg: str = nord.bg):
    return widget.TextBox(
        text="",
        font=FONT,
        padding=0,
        fontsize="30",
        foreground=fg,
        background=bg,
    )


def group_box():
    return [
        widget.GroupBox(
            font=FONT,
            active=nord.black,
            inactive=nord.light_gray,
            highlight_method="line",
            highlight_color=[nord.darkest_white, nord.darkest_white],
            background=nord.fg,
            # this_current_screen_border=nord.darkest_white,
            this_current_screen_border=nord.purple,
            this_screen_border=nord.glacier,
            other_current_screen_border=nord.glacier,
            other_screen_border=nord.glacier,
            # block_highlight_text_color=nord.black,
        ),
        # _widget_right_half_circle(nord.fg),
    ]


def window_name():
    return [
        widget.WindowName(
            fmt=" 󱂬 {}",
            font=FONT,
            background=nord.bg,
            **powerline,
        )
    ]


def systray():
    return [
        # _widget_left_half_circle(fg=nord.green),
        widget.Systray(
            background=nord.green,
            **powerline,
        ),
        # _widget_right_half_circle(fg=nord.green),
    ]


def memory():
    return [
        widget.Memory(
            font=FONT,
            fmt=" 󰍛{}",
            foreground=nord.black,
            background=nord.purple,
            **powerline,
        )
    ]


def wlan():
    return [
        widget.Wlan(
            font=FONT,
            fmt=" 󰖩 {}",
            interface="wlp1s0",
            format="{essid}",
            foreground=nord.white,
            background=nord.blue,
            **powerline,
        ),
    ]


def volume():
    return [
        widget.Volume(
            font=FONT,
            fmt="   {}",
            foreground=nord.black,
            background=nord.off_blue,
            **powerline,
        ),
    ]


def battery():
    return [
        # _widget_left_half_circle(fg=nord.yellow),
        widget.Battery(
            font=FONT,
            # fontshadow=nord.black,
            # fontsize=18,
            background=nord.yellow,
            foreground=nord.black,
            charge_char="󱟠",
            discharge_char="󱟞",
            empty="󱟩",
            full_char="󰂅 ",
            fmt=" {}",
            format="{char} {percent:2.0%}",
            **powerline,
        ),
        # _widget_right_half_circle(fg=nord.yellow),
    ]


def clock():
    return [
        # _widget_left_half_circle(fg=nord.orange),
        widget.Clock(
            font=FONT,
            # fontshadow=nord.black,
            fmt=" 󰥔 {}",
            format="%H:%M",
            background=nord.orange,
            foreground=nord.black,
            **powerline,
        ),
        # _widget_right_half_circle(fg=nord.orange),
    ]


def startmenu():
    return [
        widget.TextBox(
            text=" ",
            fontsize=20,
            foreground=nord.green,
            background=nord.blue,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    "bash -c ~/.config/qtile/rofi/rofi-power"
                )
            },
        ),
        # _widget_right_half_triangle(fg=nord.blue, bg=nord.fg),
    ]


def powermenu():
    return [
        # _widget_left_half_circle(fg=nord.red),
        widget.TextBox(
            text=" 󰐦 ",
            background=nord.red,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    "bash -c ~/.config/qtile/rofi/rofi-power"
                )
            },
        ),
    ]


def LTreeTab():
    return layout.TreeTab(
        **FONTCONFIG,
        active_bg=nord.glacier,
        bg_color=nord.black,
    )

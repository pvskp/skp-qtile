from libqtile import bar, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import hook
import colors
import nord as nr
import os

# color = colors.Neutral
nord = colors.Nord


def execute_in_background(cmd: str):
    os.system(f"{cmd} &")


execute_in_background("nitrogen --restore")
execute_in_background("xhost +si:localuser:$USER")

BORDER_WIDTH = 2


@hook.subscribe.startup_once
def start_once() -> None:
    execute_in_background("picom")
    execute_in_background("xset b off")
    execute_in_background("xset b 0 0 0")
    execute_in_background("barrier")


mod = "mod4"
alt = "mod1"
terminal = "kitty --title Kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        lazy.layout.move_down().when(layout=["treetab"]),
        desc="Move window down",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        lazy.layout.move_up().when(layout=["treetab"]),
        desc="Move window up",
    ),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.spawn(f"{terminal} -e bash -c ~/.tmux/scripts/sessionizer.tmux"),
        desc="Launch terminal",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "s", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod, "shift"],
        "space",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "d", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key(
        [mod, "shift"],
        "d",
        lazy.spawn("rofi -show run"),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [mod],
        "d",
        lazy.spawn("bash -c ~/.config/rofi/wrappers/runner"),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [mod, "shift"],
        "e",
        lazy.spawn("bash -c ~/.config/qtile/rofi/rofi-power"),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
    ),
    Key(
        [],
        "XF86AudioMicMute",
        lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle"),
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +10%"),
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 10%-"),
    ),
    Key(
        [alt],
        "Tab",
        lazy.group.focus_back(),
        desc="Alternate between two most recent windows",
    ),
    Key([mod], "Tab", lazy.screen.toggle_group(), desc="Last active group"),
    Key(
        [],
        "Print",
        lazy.spawn(
            "bash -c 'maim -s | xclip -selection clipboard -t image/png && notify-send 'Selection Saved to clipboard''"
        ),
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn("spectacle"),
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group("1"),
    Group("2"),
    Group("3", layout="treetab"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
]


for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(toggle=True),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


def default_dropdown(id: str, command: str) -> DropDown:
    return DropDown(
        id,
        command,
        opacity=1,
        height=0.7,
        width=0.7,
        x=0.15,
        y=0.15,
    )


groups.append(
    ScratchPad(
        "scratchpad",
        [
            default_dropdown(
                "Ranger",
                "kitty -e ranger",
            ),
            default_dropdown(
                "Pavucontrol",
                "/usr/bin/pavucontrol-qt",
            ),
        ],
    )
)

keys.extend(
    [
        Key(
            [mod],
            "m",
            lazy.group["scratchpad"].dropdown_toggle("Ranger"),
        ),
        Key(
            [mod],
            "p",
            lazy.group["scratchpad"].dropdown_toggle("Pavucontrol"),
        ),
    ]
)

treetab = nr.LTreeTab()

layouts = [
    layout.Columns(
        border_focus=[nord.black],
        border_focus_stack=[nord.blue],
        border_width=BORDER_WIDTH,
        margin=5,
        border_on_single=True,
    ),  # pyright: ignore[]
    treetab,
    # layout.Max(),                                                              # pyright: ignore[]
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

DEFAULT_WIDGETS = [
    *nr.startmenu(),
    *nr.group_box(),
    *nr.window_name(),
    *nr.volume(),
    *nr.wlan(),
    *nr.memory(),
    *nr.battery(),
    *nr.clock(),
    *nr.powermenu(),
]

PRIMARY_MONITOR_WIDGETS = [
    *nr.startmenu(),
    *nr.group_box(),
    *nr.window_name(),
    *nr.systray(),
    *nr.volume(),
    *nr.memory(),
    *nr.battery(),
    *nr.clock(),
    *nr.powermenu(),
]

BAR_MARGIN = 4

primary_bar = bar.Bar(
    PRIMARY_MONITOR_WIDGETS,
    30,
    margin=BAR_MARGIN,
    border_width=[2, 2, 2, 2],
    border_color=nord.black,
    # opacity=0.75,
)

default_bar = bar.Bar(
    DEFAULT_WIDGETS,
    30,
    margin=BAR_MARGIN,
    border_width=[2, 2, 2, 2],
    border_color=nord.black,
)


@hook.subscribe.startup
def _():
    primary_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)
    default_bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)


screens = [
    Screen(
        top=primary_bar,
    ),
    Screen(
        top=default_bar,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=[nord.black],
    border_width=BORDER_WIDTH,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="Gpick"),
        Match(wm_class="spectacle"),
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

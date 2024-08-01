from functools import partialmethod
from libqtile import qtile
from libqtile.config import Click, Drag, Group, Key, Screen, ScratchPad, DropDown
from libqtile import extension
from screeninfo import get_monitors
from libqtile.lazy import lazy
from libqtile import hook
from themes import nord_minimal as theme
import globals
import utils


utils.execute_in_background("nitrogen --restore")
utils.execute_in_background("xhost +si:localuser:$USER")

BORDER_WIDTH = 2


@hook.subscribe.startup_once
def start_once() -> None:
    utils.execute_in_background("picom")
    utils.execute_in_background("xset b off")
    utils.execute_in_background("xset b 0 0 0")
    utils.execute_in_background("barrier")
    utils.execute_in_background("/usr/lib/polkit-kde-authentication-agent-1")


mod = "mod4"
alt = "mod1"
terminal = globals.TERMINAL
k9s = "/home/linuxbrew/.linuxbrew/bin/k9s"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), lazy.layout.move_down().when(layout=["treetab"]), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), lazy.layout.move_up().when(layout=["treetab"]), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn(f"{terminal} -e bash -c ~/.tmux/scripts/sessionizer.tmux"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "s", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "d", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show run"), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("bash -c ~/.config/rofi/wrappers/runner"), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "e", lazy.spawn("bash -c ~/.config/qtile/rofi/rofi-power"), desc="Spawn a command using a prompt widget"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    Key([alt], "Tab", lazy.group.focus_back(), desc="Alternate between two most recent windows"),
    Key([mod], "Tab", lazy.screen.toggle_group(), desc="Last active group"),
    Key([], "Print", lazy.spawn("bash -c 'maim -s | xclip -selection clipboard -t image/png && notify-send 'Selection Saved to clipboard''")),
    Key([mod], "Print", lazy.spawn("spectacle")),
    Key([alt, "shift"], "1", lazy.spawn('bash -c \'setxkbmap us -variant intl && notify-send "Keyboard Layout" "Switched to us -variant intl"\'')),
    Key([alt, "shift"], "2", lazy.spawn('bash -c \'setxkbmap us && notify-send "Keyboard Layout" "Switched to us"\'')),
    Key(
        [alt, "shift"],
        "k",
        lazy.run_extension(
            extension.CommandSet(
                commands={
                    "dev": f"kitty --title 'k9s (dev)' -e bash -c '{k9s} --context dev'",
                    "prod": f"kitty --title 'k9s (prod)' -e bash -c '{k9s} --context prod'",
                },
                **theme.dmenu_theme(prompt="󱃾 select cluster:"),
            )
        ),
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


groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
group_labels = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
group_layouts = ["columns", "columns", "treetab", "columns", "columns", "columns", "columns", "columns", "columns"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.function(utils.go_to_group(i.name)), desc="Switch to group {}".format(i.name)),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name)),
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
            default_dropdown("Ranger", "kitty -e ranger"),
            default_dropdown("TODO", "kitty -e zsh -c 'nvim ~/TODO.md'"),
            default_dropdown("Pavucontrol", "/usr/bin/pavucontrol-qt"),
        ],
    )
)

keys.extend(
    [
        Key([mod], "m", lazy.group["scratchpad"].dropdown_toggle("Ranger")),
        Key([mod], "n", lazy.group["scratchpad"].dropdown_toggle("TODO")),
        Key([mod], "p", lazy.group["scratchpad"].dropdown_toggle("Pavucontrol")),
    ]
)

layouts = theme.layouts()

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = []
for mon in get_monitors():
    if isinstance(mon.is_primary, bool):
        screens.append(Screen(top=theme.bars(primary=not mon.is_primary)))  # don't know yet why I need to negate this


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = theme.floating_layout()
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

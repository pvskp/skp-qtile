from libqtile import layout
from libqtile.config import Match

# TERMINAL = "kitty"
TERMINAL = "ghostty"
SHELL = "bash -i -c"
CALCURSE = f"{TERMINAL} --class 'calcurse' -e {SHELL} calcurse"

FLOATING_RULES = [
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),
    Match(wm_class="makebranch"),
    Match(wm_class="maketag"),
    Match(wm_class="Webapp-manager.py"),
    Match(wm_class="Gpick"),
    Match(wm_class="Gpick"),
    Match(wm_class="spectacle"),
    Match(wm_class="Mechvibes"),
    Match(wm_class="calcurse"),
    Match(wm_class="Blueman-manager"),
    Match(wm_class="Lutris"),
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    Match(wm_class="minecraft-launcher"),
    Match(wm_class="Lxappearance"),
    Match(title="branchdialog"),  # gitk
    Match(title="pinentry"),  # GPG key password entry
    Match(wm_class="pritunl"),  # ssh-askpass
    Match(wm_class="Matplotlib"),
    Match(wm_class="pkhex.exe"),
    Match(wm_class="pamac-manager"),
    Match(wm_class="scrcpy"),
]

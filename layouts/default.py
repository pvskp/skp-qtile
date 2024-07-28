from libqtile import init, layout
from libqtile.config import Match

BORDER_WIDTH = 2


class LayoutColumnsColors:
    border_focus: list[str] = ["#000000"]
    border_focus_stack: list[str] = ["#0000ff"]

    def __init__(
        self,
        border_focus: list[str],
        border_focus_stack: list[str],
    ) -> None:
        self.border_focus: list[str] = border_focus
        self.border_focus_stack: list[str] = border_focus_stack


class LayoutTreeTabColors:
    section_fg: str = "#b500ff"
    inactive_bg: str = "#c2c2c2"
    active_bg: str = "#0000ff"
    bg_color: str = "#000000"

    def __init__(
        self,
        section_fg: str,
        inactive_bg: str,
        active_bg: str,
        bg_color: str,
    ) -> None:
        self.section_fg = section_fg
        self.inactive_bg = inactive_bg
        self.active_bg = active_bg
        self.bg_color = bg_color


def get_floating(floating_config={"border_focus": "#000000"}):
    return layout.Floating(
        **floating_config,
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


def get_layout(
    columns_colors: LayoutColumnsColors,
    treetab_colors: LayoutTreeTabColors,
):
    return [
        layout.Columns(
            **vars(columns_colors),
            border_width=BORDER_WIDTH,
            margin=5,
            border_on_single=True,
        ),  # pyright: ignore[]
        layout.TreeTab(
            font="FiraCode Nerd Font Bold",
            fontsize=17,
            **vars(treetab_colors),
            # border_width=2,
            section_fontsize=15,
            section_bottom=10,
            sections=["DEFAULT", ""],
            panel_width=200,
        ),
    ]

from typing import Optional
from libqtile import layout
from libqtile.config import Match
from libqtile import hook
import globals

BORDER_WIDTH = 2


class LayoutColumnsConfig:
    border_focus: list[str] = ["#000000"]
    border_focus_stack: list[str] = ["#0000ff"]

    def __init__(
        self,
        border_focus: list[str],
        border_focus_stack: list[str],
        border_normal: list[str],
    ) -> None:
        self.border_focus: list[str] = border_focus
        self.border_focus_stack: list[str] = border_focus_stack
        self.border_normal = border_normal


class LayoutMaxConfig:
    def __init__(
        self,
        border_focus: str,
        border_normal: str,
        only_focused: bool,
    ) -> None:
        self.border_focus: str = border_focus
        self.border_normal = border_normal
        self.only_focused = only_focused


class LayoutPlasmaConfig:
    def __init__(
        self,
        border_focus: str,
        border_focus_fixed: str,
        border_normal: str,
        border_normal_fixed: str,
    ) -> None:
        self.border_focus: str = border_focus
        self.border_focus_fixed: str = border_focus_fixed
        self.border_normal: str = border_normal
        self.border_normal_fixed: str = border_normal_fixed


class LayoutTreeTabConfig:
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


def get_floating(floating_config={"border_focus": "#000000", "border_normal": "#000000"}):
    return layout.Floating(
        **floating_config,
        border_width=BORDER_WIDTH,
        float_rules=globals.FLOATING_RULES,
    )


@hook.subscribe.client_new
def set_floating_and_size(window):
    if window.match(Match(wm_class="calcurse")):
        window.floating = True
        window.cmd_set_size_floating(1200, 600)  # Largura e altura desejadas


def get_layout(
    columns_config: Optional[LayoutColumnsConfig] = None,
    plasma_config: Optional[LayoutPlasmaConfig] = None,
    max_config: Optional[LayoutMaxConfig] = None,
    treetab_config: Optional[LayoutTreeTabConfig] = None,
):
    layouts = []

    if columns_config:
        layouts.append(
            layout.Columns(
                **vars(columns_config),
                border_width=BORDER_WIDTH,
                margin=5,
                border_on_single=True,
            ),  # pyright: ignore[]
        )

    if max_config:
        layouts.append(
            layout.Max(
                **vars(max_config),
                border_width=BORDER_WIDTH,
                margin=0,
            ),
        )

    if plasma_config:
        layouts.append(
            layout.Plasma(
                **vars(plasma_config),
                border_width=BORDER_WIDTH,
                margin=5,
                border_width_single=BORDER_WIDTH,
            ),
        )

    if treetab_config:
        layouts.append(
            layout.TreeTab(
                font="FiraCode Nerd Font Bold",
                fontsize=17,
                **vars(treetab_config),
                # border_width=2,
                section_fontsize=15,
                section_bottom=10,
                sections=["DEFAULT", ""],
                panel_width=200,
            ),
        )

    return layouts

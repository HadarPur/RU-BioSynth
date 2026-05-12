"""Design tokens and QSS stylesheet factories.

Tokens (colors, fonts, sizes, margins, labels, titles) live in
:mod:`tokens`. QSS factories that consume them live in :mod:`styles`.
Both are re-exported here so call sites can do::

    from biosynth.executions.controllers.ui.theme import COLORS, transparent_text_edit_qss
"""

from biosynth.executions.controllers.ui.theme.styles import (
    circular_button_qss,
    floating_indicator_qss,
    global_app_qss,
    info_dialog_text_qss,
    placeholder_label_qss,
    scroll_area_borderless_qss,
    status_label_qss,
    table_qss,
    text_edit_transparent_only_qss,
    transparent_text_edit_qss,
)
from biosynth.executions.controllers.ui.theme.tokens import (
    COLORS,
    FONTS,
    LABELS,
    MARGINS,
    SIZES,
    TITLES,
    Colors,
    Fonts,
    Labels,
    Margins,
    Sizes,
    Titles,
)

__all__ = [
    # Tokens
    "COLORS", "FONTS", "SIZES", "MARGINS", "LABELS", "TITLES",
    "Colors", "Fonts", "Sizes", "Margins", "Labels", "Titles",
    # Styles
    "global_app_qss",
    "transparent_text_edit_qss",
    "text_edit_transparent_only_qss",
    "circular_button_qss",
    "floating_indicator_qss",
    "info_dialog_text_qss",
    "status_label_qss",
    "placeholder_label_qss",
    "scroll_area_borderless_qss",
    "table_qss",
]

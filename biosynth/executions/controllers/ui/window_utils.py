"""Backwards-compatibility shim.

Original ``window_utils`` was split first into ``widgets``, ``factories``,
and ``file_actions`` modules, then reorganized into ``widgets/``,
``utils/``, ``theme/``, and ``windows/`` subpackages. Existing imports
such as ``from ...window_utils import add_button`` keep working through
these re-exports.
"""

from biosynth.executions.controllers.ui.utils import (
    add_button,
    add_code_block,
    add_drop_table,
    add_drop_text_edit,
    add_intro,
    add_logo_toolbar,
    add_png_logo,
    add_spinbox,
    add_text_edit,
    add_text_edit_html,
    add_toggle,
    adjust_scroll_area_height,
    adjust_text_edit_height,
    copy_to_clipboard,
    create_scroll_area,
    create_table_from_data,
    download_file,
    save_to_file,
)
from biosynth.executions.controllers.ui.widgets import (
    CircularButton,
    DropTableWidget,
    DropTextEdit,
    FloatingScrollIndicator,
    ToggleSwitch,
)

__all__ = [
    "CircularButton",
    "DropTableWidget",
    "DropTextEdit",
    "FloatingScrollIndicator",
    "ToggleSwitch",
    "add_button",
    "add_code_block",
    "add_drop_table",
    "add_drop_text_edit",
    "add_intro",
    "add_logo_toolbar",
    "add_png_logo",
    "add_spinbox",
    "add_text_edit",
    "add_text_edit_html",
    "add_toggle",
    "adjust_scroll_area_height",
    "adjust_text_edit_height",
    "copy_to_clipboard",
    "create_scroll_area",
    "create_table_from_data",
    "download_file",
    "save_to_file",
]

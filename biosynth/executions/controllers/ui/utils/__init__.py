"""Helper utilities for the BioSynth GUI.

- :mod:`factories` — layout-builder helpers (add_button, add_spinbox, ...).
- :mod:`file_actions` — download/save-as/copy callbacks wired to buttons.
- :mod:`validation` — GUI-side input validation with QMessageBox feedback.
"""

from biosynth.executions.controllers.ui.utils.factories import (
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
    create_scroll_area,
    create_table_from_data,
)
from biosynth.executions.controllers.ui.utils.file_actions import (
    copy_to_clipboard,
    download_file,
    save_to_file,
)
from biosynth.executions.controllers.ui.utils.validation import GuiValidator
from biosynth.executions.controllers.ui.utils.workers import EliminationWorker

__all__ = [
    "EliminationWorker",
    "GuiValidator",
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

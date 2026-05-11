"""Custom Qt widgets used by the BioSynth GUI.

Custom widgets (toggles, drop targets, the floating scroll indicator) live
in :mod:`custom`. The tabbed help dialog lives in :mod:`info_dialog`. All
are re-exported here.
"""

from biosynth.executions.controllers.ui.widgets.busy_dialog import BusyDialog
from biosynth.executions.controllers.ui.widgets.custom import (
    CircularButton,
    DropTableWidget,
    DropTextEdit,
    FloatingScrollIndicator,
    ToggleSwitch,
)
from biosynth.executions.controllers.ui.widgets.info_dialog import InfoDialog

__all__ = [
    "BusyDialog",
    "CircularButton",
    "DropTableWidget",
    "DropTextEdit",
    "FloatingScrollIndicator",
    "InfoDialog",
    "ToggleSwitch",
]

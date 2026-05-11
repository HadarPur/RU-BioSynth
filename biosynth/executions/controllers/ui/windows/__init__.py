"""Wizard windows for the BioSynth GUI.

The flow is Upload → Settings → Elimination → Results, all coordinated by
:class:`BaseWindow`. Each step inherits from :class:`WizardPage`.
"""

from biosynth.executions.controllers.ui.windows.base_window import BaseWindow
from biosynth.executions.controllers.ui.windows.elimination_window import EliminationWindow
from biosynth.executions.controllers.ui.windows.results_window import ResultsWindow
from biosynth.executions.controllers.ui.windows.settings_window import SettingsWindow
from biosynth.executions.controllers.ui.windows.upload_window import UploadWindow
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage

__all__ = [
    "BaseWindow",
    "EliminationWindow",
    "ResultsWindow",
    "SettingsWindow",
    "UploadWindow",
    "WizardPage",
]

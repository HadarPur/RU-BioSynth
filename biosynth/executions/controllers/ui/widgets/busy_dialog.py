"""Modal dialog with an indeterminate progress bar.

Shown while a long-running operation runs on a worker thread. The dialog
has no Cancel/Close affordance — the caller controls its lifetime by
calling :meth:`close` from the worker's completion slot.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout

from biosynth.executions.controllers.ui.theme import LABELS, SIZES, TITLES


class BusyDialog(QDialog):
    def __init__(self, parent=None, message=None, title=None):
        super().__init__(parent)
        self.setWindowTitle(title or TITLES.busy_dialog)
        self.setFixedSize(SIZES.busy_dialog_w, SIZES.busy_dialog_h)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        label = QLabel(message or LABELS.busy_message)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        bar = QProgressBar()
        bar.setRange(0, 0)  # indeterminate
        bar.setTextVisible(False)
        layout.addWidget(bar)

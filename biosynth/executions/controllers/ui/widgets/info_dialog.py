"""Reusable tabbed help dialog.

Replaces the inline `QDialog` builders that were duplicated in
`upload_window.py` and `results_window.py`. Two convenience constructors:

    InfoDialog.from_html(parent, title, tabs=[(name, html), ...])
    InfoDialog.from_widgets(parent, title, tabs=[(name, widget), ...])

The dialog opens at its design dimensions, which also serve as its
minimum size — the user can drag it larger but not below the baseline.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from biosynth.executions.controllers.ui.theme import (
    SIZES,
    TITLES,
    info_dialog_tabs_qss,
    info_dialog_text_qss,
)


class InfoDialog(QDialog):
    def __init__(self, parent=None, title=None, fixed_size=None):
        super().__init__(parent)
        self.setWindowTitle(title or TITLES.info_dialog)
        # ``fixed_size`` keeps the old API but now means "initial / minimum
        # size" — the dialog is resizable from there upwards.
        w, h = fixed_size or (SIZES.info_dialog_w, SIZES.info_dialog_h_short)
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setWindowFlags(
            Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint
        )
        self.setWindowModality(Qt.NonModal)
        self.setSizeGripEnabled(True)

        self._layout = QVBoxLayout()
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(info_dialog_tabs_qss())
        self._layout.addWidget(self._tabs)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        self._layout.addWidget(button_box)
        self.setLayout(self._layout)

    def add_html_tab(self, name: str, html: str):
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(html)
        text_edit.setStyleSheet(info_dialog_text_qss())
        self._tabs.addTab(text_edit, name)
        return text_edit

    def add_widget_tab(self, name: str, widget: QWidget):
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(widget)
        wrapper.setLayout(wrapper_layout)
        self._tabs.addTab(wrapper, name)
        return wrapper

    @classmethod
    def from_html(cls, parent, title, tabs, fixed_size=None):
        dialog = cls(parent=parent, title=title, fixed_size=fixed_size)
        for name, html in tabs:
            dialog.add_html_tab(name, html)
        return dialog

    @classmethod
    def from_widgets(cls, parent, title, tabs, fixed_size=None):
        dialog = cls(parent=parent, title=title, fixed_size=fixed_size)
        for name, widget in tabs:
            dialog.add_widget_tab(name, widget)
        return dialog

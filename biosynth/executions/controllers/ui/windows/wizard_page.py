"""Base class for BioSynth wizard pages.

Each step (Settings, Elimination, Results) is a `QWidget` that follows the
same skeleton:

    [ top bar with Back button ]
    [ middle body — overridden per page ]
    [ bottom bar with Next/Done button ]

`WizardPage` encapsulates the skeleton so subclasses only implement
`build_body()`. It also owns the `FloatingScrollIndicator` so `resizeEvent`
isn't reimplemented in every window.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from biosynth.executions.controllers.ui.theme import LABELS, MARGINS
from biosynth.executions.controllers.ui.utils import add_button
from biosynth.executions.controllers.ui.widgets import FloatingScrollIndicator


class WizardPage(QWidget):
    def __init__(self, back_callback=None, next_callback=None,
                 next_label=None, back_label=None):
        super().__init__()
        self._back_callback = back_callback
        self._next_callback = next_callback
        self._next_label = next_label or LABELS.next
        self._back_label = back_label or LABELS.back
        self.floating_btn = None
        self.next_button = None

    def build(self):
        """Template method — call from subclass `__init__` after fields are set."""
        layout = QVBoxLayout(self)
        if self._back_callback is not None:
            self.build_top_bar(layout)
        self.build_body(layout)
        if self._next_callback is not None:
            self.build_bottom_bar(layout)

    def build_top_bar(self, layout):
        add_button(layout, self._back_label, Qt.AlignLeft, self._back_callback, ())

    def build_body(self, layout):  # pragma: no cover - subclasses override
        raise NotImplementedError

    def build_bottom_bar(self, layout):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(*MARGINS.page_top_bottom)
        layout.addLayout(bottom_layout)
        self.next_button = add_button(bottom_layout, self._next_label, Qt.AlignRight)
        self.next_button.clicked.connect(lambda: self._next_callback())

    def attach_floating_indicator(self, scroll_target):
        self.floating_btn = FloatingScrollIndicator(parent=self, scroll_area=scroll_target)
        scrollbar = scroll_target.verticalScrollBar()
        scrollbar.rangeChanged.connect(
            lambda _min, _max: self.floating_btn.on_scroll(scrollbar.value())
        )
        self.floating_btn.on_scroll(scrollbar.value())

    def resizeEvent(self, event):
        if self.floating_btn is not None:
            self.floating_btn.raise_()
            self.floating_btn.reposition()
        super().resizeEvent(event)

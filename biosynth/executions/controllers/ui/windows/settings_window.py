from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout

from biosynth.data.app_data import InputData
from biosynth.executions.controllers.ui.theme import (
    FONTS,
    MARGINS,
    text_edit_transparent_only_qss,
    transparent_text_edit_qss,
)
from biosynth.executions.controllers.ui.utils import create_scroll_area
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils


def _monospace_font():
    font = QFont(FONTS.code_family)
    font.setPointSize(FONTS.code_point_size)
    return font


class _AutoHeightHtmlView(QTextEdit):
    """Read-only HTML view that keeps its document text width in sync with
    its viewport and resizes its height to fit the rendered content.

    Solves the symptom where ``QTextEdit`` initialised with a fixed
    ``setTextWidth`` keeps that text width even after the parent window
    has been resized — leaving the text content stuck at a narrow column
    while the widget border grows around it.
    """

    def __init__(self, html: str = "", parent=None):
        super().__init__(parent)
        self.setFont(_monospace_font())
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.viewport().setCursor(Qt.ArrowCursor)
        self.setStyleSheet(text_edit_transparent_only_qss())
        if html:
            self.setHtml(html)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_height()

    def showEvent(self, event):
        super().showEvent(event)
        self._adjust_height()

    def _adjust_height(self):
        self.document().setTextWidth(self.viewport().width())
        margins = self.contentsMargins()
        height = int(
            self.document().size().height()
            + margins.top()
            + margins.bottom()
            + 10
        )
        self.setFixedHeight(height)


class _AutoFitSequenceView(_AutoHeightHtmlView):
    """Sequence view that recomputes its per-line wrap to match the
    current viewport width on every resize, so the rendered bases fill
    the visible area instead of stopping at a hard-coded line length.
    """

    def __init__(self, sequence: str, coding_indexes, parent=None):
        self._sequence = sequence
        self._coding_indexes = coding_indexes
        self._rendering = False
        super().__init__("", parent)
        self._render()

    def _chars_per_line(self) -> int:
        char_w = max(1, self.fontMetrics().horizontalAdvance("A"))
        # Subtract a small padding so the right column never clips.
        usable = max(20, self.viewport().width() - 10)
        return max(20, usable // char_w)

    def _render(self):
        if self._rendering:
            return
        self._rendering = True
        try:
            html = "<pre>" + SequenceUtils.highlight_sequences_to_html(
                self._sequence,
                self._coding_indexes,
                line_length=self._chars_per_line(),
                returnBr=True,
            ) + "</pre>"
            self.setHtml(html)
            self._adjust_height()
        finally:
            self._rendering = False

    def resizeEvent(self, event):
        # Re-render BEFORE auto-adjusting height so the height reflects
        # the freshly-computed line count.
        QTextEdit.resizeEvent(self, event)
        self._render()


class SettingsWindow(WizardPage):
    def __init__(self, switch_to_eliminate_callback, back_to_upload_callback):
        super().__init__(
            back_callback=back_to_upload_callback,
            next_callback=switch_to_eliminate_callback,
        )
        self.build()

    def build_body(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(*MARGINS.page_middle)
        layout.addLayout(middle_layout)

        scroll_area, _content_widget, content_layout = create_scroll_area(middle_layout)

        self._add_target_sequence(content_layout)
        self._add_unwanted_patterns(content_layout)

        content_layout.addStretch(1)
        self.attach_floating_indicator(scroll_area)

    def _add_target_sequence(self, content_layout):
        content_layout.addWidget(QLabel("<h2>Input</h2><h3>Target Sequence:</h3>"))

        InputData.coding_positions, InputData.coding_indexes = (
            DNAUtils.get_coding_and_non_coding_regions_positions(
                InputData.cleaned_dna_sequence, InputData.start_codon_identified
            )
        )

        if InputData.coding_indexes is not None and len(InputData.coding_indexes) > 0:
            description = (
                f"<p>A coding region was identified in the target sequence at "
                f"positions {InputData.coding_indexes[0] + 1} - "
                f"{InputData.coding_indexes[1]}:</p>"
            )
        else:
            description = "<p>A coding region identified in the provided target sequence</p>"

        content_layout.addWidget(QLabel(description))

        view = _AutoFitSequenceView(
            InputData.cleaned_dna_sequence,
            InputData.coding_indexes,
        )
        view.setStyleSheet(transparent_text_edit_qss(margin_right_px=0))
        content_layout.addWidget(view)

    def _add_unwanted_patterns(self, content_layout):
        content_layout.addWidget(QLabel("<h3>Unwanted Patterns:</h3>"))

        html = f"<p>{SequenceUtils.get_patterns(InputData.unwanted_patterns)}</p>"
        view = _AutoHeightHtmlView(html)
        view.setStyleSheet(transparent_text_edit_qss(margin_right_px=0))
        content_layout.addWidget(view)

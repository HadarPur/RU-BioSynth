from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from biosynth.data.app_data import InputData
from biosynth.executions.controllers.ui.theme import (
    FONTS,
    MARGINS,
    SIZES,
    table_qss,
    text_edit_transparent_only_qss,
    transparent_text_edit_qss,
)
from biosynth.executions.controllers.ui.utils import create_scroll_area
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils


def _monospace_font():
    font = QFont(FONTS.code_family)
    # Pixel size to match the QSS body font size 1:1 so the sequence
    # display renders at the same visual size as the rest of the UI.
    font.setPixelSize(FONTS.body_px)
    return font


class _AutoHeightHtmlView(QTextEdit):
    """Read-only HTML view that keeps its document text width in sync with
    its viewport and resizes its height to fit the rendered content.

    Solves the symptom where ``QTextEdit`` initialised with a fixed
    ``setTextWidth`` keeps that text width even after the parent window
    has been resized — leaving the text content stuck at a narrow column
    while the widget border grows around it.
    """

    def __init__(self, html: str = "", parent=None, max_height: int | None = None):
        super().__init__(parent)
        self._max_height = max_height
        self.setFont(_monospace_font())
        self.setReadOnly(True)
        self.viewport().setCursor(Qt.ArrowCursor)
        if max_height is None:
            self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setStyleSheet(text_edit_transparent_only_qss())
        # Force <pre>/<p> blocks in the parsed HTML to honour body_px —
        # Qt's HTML renderer otherwise shrinks <pre> by ~17%.
        self.document().setDefaultStyleSheet(
            f"pre {{ font-size: {FONTS.body_px}px; margin: 0; }} "
            f"p {{ font-size: {FONTS.body_px}px; margin: 0; }}"
        )
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
        if self._max_height is not None and height > self._max_height:
            height = self._max_height
        self.setFixedHeight(height)


class _AutoFitSequenceView(_AutoHeightHtmlView):
    """Sequence view that recomputes its per-line wrap to match the
    current viewport width on every resize, so the rendered bases fill
    the visible area instead of stopping at a hard-coded line length.
    """

    def __init__(self, sequence: str, coding_indexes, parent=None, max_height: int | None = None):
        self._sequence = sequence
        self._coding_indexes = coding_indexes
        self._highlight_range = None
        self._rendering = False
        super().__init__("", parent, max_height=max_height)
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
                highlight_ranges=[self._highlight_range] if self._highlight_range else None,
            ) + "</pre>"
            self.setHtml(html)
            self._adjust_height()
        finally:
            self._rendering = False

    def set_highlight_range(self, start: int, end: int):
        self._highlight_range = (start, end)
        self._render()
        self._scroll_to_position(start)

    def _scroll_to_position(self, pos_1based: int):
        chars_per_line = self._chars_per_line()
        if chars_per_line <= 0:
            return
        line_index = max(0, (pos_1based - 1) // chars_per_line)
        line_height = max(1, self.fontMetrics().height())
        y_in_view = line_index * line_height

        # If this view has its own scrollbar (max_height clamp triggered),
        # scroll inside it; otherwise scroll the surrounding QScrollArea.
        sb = self.verticalScrollBar()
        if sb.maximum() > 0:
            sb.setValue(max(0, min(sb.maximum(), y_in_view - self.viewport().height() // 2)))
            return

        scroll_area = self.parentWidget()
        while scroll_area is not None and not isinstance(scroll_area, QAbstractScrollArea):
            scroll_area = scroll_area.parentWidget()
        if scroll_area is None or scroll_area.widget() is None:
            return

        top_in_scroll = self.mapTo(scroll_area.widget(), self.rect().topLeft())
        target_y = top_in_scroll.y() + y_in_view
        scroll_area.ensureVisible(
            0,
            target_y,
            0,
            scroll_area.viewport().height() // 2,
        )

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

        self._sequence_view = None
        self._add_target_sequence(content_layout)
        self._add_unwanted_patterns(content_layout)
        self._add_pattern_occurrences(content_layout)

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
            max_height=SIZES.sequence_diff_height,
        )
        view.setStyleSheet(transparent_text_edit_qss(margin_right_px=0))
        content_layout.addWidget(view)
        self._sequence_view = view

    def _add_unwanted_patterns(self, content_layout):
        content_layout.addWidget(QLabel("<h3>Unwanted Patterns:</h3>"))

        html = f"<p>{SequenceUtils.get_patterns(InputData.unwanted_patterns)}</p>"
        view = _AutoHeightHtmlView(html)
        view.setStyleSheet(transparent_text_edit_qss(margin_right_px=0))
        content_layout.addWidget(view)

    def _add_pattern_occurrences(self, content_layout):
        if not InputData.unwanted_patterns:
            return

        rows = SequenceUtils.get_pattern_occurrences(
            InputData.cleaned_dna_sequence, InputData.unwanted_patterns
        )
        InputData.unwanted_patterns_occurrences = rows
        if not any(row["Count"] for row in rows):
            return

        content_layout.addWidget(
            QLabel("<h3>Unwanted Pattern Occurrences in the Target Sequence:</h3>")
        )

        table = QTableWidget()
        table.setFont(_monospace_font())
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Pattern", "Count", "Positions"])
        table.setRowCount(len(rows))

        left_align = Qt.AlignLeft | Qt.AlignVCenter
        pattern_labels = []

        for r, row in enumerate(rows):
            pattern_item = QTableWidgetItem(row["Pattern"])
            pattern_item.setTextAlignment(left_align)
            pattern_item.setFlags(pattern_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(r, 0, pattern_item)

            count_item = QTableWidgetItem(str(row["Count"]))
            count_item.setTextAlignment(left_align)
            count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(r, 1, count_item)

            if row["Positions"]:
                links = ", ".join(
                    f'<a href="hl:{tok}" style="color:#245076; text-decoration:none;">{tok}</a>'
                    for tok in row["Positions"]
                )
            else:
                links = "—"

            label = QLabel(links)
            label.setTextFormat(Qt.RichText)
            label.setWordWrap(True)
            label.setOpenExternalLinks(False)
            label.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.LinksAccessibleByKeyboard)
            label.setAlignment(left_align)
            label.setContentsMargins(10, 4, 10, 4)
            label.linkActivated.connect(self._on_position_link_activated)
            table.setCellWidget(r, 2, label)
            pattern_labels.append((r, label))

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setDefaultAlignment(left_align)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setFocusPolicy(Qt.NoFocus)
        table.horizontalHeader().setMinimumHeight(SIZES.table_header_min_h)
        table.verticalHeader().setDefaultSectionSize(SIZES.table_row_default_h)
        table.setCornerButtonEnabled(False)
        table.setStyleSheet(table_qss())
        table.setMinimumHeight(SIZES.scroll_area_max_inline * 2)

        def resize_rows():
            col_w = table.columnWidth(2) - 24  # subtract label content margins
            if col_w <= 0:
                return
            for row_idx, lbl in pattern_labels:
                h = lbl.heightForWidth(col_w)
                if h <= 0:
                    h = lbl.sizeHint().height()
                table.setRowHeight(row_idx, max(SIZES.table_row_default_h, h + 12))

        header.sectionResized.connect(
            lambda idx, *_: resize_rows() if idx == 2 else None
        )
        QTimer.singleShot(0, resize_rows)

        content_layout.addWidget(table)

    def _on_position_link_activated(self, href: str):
        if self._sequence_view is None or not href.startswith("hl:"):
            return
        try:
            start_str, end_str = href[3:].split("-", 1)
            start = int(start_str)
            end = int(end_str)
        except ValueError:
            return
        self._sequence_view.set_highlight_range(start, end)

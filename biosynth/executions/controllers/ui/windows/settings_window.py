from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QHeaderView,
    QLabel,
    QLayout,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from biosynth.data.app_data import InputData
from biosynth.executions.controllers.ui.theme import (
    COLORS,
    FONTS,
    HEADINGS,
    MARGINS,
    SIZES,
    card_text_edit_qss,
    table_qss,
    text_edit_transparent_only_qss,
    transparent_text_edit_qss,
)
from biosynth.executions.controllers.ui.utils import create_scroll_area
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.coding_region import CodingRegionLocator


class _FlowLayout(QLayout):
    """Left-to-right layout that wraps children onto new lines when they
    overflow the available width — used to lay out position-range chips."""

    def __init__(self, parent=None, margin=0, spacing=4):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self._items = []

    def addItem(self, item):
        """Append a QLayoutItem to the flow."""
        self._items.append(item)

    def count(self):
        """Return the number of layout items."""
        return len(self._items)

    def itemAt(self, index):
        """Return the item at ``index`` or ``None`` if out of range."""
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index):
        """Pop and return the item at ``index`` or ``None`` if out of range."""
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self):
        """Report that the layout does not expand in any orientation."""
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        """Indicate that height depends on width for proper wrapping."""
        return True

    def heightForWidth(self, width):
        """Compute the wrapped layout height needed for the given ``width``."""
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        """Apply ``rect`` to the layout and reposition all child items."""
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        """Return the preferred size — same as the minimum size."""
        return self.minimumSize()

    def minimumSize(self):
        """Return the smallest size that fits any single item plus margins."""
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        return size + QSize(m.left() + m.right(), m.top() + m.bottom())

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_h = 0
        spacing = self.spacing()
        for item in self._items:
            hint = item.sizeHint()
            next_x = x + hint.width() + spacing
            if next_x - spacing > rect.right() and line_h > 0:
                x = rect.x()
                y = y + line_h + spacing
                next_x = x + hint.width() + spacing
                line_h = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x = next_x
            line_h = max(line_h, hint.height())
        return y + line_h - rect.y()


class _PositionChip(QLabel):
    """Clickable pill-shaped range label that mirrors the report's
    `.pos-range` styling — primary-blue border + text, fills on hover."""

    clicked = pyqtSignal(int, int)

    def __init__(self, token: str, parent=None):
        super().__init__(token, parent)
        self._token = token
        try:
            start_str, end_str = token.split("-", 1)
            self._start = int(start_str)
            self._end = int(end_str)
        except ValueError:
            self._start = self._end = None
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setStyleSheet(
            f"""
            QLabel {{
                border: 1px solid {COLORS.primary};
                border-radius: 4px;
                color: {COLORS.primary};
                background-color: white;
                padding: 1px 6px;
            }}
            QLabel:hover {{
                background-color: {COLORS.primary};
                color: white;
            }}
            """
        )

    def mousePressEvent(self, event):
        """Emit ``clicked(start, end)`` on left-click for a valid range."""
        if event.button() == Qt.LeftButton and self._start is not None:
            self.clicked.emit(self._start, self._end)
        super().mousePressEvent(event)


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
        """Re-fit the widget height to its content after each resize."""
        super().resizeEvent(event)
        self._adjust_height()

    def showEvent(self, event):
        """Re-fit the widget height to its content when first shown."""
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
        """Highlight the 1-based ``[start, end]`` window and scroll it into view."""
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
        """Re-render the sequence so wrap matches the new viewport width."""
        # Re-render BEFORE auto-adjusting height so the height reflects
        # the freshly-computed line count.
        QTextEdit.resizeEvent(self, event)
        self._render()


class SettingsWindow(WizardPage):
    """Second wizard page — previews the parsed inputs before elimination runs."""

    def __init__(self, switch_to_eliminate_callback, back_to_upload_callback):
        super().__init__(
            back_callback=back_to_upload_callback,
            next_callback=switch_to_eliminate_callback,
        )
        self.build()

    def build_body(self, layout):
        """Populate the scrollable body with sequence, patterns, and occurrences."""
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
        content_layout.addWidget(QLabel(f"<h2>Input</h2><h3>{HEADINGS.target_sequence}:</h3>"))

        InputData.coding_positions, InputData.coding_indexes = (
            CodingRegionLocator.get_coding_and_non_coding_regions_positions(
                InputData.cleaned_dna_sequence, InputData.start_codon_identified
            )
        )

        if InputData.coding_indexes is not None and len(InputData.coding_indexes) > 0:
            text = HEADINGS.coding_region_identified.format(
                start=InputData.coding_indexes[0] + 1,
                end=InputData.coding_indexes[1],
            )
            content_layout.addWidget(QLabel(f"<p>{text}:</p>"))

        view = _AutoFitSequenceView(
            InputData.cleaned_dna_sequence,
            InputData.coding_indexes,
            max_height=SIZES.sequence_height,
        )
        view.setStyleSheet(card_text_edit_qss())
        content_layout.addWidget(view)
        self._sequence_view = view

    def _add_unwanted_patterns(self, content_layout):
        content_layout.addWidget(QLabel(f"<h3>{HEADINGS.unwanted_patterns}:</h3>"))

        html = f"<p>{SequenceUtils.get_patterns(InputData.unwanted_patterns)}</p>"
        view = _AutoHeightHtmlView(html)
        view.setStyleSheet(card_text_edit_qss())
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
            QLabel(f"<h3>{HEADINGS.unwanted_pattern_occurrences}:</h3>")
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

            cell_widget = QWidget()
            flow = _FlowLayout(cell_widget, margin=6, spacing=4)
            cell_widget.setLayout(flow)

            if row["Positions"]:
                for tok in row["Positions"]:
                    chip = _PositionChip(tok)
                    chip.clicked.connect(self._on_position_chip_clicked)
                    flow.addWidget(chip)
            else:
                flow.addWidget(QLabel("—"))

            table.setCellWidget(r, 2, cell_widget)
            pattern_labels.append((r, cell_widget))

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
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setFocusPolicy(Qt.NoFocus)
        table.horizontalHeader().setMinimumHeight(SIZES.table_header_min_h)
        table.verticalHeader().setDefaultSectionSize(SIZES.table_row_default_h)
        table.setCornerButtonEnabled(False)
        table.setStyleSheet(table_qss() + " QHeaderView::section { padding: 4px 10px; }")
        table.setMinimumHeight(SIZES.scroll_area_max_inline * 2)

        def resize_rows():
            """Resize each row to fit its wrapped chip flow at the current column width."""
            col_w = table.columnWidth(2) - 12  # subtract flow margins
            if col_w <= 0:
                return
            for row_idx, widget in pattern_labels:
                layout = widget.layout()
                if layout is not None and layout.hasHeightForWidth():
                    h = layout.heightForWidth(col_w)
                else:
                    h = widget.sizeHint().height()
                table.setRowHeight(row_idx, max(SIZES.table_row_default_h, h + 12))

        header.sectionResized.connect(
            lambda idx, *_: resize_rows() if idx == 2 else None
        )
        QTimer.singleShot(0, resize_rows)

        content_layout.addWidget(table)

    def _on_position_chip_clicked(self, start: int, end: int):
        if self._sequence_view is None:
            return
        self._sequence_view.set_highlight_range(start, end)

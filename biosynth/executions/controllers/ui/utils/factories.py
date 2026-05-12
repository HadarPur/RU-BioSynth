"""Layout-builder helpers for the BioSynth GUI.

These functions take a parent layout and return a configured widget already
attached to it. They centralize the boilerplate of creating buttons,
spinboxes, text edits, drop targets, scroll areas, and tables.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from biosynth.executions.controllers.ui.theme import (
    FONTS,
    LABELS,
    MARGINS,
    SIZES,
    placeholder_label_qss,
    scroll_area_borderless_qss,
    table_qss,
    text_edit_transparent_only_qss,
)
from biosynth.executions.controllers.ui.utils.file_actions import (
    copy_to_clipboard,
    download_file,
    save_to_file,
)
from biosynth.executions.controllers.ui.widgets import (
    DropTableWidget,
    DropTextEdit,
    ToggleSwitch,
)
from biosynth.utils.file_utils import resource_path


def add_intro(layout, row=0, column=0):
    intro_text = (
        "Welcome to the BioSynth App!\n\n"
        "To begin, upload the following files and optionally adjust substitution costs."
    )
    intro_label = QLabel(intro_text)
    intro_label.setWordWrap(True)
    intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    required_files_text = (
        "Required files:\n"
        "• Target DNA sequence file\n"
        "• Unwanted patterns file\n"
        "• Codon usage file"
    )
    required_label = QLabel(required_files_text)
    required_label.setWordWrap(True)
    required_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    optional_costs_text = (
        "Optional substitution costs:\n"
        "• Transitions substitutions in non-coding regions (default: 1.0)\n"
        "• Transversions substitutions in non-coding regions (default: 2.0)\n"
        "• Non-synonymous substitutions in coding regions (default: 100.0)"
    )
    optional_label = QLabel(optional_costs_text)
    optional_label.setWordWrap(True)
    optional_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    bottom_text = (
        "Once you're done, BioSynth will optimize your sequence.\n"
        "Let’s get started!"
    )
    bottom_label = QLabel(bottom_text)
    bottom_label.setWordWrap(True)
    bottom_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    mid_layout = QHBoxLayout()
    mid_layout.addWidget(required_label)
    mid_layout.addWidget(optional_label)

    container = QWidget()
    container_layout = QVBoxLayout(container)
    container_layout.addWidget(intro_label)
    container_layout.addLayout(mid_layout)
    container_layout.addWidget(bottom_label)

    layout.addWidget(container, row, column)

    return intro_label, required_label, optional_label, bottom_label


def add_png_logo(layout, row=0, column=0):
    frame = QFrame()
    frame_layout = QHBoxLayout(frame)
    frame_layout.setContentsMargins(*MARGINS.frame_padding)

    image_path = resource_path("images/BioSynth-Transparent.png")
    logo = QLabel()
    pixmap = QPixmap(image_path)
    logo.setPixmap(pixmap)
    logo.setFixedSize(SIZES.logo_w, SIZES.logo_h)
    logo.setScaledContents(True)

    frame_layout.addWidget(logo)
    layout.addWidget(frame, row, column, alignment=Qt.AlignTop)


def add_logo_toolbar(layout):
    logo_toolbar = QToolBar()
    logo_toolbar.setMovable(False)

    image_path = resource_path("images/BioSynth-Transparent.png")
    logo_label = QLabel()
    pixmap = QPixmap(image_path)
    logo_label.setPixmap(pixmap)
    logo_label.setFixedSize(SIZES.logo_w, SIZES.logo_h)
    logo_label.setScaledContents(True)

    logo_toolbar.addWidget(logo_label)
    layout.addToolBar(Qt.TopToolBarArea, logo_toolbar)


def add_drop_table(layout, placeholder, columns, headers, drop_callback):
    table = DropTableWidget(drop_callback=drop_callback)
    table.setColumnCount(columns)
    table.setHorizontalHeaderLabels(headers)
    # Match the body-text size used everywhere else in the UI. Without
    # this, cells fall back to Qt's default UI font which is smaller.
    table.setFont(_code_font())
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    layout.addWidget(table)

    placeholder_label = QLabel(placeholder, table.viewport())
    placeholder_label.setAlignment(Qt.AlignLeft)
    placeholder_label.setStyleSheet(placeholder_label_qss())
    placeholder_label.setAttribute(Qt.WA_TransparentForMouseEvents)
    placeholder_label.show()

    table.placeholder_label = placeholder_label

    def update_placeholder():
        placeholder_label.setVisible(table.rowCount() == 0)

    table.update_placeholder = update_placeholder
    update_placeholder()

    original_resize_event = table.resizeEvent

    def new_resize_event(event):
        placeholder_label.resize(table.viewport().size())
        if original_resize_event:
            original_resize_event(event)

    table.resizeEvent = new_resize_event

    return table


def add_drop_text_edit(layout, placeholder, drop_callback, wrap=None):
    text_edit = DropTextEdit(drop_callback=drop_callback)
    text_edit.setPlaceholderText(placeholder)
    # ``set_content_font`` stores the preference on the widget and
    # re-applies it on every ``FontChange`` — so even when QSS is
    # applied later and forces a widget-font update (which Qt would
    # otherwise propagate onto the document), the entered content
    # keeps rendering in Menlo. The placeholder uses the widget font,
    # so it continues to use the regular UI font from the QSS.
    text_edit.set_content_font(_code_font())
    text_edit.setLineWrapMode(wrap if wrap is not None else QTextEdit.WidgetWidth)
    text_edit.viewport().setCursor(Qt.ArrowCursor)
    layout.addWidget(text_edit)
    return text_edit


def _code_font():
    font = QFont(FONTS.code_family)
    # Pixel size (matches QSS px-based font sizes 1:1) instead of point
    # size, so monospace text renders at the same visual size as the rest
    # of the UI's body text.
    font.setPixelSize(FONTS.body_px)
    return font


def add_text_edit(layout, placeholder, content, wrap=None):
    text_edit = QTextEdit()
    text_edit.setPlaceholderText(placeholder)
    if content:
        text_edit.setPlainText(content)

    text_edit.setFont(_code_font())
    text_edit.setReadOnly(True)
    text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
    text_edit.viewport().setCursor(Qt.ArrowCursor)
    text_edit.setLineWrapMode(wrap if wrap is not None else QTextEdit.WidgetWidth)

    layout.addWidget(text_edit)
    return text_edit


def adjust_text_edit_height(text_edit):
    text_edit.document().setTextWidth(text_edit.viewport().width())
    margins = text_edit.contentsMargins()
    height = int(
        text_edit.document().size().height() + margins.top() + margins.bottom() + 10
    )
    text_edit.setFixedHeight(height)


def adjust_scroll_area_height(scroll_area):
    widget = scroll_area.widget()
    widget.adjustSize()
    widget_height = widget.sizeHint().height()
    new_height = min(SIZES.scroll_area_max_inline, widget_height + SIZES.scroll_padding)
    scroll_area.setFixedHeight(new_height + SIZES.scroll_padding)


def add_text_edit_html(layout, placeholder, content):
    text_edit = QTextEdit()
    text_edit.setPlaceholderText(placeholder)

    # Apply font and document-level CSS BEFORE setHtml so the HTML parses
    # with the right base. Qt's default <pre>/<p> rendering applies its
    # own font-size, which would otherwise shrink the text below body_px.
    text_edit.setFont(_code_font())
    text_edit.setStyleSheet(text_edit_transparent_only_qss())
    text_edit.document().setDefaultStyleSheet(
        f"pre {{ font-size: {FONTS.body_px}px; margin: 0; }} "
        f"p {{ font-size: {FONTS.body_px}px; margin: 0; }}"
    )
    if content:
        text_edit.setHtml(content)

    text_edit.setReadOnly(True)
    text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
    text_edit.viewport().setCursor(Qt.ArrowCursor)

    layout.addWidget(text_edit)
    return text_edit


def add_code_block(parent_layout, text, file_date, update_status):
    layout = QVBoxLayout()
    parent_layout.addLayout(layout)

    code_display = QPlainTextEdit(text)
    # Same monospace font + body_px size as every other "code" view, so
    # the optimized-sequence display matches the rest of the UI.
    code_display.setFont(_code_font())
    code_display.setReadOnly(True)
    layout.addWidget(code_display)

    button_layout = QHBoxLayout()
    layout.addLayout(button_layout)
    button_layout.addStretch(1)

    add_button(
        button_layout, LABELS.download, Qt.AlignRight,
        download_file, (code_display, file_date, update_status,),
        size=(SIZES.button_medium_w, SIZES.button_medium_h),
    )
    add_button(
        button_layout, LABELS.save_as, Qt.AlignRight,
        save_to_file, (code_display, update_status,),
        size=(SIZES.button_medium_w, SIZES.button_medium_h),
    )
    add_button(
        button_layout, LABELS.copy, Qt.AlignRight,
        copy_to_clipboard, (code_display, update_status,),
    )


def add_button(layout, text, alignment=None, callback=None, args=(), size=None):
    bottom_layout = QHBoxLayout()
    layout.addLayout(bottom_layout)

    w, h = size if size is not None else (SIZES.button_w, SIZES.button_h)
    button = QPushButton(text)
    button.setFixedSize(w, h)
    button.setFocusPolicy(Qt.NoFocus)

    if callback is not None:
        if callable(args):
            button.clicked.connect(lambda: callback(*args()))
        else:
            button.clicked.connect(lambda: callback(*args))

    bottom_layout.addWidget(button, alignment=alignment)
    return button


def add_spinbox(layout, default_value, step=0.01,
                alignment=None, callback=None, args=(), size=None):
    bottom_layout = QHBoxLayout()
    bottom_layout.setContentsMargins(*MARGINS.spinbox_row)
    layout.addLayout(bottom_layout)

    if args and isinstance(args[0], str):
        label = QLabel(str(args[0]))
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        bottom_layout.addWidget(label, stretch=4)

    w, h = size if size is not None else (SIZES.spinbox_w, SIZES.spinbox_h)
    spinbox = QDoubleSpinBox()
    spinbox.setMinimum(0.0)
    spinbox.setMaximum(2147483647.0)
    spinbox.setValue(default_value)
    spinbox.setSingleStep(step)
    spinbox.setFixedSize(w, h)
    spinbox.setFocusPolicy(Qt.StrongFocus)

    if callback is not None:
        spinbox.valueChanged.connect(lambda val: callback(val))

    bottom_layout.addWidget(spinbox, alignment=alignment, stretch=1)
    return spinbox


def add_toggle(layout, default_value=False,
               alignment=None, callback=None, args=(), size=None):
    bottom_layout = QHBoxLayout()
    bottom_layout.setContentsMargins(*MARGINS.spinbox_row)
    layout.addLayout(bottom_layout)

    if args and isinstance(args[0], str):
        label = QLabel(str(args[0]))
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        bottom_layout.addWidget(label, stretch=4)

    w, h = size if size is not None else (SIZES.toggle_w, SIZES.toggle_h)
    toggle = ToggleSwitch()
    toggle.setChecked(default_value)
    toggle.setFixedSize(w, h)
    toggle.setFocusPolicy(Qt.StrongFocus)

    if callback is not None:
        toggle.toggled.connect(lambda val: callback(val))

    bottom_layout.addWidget(toggle, alignment=alignment, stretch=1)
    return toggle


def create_scroll_area(parent_layout):
    scroll_area = QScrollArea()
    # Minimum (not fixed) so the area grows when the window is resized.
    scroll_area.setMinimumHeight(SIZES.scroll_area_height)
    scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet(scroll_area_borderless_qss())
    scroll_area.setAlignment(Qt.AlignTop)

    parent_layout.addWidget(scroll_area)

    content_widget = QWidget()
    scroll_area.setWidget(content_widget)

    content_layout = QVBoxLayout(content_widget)
    content_layout.setAlignment(Qt.AlignTop)

    return scroll_area, content_widget, content_layout


def make_item(value):
    item = QTableWidgetItem(str(value))
    item.setTextAlignment(Qt.AlignCenter)
    return item

def create_table_from_data(data):
    """Build a QTableWidget from a dict, nested dict, or list of dicts."""
    table = QTableWidget()

    if not data:
        table.setRowCount(0)
        table.setColumnCount(0)
        return table

    table.setFont(_code_font())

    if isinstance(data, list) and isinstance(data[0], dict):
        headers = list(data[0].keys())
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))

        for row, row_data in enumerate(data):
            for col, header in enumerate(headers):
                value = row_data.get(header, "")
                table.setItem(row, col, make_item(value))

    elif isinstance(data, dict):
        first_value = next(iter(data.values()))

        if isinstance(first_value, dict):
            headers = ["Key"] + list(first_value.keys())
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(data))

            for row, (key, values) in enumerate(data.items()):
                table.setItem(row, 0, QTableWidgetItem(str(key)))
                for col, header in enumerate(headers[1:], start=1):
                    value = values.get(header, "")
                    table.setItem(row, col, make_item(value))

        else:
            headers = ["Key", "Value"]
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(data))

            for row, (key, value) in enumerate(data.items()):
                table.setItem(row, 0, QTableWidgetItem(str(key)))
                table.setItem(row, 1, make_item(value))

    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

    return table

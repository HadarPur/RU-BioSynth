from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QMessageBox

from biosynth.data.app_data import InputData
from biosynth.executions.controllers.ui.window_utils import FloatingScrollIndicator, add_button, add_text_edit_html, \
    add_text_edit, \
    adjust_text_edit_height, adjust_scroll_area_height, create_scroll_area
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils


class SettingsWindow(QWidget):
    def __init__(self, switch_to_eliminate_callback, back_to_upload_callback):
        super().__init__()
        self.next_button = None
        self.floating_btn = None

        self.init_ui(back_to_upload_callback, switch_to_eliminate_callback)

    def init_ui(self, back_callback, next_callback):
        layout = QVBoxLayout(self)

        # Top Layout
        self.add_top_layout(layout, back_callback)

        # Middle layout with information
        self.add_middle_layout(layout)

        # Bottom layout
        self.add_bottom_layout(layout, next_callback)

    def add_top_layout(self, layout, back_callback):
        # Top-level layout
        add_button(layout, 'Back', Qt.AlignLeft, back_callback, ())
        return layout

    def add_middle_layout(self, layout):
        # Middle layout
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 10, 20, 10)
        layout.addLayout(middle_layout)

        scroll_area, content_widget, content_layout = create_scroll_area(middle_layout)

        # Adding target sequence layout
        self.add_target_sequence_layout(content_layout)

        # Adding unwanted patterns layout
        self.add_unwanted_patterns_layout(content_layout)

        # Add a stretch to push all content to the top
        content_layout.addStretch(1)

        # Add floating button
        self.floating_btn = FloatingScrollIndicator(parent=self, scroll_area=scroll_area)
        scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda min_val, max_val: self.floating_btn.on_scroll(scroll_area.verticalScrollBar().value())
        )

    def add_bottom_layout(self, layout, next_callback):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(bottom_layout)

        next_button = add_button(bottom_layout, 'Next', Qt.AlignRight)
        next_button.clicked.connect(
            lambda: next_callback())

    def add_target_sequence_layout(self, content_layout):
        label_html = f"""
            <h2>Input</h2>
            <h3>Target Sequence:</h3>
        """
        label = QLabel(label_html)
        content_layout.addWidget(label)

        # Extract coding regions
        InputData.coding_positions, InputData.coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(
            InputData.cleaned_dna_sequence, InputData.start_codon_identified)

        highlighted_sequence = f"<pre>{SequenceUtils.highlight_sequences_to_html(InputData.cleaned_dna_sequence, InputData.coding_indexes, line_length=96, returnBr=True)}</pre>"
        if InputData.coding_indexes is not None and len(InputData.coding_indexes) > 0:
            label_html = f"""
                <p>A coding region was identified in the target sequence at positions {InputData.coding_indexes[0] + 1} - {InputData.coding_indexes[1]}:</p>
            """


        else:
            label_html = f"""
                <p>A coding region identified in the provided target sequence</p>
            """

        label = QLabel(label_html)
        content_layout.addWidget(label)

        text_edit = add_text_edit_html(content_layout, "", highlighted_sequence)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
                margin-right: 25px;
            }
        """)

    def add_unwanted_patterns_layout(self, content_layout):
        label_html = f"""
            <h3>Unwanted Patterns:</h3>
        """
        label = QLabel(label_html)
        content_layout.addWidget(label)

        unwanted_pattern = f"<p>{SequenceUtils.get_patterns(InputData.unwanted_patterns)}</p>"
        text_edit = add_text_edit_html(content_layout, "", unwanted_pattern)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
                margin-right: 25px;
            }
        """)

    def resizeEvent(self, event):
        self.floating_btn.raise_()  # Bring to front
        self.floating_btn.reposition()
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from executions.controllers.ui.window_utils import add_button, add_text_edit_html
from executions.execution_utils import eliminate_unwanted_patterns
from data.app_data import InputData, EliminationData


class EliminationWindow(QWidget):
    def __init__(self, switch_to_results_callback, updated_coding_positions, back_to_processing_callback):
        super().__init__()
        self.switch_to_results_callback = switch_to_results_callback
        self.updated_coding_positions = updated_coding_positions

        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None

        self.yes_button = None
        self.no_button = None
        self.next_button = None

        self.init_ui(back_to_processing_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)
        add_button(layout, 'Back', Qt.AlignLeft, callback)
        self.display_info(layout)

    def display_info(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(middle_layout)

        content_layout = QVBoxLayout()
        middle_layout.addLayout(content_layout)

        eliminate_unwanted_patterns(InputData.dna_sequence, InputData.unwanted_patterns, self.updated_coding_positions)

        info = EliminationData.info.replace("\n", "<br>")
        label_html = f"""
            <h2>Elimination Process:</h2>
            <p>{info}</p>
        """
        info_text_edit = add_text_edit_html(content_layout, "", label_html)
        info_text_edit.setMinimumHeight(650)

        # Adjust size policy to expand with content
        info_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        document = info_text_edit.document()
        document.contentsChanged.connect(lambda: info_text_edit.setMaximumHeight(document.size().height()))

        content_layout.addStretch(1)  # This ensures that the layout can expand and push content

        # Add next button to the bottom layout
        add_button(layout, 'Next', Qt.AlignRight, self.switch_to_results_callback, lambda: (self.updated_coding_positions,))

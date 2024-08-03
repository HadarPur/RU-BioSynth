from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from executions.controllers.ui.window_utils import add_button, add_text_edit_html
from executions.execution_utils import eliminate_unwanted_patterns


class EliminationWindow(QWidget):
    def __init__(self, switch_to_results_callback, dna_sequence, unwanted_patterns, original_coding_regions,
                 original_region_list,
                 selected_regions_to_exclude,
                 selected_region_list, back_to_processing_callback):
        super().__init__()
        self.switch_to_results_callback = switch_to_results_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = unwanted_patterns
        self.original_coding_regions = original_coding_regions
        self.original_region_list = original_region_list
        self.selected_regions_to_exclude = selected_regions_to_exclude
        self.selected_region_list = selected_region_list

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

        info, detailed_changes, target_seq, min_cost = eliminate_unwanted_patterns(self.dna_sequence,
                                                                                   self.unwanted_patterns,
                                                                                   self.selected_region_list)

        info = info.replace("\n", "<br>")
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
        add_button(layout, 'Next', Qt.AlignRight, self.switch_to_results_callback,
                   lambda: (self.original_coding_regions,
                            self.original_region_list,
                            self.selected_regions_to_exclude,
                            self.selected_region_list, target_seq,
                            min_cost, detailed_changes))

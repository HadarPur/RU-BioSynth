from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, save_report_locally
from utils.display_utils import SequenceUtils
from executions.ui.layout_utils import add_back_button


class EliminationWindow(QWidget):
    def __init__(self, switch_to_results_callback, dna_sequence, unwanted_patterns, original_coding_regions,
                 original_region_list,
                 selected_regions_to_exclude,
                 selected_region_list, back_to_processing_callback):
        super().__init__()
        self.switch_to_results_callback = switch_to_results_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())
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
        add_back_button(layout, callback)
        self.display_info(layout)

    def display_info(self, layout):
        self.middle_layout = QVBoxLayout()
        layout.addLayout(self.middle_layout)

        infoLabel = QLabel()
        self.middle_layout.addWidget(infoLabel, alignment=Qt.AlignTop)

        info, target_seq, min_cost = eliminate_unwanted_patterns(self.dna_sequence, self.unwanted_patterns,
                                                                 self.selected_region_list)

        infoLabel.setText(info)

        # Spacer to push other widgets to the top
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a horizontal layout for the bottom section
        self.bottom_layout = QHBoxLayout()
        layout.addLayout(self.bottom_layout)

        # Add a stretch to push the next button to the right
        self.bottom_layout.addStretch(1)

        # Add next button to the bottom layout
        self.next_button = QPushButton('Next')
        self.next_button.setFixedSize(60, 30)
        self.next_button.clicked.connect(
            lambda: self.switch_to_results_callback(self.original_coding_regions, self.original_region_list,
                                                    self.selected_regions_to_exclude,
                                                    self.selected_region_list, target_seq, min_cost))

        self.bottom_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

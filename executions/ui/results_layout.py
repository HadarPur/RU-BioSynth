from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, save_report_locally
from utils.display_utils import SequenceUtils

from executions.ui.layout_utils import add_back_button


class ResultsWindow(QWidget):
    def __init__(self, dna_sequence, unwanted_patterns, original_coding_regions, original_region_list,
                 selected_regions_to_exclude, selected_region_list, target_seq, min_cost,
                 back_to_elimination_callback):
        super().__init__()
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())
        self.original_coding_regions = original_coding_regions
        self.original_region_list = original_region_list
        self.selected_regions_to_exclude = selected_regions_to_exclude
        self.selected_region_list = selected_region_list
        self.target_seq = target_seq
        self.min_cost = min_cost

        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None

        self.yes_button = None
        self.no_button = None
        self.done_button = None

        self.init_ui(back_to_elimination_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)

        callback_args = (self.original_coding_regions, self.original_region_list,
                         self.selected_regions_to_exclude, self.selected_region_list)
        add_back_button(layout, callback, callback_args)

        self.display_info(layout)

    def display_info(self, layout):
        self.middle_layout = QVBoxLayout()
        layout.addLayout(self.middle_layout)

        infoLabel = QLabel()
        self.middle_layout.addWidget(infoLabel, alignment=Qt.AlignTop)

        # Mark non-equal codons and print the target sequence
        marked_input_seq, marked_target_seq, marked_seq, region_list_target = mark_non_equal_codons(
            self.selected_region_list, self.target_seq)

        info = marked_seq
        info += SequenceUtils.get_sequence("Target DNA sequence", self.target_seq)

        infoLabel.setText(info)

        # Spacer to push other widgets to the top
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.prompt_report(self.middle_layout, self.target_seq, marked_input_seq, marked_target_seq,
                           self.original_coding_regions, self.original_region_list, self.selected_regions_to_exclude,
                           self.selected_region_list, self.min_cost)

        # Create a horizontal layout for the bottom section
        self.bottom_layout = QHBoxLayout()
        layout.addLayout(self.bottom_layout)

        # Add a stretch to push the next button to the right
        self.bottom_layout.addStretch(1)

        # Add next button to the bottom layout
        self.done_button = QPushButton('Done')
        self.done_button.setFixedSize(60, 30)
        self.done_button.setEnabled(False)
        self.done_button.clicked.connect(QApplication.instance().quit)  # Connect to quit the application
        self.bottom_layout.addWidget(self.done_button, alignment=Qt.AlignRight)

    def prompt_report(self, layout, target_seq, marked_input_seq, marked_target_seq, original_coding_regions,
                      original_region_list, selected_regions_to_exclude, selected_region_list, min_cost):
        # Create a horizontal layout for the entire prompt
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(10)  # Adjust spacing between elements

        # Create and add the question label to the horizontal layout
        question_label = QLabel("Do you want to save the report? (yes/no): ")
        prompt_layout.addWidget(question_label)

        # Create the 'Yes' button
        self.yes_button = QPushButton('Yes')
        self.yes_button.setFixedSize(60, 30)
        self.yes_button.clicked.connect(
            lambda: self.save_report(layout, self.dna_sequence, target_seq, marked_input_seq, marked_target_seq,
                                     self.unwanted_patterns,
                                     original_coding_regions, original_region_list,
                                     selected_regions_to_exclude, selected_region_list,
                                     min_cost))

        # Create the 'No' button
        self.no_button = QPushButton('No')
        self.no_button.setFixedSize(60, 30)
        self.no_button.clicked.connect(
            lambda: self.do_not_save_report(layout))

        # Add the buttons to the horizontal layout
        prompt_layout.addWidget(self.yes_button)
        prompt_layout.addWidget(self.no_button)

        # Add a spacer to push the buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        prompt_layout.addItem(spacer)

        # Add the entire horizontal layout to the parent layout
        layout.addLayout(prompt_layout)

    def save_report(self, layout, seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                    original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list,
                    min_cost):
        if not self.no_button.isEnabled():
            return

        report_path = save_report_locally(seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                                          original_coding_regions, original_region_list, selected_regions_to_exclude,
                                          selected_region_list,
                                          min_cost)
        report_path += "\nReport saved successfully!"

        message_label = QLabel(report_path)
        layout.addWidget(message_label)

        self.no_button.setEnabled(False)
        self.done_button.setEnabled(True)

    def do_not_save_report(self, layout):
        if not self.yes_button.isEnabled():
            return

        message = "Report not saved."
        message_label = QLabel(message)
        layout.addWidget(message_label)

        self.yes_button.setEnabled(False)
        self.done_button.setEnabled(True)

import copy

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAHighlighter


class ProcessWindow(QWidget):
    def __init__(self, switch_to_eliminate_callback, dna_sequence, unwanted_patterns, back_to_upload_callback):
        super().__init__()
        self.switch_to_eliminate_callback = switch_to_eliminate_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())
        self.back_to_upload_callback = back_to_upload_callback

        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None
        self.start_elimination_button = None
        self.yes_button = None
        self.no_button = None
        self.region_selector = None
        self.submit_button = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.add_back_button(layout)
        self.display_info(layout)

    def add_back_button(self, layout):
        self.top_layout = QHBoxLayout()
        layout.addLayout(self.top_layout)

        # Add back button to the top layout
        back_button = QPushButton('Back')
        back_button.setFixedSize(60, 30)
        back_button.clicked.connect(self.back_to_upload_callback)
        self.top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

    def display_info(self, layout):
        self.middle_layout = QVBoxLayout()
        layout.addLayout(self.middle_layout)

        infoLabel = QLabel()
        self.middle_layout.addWidget(infoLabel, alignment=Qt.AlignTop)

        original_region_list = DNAHighlighter.get_coding_and_non_coding_regions(self.dna_sequence)
        original_coding_regions, coding_indexes = DNAHighlighter.extract_coding_regions_with_indexes(
            original_region_list)
        highlighted_sequence = SequenceUtils.highlight_sequences_to_html(original_region_list)

        info = SequenceUtils.get_sequence("DNA sequence", self.dna_sequence)
        info += SequenceUtils.get_patterns(self.unwanted_patterns)
        info += SequenceUtils.get_highlighted_sequence(highlighted_sequence)
        info += f"\n\nNumber of coding regions is: {len(original_coding_regions)}\n"

        infoLabel.setText(info)

        if len(original_coding_regions) > 0:
            self.prompt_coding_regions_decision(self.middle_layout, original_coding_regions, original_region_list,
                                                coding_indexes, self.unwanted_patterns)

        # Spacer to push other widgets to the top
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a horizontal layout for the bottom section
        self.bottom_layout = QHBoxLayout()
        layout.addLayout(self.bottom_layout)

        # Add a stretch to push the next button to the right
        self.bottom_layout.addStretch(1)

        # Add next button to the bottom layout
        self.start_elimination_button = QPushButton('Start Elimination')
        self.start_elimination_button.setFixedSize(150, 30)
        self.start_elimination_button.setEnabled(False)
        self.bottom_layout.addWidget(self.start_elimination_button, alignment=Qt.AlignRight)

    def prompt_coding_regions_decision(self, layout, original_coding_regions, original_region_list, coding_indexes,
                                       unwanted_patterns):
        # Create a horizontal layout for the entire prompt
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(10)  # Adjust spacing between elements

        # Create and add the question label to the horizontal layout
        question_label = QLabel("Do you want to proceed with all coding regions?")
        prompt_layout.addWidget(question_label)

        # Create the 'Yes' button
        self.yes_button = QPushButton('Yes')
        self.yes_button.setFixedSize(60, 30)
        self.yes_button.clicked.connect(
            lambda: self.select_all_regions(original_coding_regions, original_region_list))

        # Create the 'No' button
        self.no_button = QPushButton('No')
        self.no_button.setFixedSize(60, 30)
        self.no_button.clicked.connect(
            lambda: self.select_regions_to_exclude(layout, original_coding_regions, original_region_list,
                                                   coding_indexes, unwanted_patterns))

        # Add the buttons to the horizontal layout
        prompt_layout.addWidget(self.yes_button)
        prompt_layout.addWidget(self.no_button)

        # Add a spacer to push the buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        prompt_layout.addItem(spacer)

        # Add the entire horizontal layout to the parent layout
        layout.addLayout(prompt_layout)

    def select_all_regions(self, original_coding_regions, original_region_list):
        if not self.no_button.isEnabled():
            return

        self.no_button.setEnabled(False)

        self.start_elimination_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list, None,
                                                      original_region_list))
        self.start_elimination_button.setEnabled(True)
        self.start_elimination_button.setFocus(True)

    def select_regions_to_exclude(self, layout, original_coding_regions, original_region_list, coding_indexes,
                                  unwanted_patterns):
        if not self.yes_button.isEnabled():
            return

        self.yes_button.setEnabled(False)
        self.region_selector = RegionSelector(layout, original_coding_regions, original_region_list, coding_indexes,
                                              unwanted_patterns, self.handle_results)
        layout.addWidget(self.region_selector, alignment=Qt.AlignTop)

    def handle_results(self, original_coding_regions, original_region_list, selected_regions_to_exclude,
                       selected_region_list):
        self.region_selector.setEnabled(False)

        self.start_elimination_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list,
                                                      selected_regions_to_exclude, selected_region_list))
        self.start_elimination_button.setEnabled(True)
        self.start_elimination_button.setFocus(True)

        exclude = ""
        for index, region in selected_regions_to_exclude.items():
            exclude += f"[{index}]: {region}\n"

        exclude_label = QLabel(f"Selected regions to exclude:\n{exclude}")
        self.middle_layout.addWidget(exclude_label)


class RegionSelector(QWidget):
    def __init__(self, layout, original_coding_regions, original_region_list, coding_indexes, unwanted_patterns,
                 result_callback):
        super().__init__()
        self.original_coding_regions = original_coding_regions
        self.original_region_list = original_region_list
        self.coding_indexes = coding_indexes
        self.unwanted_patterns = unwanted_patterns
        self.result_callback = result_callback

        self.checkboxes = []
        self.submit_button = None

        self.init_ui(layout)

    def init_ui(self, layout):
        instructions_label = QLabel("Check the regions you want to exclude:")
        layout.addWidget(instructions_label)

        for index, region in enumerate(self.original_coding_regions):
            checkbox = QCheckBox(f"[{index + 1}]: {region}")
            layout.addWidget(checkbox)
            self.checkboxes.append((checkbox, region))

        control_buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton('Submit Exclusions')
        self.submit_button.setFixedSize(150, 30)

        self.submit_button.clicked.connect(lambda: self.submit_exclusions())

        control_buttons_layout.addWidget(self.submit_button, alignment=Qt.AlignLeft)
        layout.addLayout(control_buttons_layout)

    def submit_exclusions(self):
        # Prompt the user for confirmation
        reply = QMessageBox.question(self, 'Confirm Exclusion', 'Do you want to eliminate selected coding regions?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.submit_button.setEnabled(False)
            self.disable_checkboxes()
            original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list = self.handle_coding_region_checkboxes()
            self.result_callback(original_coding_regions, original_region_list, selected_regions_to_exclude,
                                 selected_region_list)

    def handle_coding_region_checkboxes(self):
        # Implementation of the exclusion logic
        original_region_list = copy.deepcopy(self.original_region_list)
        selected_region_list = copy.deepcopy(self.original_region_list)

        original_coding_regions = {}
        selected_regions_to_exclude = {}
        coding_regions_to_exclude = {}

        for index, (checkbox, region) in enumerate(self.checkboxes):
            original_coding_regions[f'{index + 1}'] = region
            if checkbox.isChecked():
                selected_regions_to_exclude[f'{index + 1}'] = region
                coding_regions_to_exclude[index] = region

        # Update the coding regions based on user input
        selected_region_list = DNAHighlighter.update_coding_regions(selected_region_list, self.coding_indexes,
                                                                    coding_regions_to_exclude)

        return original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list

    def disable_checkboxes(self):
        for checkbox, region in self.checkboxes:
            checkbox.setEnabled(False)

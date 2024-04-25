import copy

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QScrollArea

from executions.ui.layout_utils import add_back_button, remove_item_at
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAHighlighter


class ProcessWindow(QWidget):
    def __init__(self, switch_to_eliminate_callback, dna_sequence, unwanted_patterns, back_to_upload_callback):
        super().__init__()
        self.switch_to_eliminate_callback = switch_to_eliminate_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())

        self.scroll = None
        self.start_elimination_button = None
        self.yes_button = None
        self.no_button = None
        self.region_selector = None
        self.submit_button = None

        self.init_ui(back_to_upload_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)
        add_back_button(layout, callback)
        self.display_info(layout)

    def display_info(self, layout):
        middle_layout = QVBoxLayout()
        layout.addLayout(middle_layout)

        self.scroll = QScrollArea()
        middle_layout.addWidget(self.scroll, alignment=Qt.AlignTop)

        content_widget = QWidget()
        self.scroll.setWidget(content_widget)
        self.scroll.setStyleSheet("QScrollArea { border: none; }")
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(650)

        content_layout = QVBoxLayout(content_widget)

        original_region_list = DNAHighlighter.get_coding_and_non_coding_regions(self.dna_sequence)
        original_coding_regions, coding_indexes = DNAHighlighter.extract_coding_regions_with_indexes(
            original_region_list)
        highlighted_sequence = SequenceUtils.highlight_sequences_to_html(original_region_list)

        # Adding formatted text to QLabel
        label_html = f"""
            <h3>DNA Sequence:</h3>
            <p>{self.dna_sequence}</p>
            <h3>Unwanted Patterns:</h3>
            <p>{SequenceUtils.get_patterns(self.unwanted_patterns)}</p>
            <br>
            <h3>Coding Regions:</h3>
            <p>Identify the coding regions within the given DNA sequence and mark them for emphasis:
            <br>
            {SequenceUtils.get_highlighted_sequence(highlighted_sequence)}</p>
            <br>
            <p>Number of coding regions is {len(original_coding_regions)}</p>
        """

        label = QLabel(label_html)
        label.setWordWrap(True)
        content_layout.addWidget(label)

        if len(original_coding_regions) > 0:
            self.prompt_coding_regions_decision(content_layout, original_coding_regions, original_region_list,
                                                coding_indexes, self.unwanted_patterns)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addSpacerItem(self.spacer)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)
        bottom_layout.addStretch(1)

        self.start_elimination_button = QPushButton('Start Elimination')
        self.start_elimination_button.setFixedSize(150, 30)
        self.start_elimination_button.setEnabled(False)
        bottom_layout.addWidget(self.start_elimination_button, alignment=Qt.AlignRight)

    def prompt_coding_regions_decision(self, layout, original_coding_regions, original_region_list, coding_indexes,
                                       unwanted_patterns):
        # Create a horizontal layout for the entire prompt
        prompt_layout = QHBoxLayout()
        container_widget = QWidget()
        prompt_layout.setContentsMargins(0, 0, 0, 0)

        container_widget.setLayout(prompt_layout)
        layout.addWidget(container_widget, alignment=Qt.AlignTop)

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

    def select_all_regions(self, original_coding_regions, original_region_list):
        if not self.no_button.isEnabled():
            return

        self.no_button.setEnabled(False)

        self.start_elimination_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list, None,
                                                      original_region_list))
        self.start_elimination_button.setEnabled(True)

        # Scroll to the bottom after a short delay to ensure the layout updates
        QTimer.singleShot(50, self.scroll_to_bottom)

    def select_regions_to_exclude(self, layout, original_coding_regions, original_region_list, coding_indexes,
                                  unwanted_patterns):
        remove_item_at(layout, 2)
        container_widget = QWidget()
        layout.addWidget(container_widget, alignment=Qt.AlignTop)

        if not self.yes_button.isEnabled():
            return

        self.yes_button.setEnabled(False)
        self.region_selector = RegionSelector(container_widget, original_coding_regions, original_region_list, coding_indexes,
                                              unwanted_patterns, self.handle_results)

        layout.addSpacerItem(self.spacer)

    def handle_results(self, layout, original_coding_regions, original_region_list, selected_regions_to_exclude,
                       selected_region_list):

        self.region_selector.setEnabled(False)

        self.start_elimination_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list,
                                                      selected_regions_to_exclude, selected_region_list))
        self.start_elimination_button.setEnabled(True)

        exclude = ""
        for index, region in selected_regions_to_exclude.items():
            exclude += f"[{index}]: {region}\n"

        exclude_label = QLabel(f"Selected regions to exclude:\n{exclude}")
        layout.addWidget(exclude_label)

        # Scroll to the bottom after a short delay to ensure the layout updates
        QTimer.singleShot(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())


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

    def init_ui(self, parent_layout):
        # Create a new QVBoxLayout for the content of this section
        layout = QVBoxLayout()

        # Add this layout to the parent layout
        parent_layout.setLayout(layout)

        instructions_label = QLabel("Check the regions you want to exclude:")
        layout.addWidget(instructions_label, alignment=Qt.AlignTop)

        for index, region in enumerate(self.original_coding_regions):
            checkbox = QCheckBox(f"[{index + 1}]: {region}")
            layout.addWidget(checkbox, alignment=Qt.AlignTop)
            self.checkboxes.append((checkbox, region))

        control_buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton('Submit Exclusions')
        self.submit_button.setFixedSize(150, 30)
        self.submit_button.clicked.connect(lambda: self.submit_exclusions(layout))
        control_buttons_layout.addWidget(self.submit_button, alignment=Qt.AlignLeft)

        # Add the control buttons layout to the QVBoxLayout for this section
        layout.addLayout(control_buttons_layout)

    def submit_exclusions(self, layout):
        checked_indices = [index for index, (checkbox, region) in enumerate(self.checkboxes) if checkbox.isChecked()]
        if len(checked_indices) <= 0:
            QMessageBox.question(self, 'Error', 'You need to choose one coding region at least to continue', QMessageBox.Ok)
            return

        # Prompt the user for confirmation
        reply = QMessageBox.question(self, 'Confirm', 'Do you want to eliminate selected coding regions?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.submit_button.setEnabled(False)
            self.disable_checkboxes()
            original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list = self.handle_coding_region_checkboxes()
            self.result_callback(layout, original_coding_regions, original_region_list, selected_regions_to_exclude,
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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout
from utils.dna_utils import DNAHighlighter
from utils.display_utils import SequenceUtils


class ProcessWindow(QWidget):
    def __init__(self, dna_sequence, unwanted_patterns, back_to_upload_callback):
        super().__init__()
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())  # Convert to set
        self.back_to_upload_callback = back_to_upload_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Create a horizontal layout for the top section
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        # Add back button to the top layout
        back_button = QPushButton('Back')
        back_button.setFixedSize(60, 30)  # Set smaller size
        back_button.clicked.connect(self.back_to_upload_callback)
        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        infoLabel = QLabel()
        layout.addWidget(infoLabel)

        regions = DNAHighlighter.get_coding_and_non_coding_regions(self.dna_sequence)
        coding_regions, _ = DNAHighlighter.extract_coding_regions_with_indexes(regions)
        highlighted_sequence = SequenceUtils.highlight_sequences_to_html(regions)

        info = SequenceUtils.get_sequence("DNA sequence", self.dna_sequence)
        info += SequenceUtils.get_patterns(self.unwanted_patterns)
        info += SequenceUtils.get_highlighted_sequence(highlighted_sequence)
        info += f"\n\nNumber of coding regions is: {len(coding_regions)}\n"

        infoLabel.setText(info)

        if len(coding_regions) > 0:
            self.promptCodingRegionsDecision(layout, coding_regions, self.unwanted_patterns)

    def promptCodingRegionsDecision(self, layout, coding_regions, unwanted_patterns):
        decision_layout = QHBoxLayout()
        question_label = QLabel("Do you want to proceed with all coding regions?")
        decision_layout.addWidget(question_label)

        yes_button = QPushButton('Yes')
        no_button = QPushButton('No')
        yes_button.clicked.connect(lambda: self.eliminateRegions(coding_regions, unwanted_patterns))
        no_button.clicked.connect(lambda: self.selectRegionsToExclude(coding_regions, unwanted_patterns))

        decision_layout.addWidget(yes_button)
        decision_layout.addWidget(no_button)

        layout.addLayout(decision_layout)

    def selectRegionsToExclude(self, coding_regions, unwanted_patterns):
        region_selector = RegionSelector(coding_regions, unwanted_patterns, self.back_to_upload_callback)
        self.layout().addWidget(region_selector)


class RegionSelector(QWidget):
    def __init__(self, coding_regions, unwanted_patterns, back_to_upload_callback):
        super().__init__()
        self.coding_regions = coding_regions
        self.unwanted_patterns = unwanted_patterns
        self.back_to_upload_callback = back_to_upload_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        instructions_label = QLabel("Check the regions you want to exclude:")
        layout.addWidget(instructions_label)

        for index, region in enumerate(self.coding_regions):
            checkbox = QCheckBox(f"Region {index + 1}: {region}")
            layout.addWidget(checkbox)

        control_buttons_layout = QHBoxLayout()
        submit_button = QPushButton('Submit Exclusions')
        cancel_button = QPushButton('Cancel')
        submit_button.clicked.connect(self.submitExclusions)
        cancel_button.clicked.connect(self.back_to_upload_callback)

        control_buttons_layout.addWidget(submit_button)
        control_buttons_layout.addWidget(cancel_button)
        layout.addLayout(control_buttons_layout)

    def submitExclusions(self):
        selected_regions = [region for checkbox, region in self.coding_regions.items() if checkbox.isChecked()]
        print("Selected regions to exclude:", selected_regions)
        # Implement the exclusion logic here

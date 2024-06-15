import copy

from PyQt5.QtCore import Qt, QEvent, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QMessageBox

from executions.ui.layout_utils import add_button, add_text_edit_html, add_text_edit, adjust_text_edit_height, \
    adjust_scroll_area_height
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAUtils
from utils.input_utils import UserInputHandler


class ProcessWindow(QWidget):
    def __init__(self, switch_to_eliminate_callback, dna_sequence, unwanted_patterns, back_to_upload_callback):
        super().__init__()
        self.switch_to_eliminate_callback = switch_to_eliminate_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = unwanted_patterns

        self.scroll = None
        self.next_button = None
        self.yes_button = None
        self.no_button = None
        self.region_selector = None
        self.submit_button = None
        self.animation = None

        self.content_widget = None

        self.init_ui(back_to_upload_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)
        add_button(layout, 'Back', Qt.AlignLeft, callback, ())
        self.display_info(layout)

    def display_info(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 10, 20, 10)
        layout.addLayout(middle_layout)

        self.scroll = QScrollArea()
        self.scroll.setFixedHeight(650)  # Set the maximum height for scrolling to begin.
        self.scroll.setWidgetResizable(True)  # Ensure the scroll area can resize to its content.
        self.scroll.setStyleSheet("QScrollArea { border: none; }")
        self.scroll.setAlignment(Qt.AlignTop)

        middle_layout.addWidget(self.scroll, alignment=Qt.AlignTop)

        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setAlignment(Qt.AlignTop)  # Align the content_layout to the top

        # Adding formatted text to QLabel
        label_html = f"""
            <h2>Input</h2>
            <h3>DNA Sequence:</h3>
        """
        label = QLabel(label_html)
        content_layout.addWidget(label)

        content = f'{self.dna_sequence}'
        text_edit = add_text_edit(content_layout, "", content)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
            }
        """)

        label_html = f"""
            <h3>Unwanted Patterns:</h3>
        """
        label = QLabel(label_html)
        content_layout.addWidget(label)

        content = f'{SequenceUtils.get_patterns(self.unwanted_patterns)}'
        text_edit = add_text_edit(content_layout, "", content)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
            }
        """)

        original_region_list = DNAUtils.get_coding_and_non_coding_regions(self.dna_sequence)
        original_coding_regions, coding_indexes = DNAUtils.extract_coding_regions_with_indexes(
            original_region_list)
        highlighted_sequence = SequenceUtils.highlight_sequences_to_html(original_region_list)

        # Adding formatted text to QLabel
        label_html = f"""
            <br>
            <h2>DNA Elimination</h2>
            <h3>Coding Regions:</h3>
            <p>Identify the coding regions within the given DNA sequence and mark them for emphasis:
        """

        label = QLabel(label_html)
        content_layout.addWidget(label)

        label_html = f'''
        <p style="word-wrap: break-word;">{highlighted_sequence}</p>
        '''

        text_edit = add_text_edit_html(content_layout, "", label_html)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
            }
        """)

        label_html = f"""
            <p>Number of coding regions is {len(original_coding_regions)}</p>
        """

        label = QLabel(label_html)
        content_layout.addWidget(label)

        if len(original_coding_regions) > 0:
            self.prompt_coding_regions_decision(content_layout, original_coding_regions, original_region_list,
                                                coding_indexes, self.unwanted_patterns)

        # Add a stretch to push all content to the top
        content_layout.addStretch(1)

        self.next_button = add_button(layout, 'Next', Qt.AlignRight)
        self.next_button.setEnabled(False)

        QTimer.singleShot(50, self.scroll_to_bottom)  # Add this line

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
        callback_args = (original_coding_regions, original_region_list)
        self.yes_button = add_button(prompt_layout, 'Yes', Qt.AlignLeft, self.select_all_regions, callback_args)

        # Create the 'No' button
        callback_args = (layout, original_coding_regions, original_region_list,
                         coding_indexes, unwanted_patterns)
        self.no_button = add_button(prompt_layout, 'No', Qt.AlignLeft, self.select_regions_to_exclude, callback_args)

        # Add a spacer to push the buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        prompt_layout.addItem(spacer)

    def select_all_regions(self, original_coding_regions, original_region_list):
        if not self.no_button.isEnabled() or self.next_button.isEnabled():
            return

        self.no_button.setEnabled(False)
        original_coding_regions = UserInputHandler.get_coding_regions_list(original_coding_regions)

        self.next_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list, None,
                                                      original_region_list))
        self.next_button.setEnabled(True)

    def select_regions_to_exclude(self, layout, original_coding_regions, original_region_list, coding_indexes,
                                  unwanted_patterns):

        if not self.yes_button.isEnabled() or self.next_button.isEnabled():
            return

        container_widget = QWidget()
        layout.addWidget(container_widget, alignment=Qt.AlignTop)

        self.yes_button.setEnabled(False)
        self.region_selector = RegionSelector(container_widget, original_coding_regions, original_region_list,
                                              coding_indexes,
                                              unwanted_patterns, self.handle_results)

        QTimer.singleShot(50, self.scroll_to_bottom)  # Add this line

    def handle_results(self, layout, original_coding_regions, original_region_list, selected_regions_to_exclude,
                       selected_region_list):

        self.region_selector.setEnabled(False)

        self.next_button.clicked.connect(
            lambda: self.switch_to_eliminate_callback(original_coding_regions, original_region_list,
                                                      selected_regions_to_exclude, selected_region_list))
        self.next_button.setEnabled(True)

        label = QLabel(f"\nSelected regions to exclude:")
        layout.addWidget(label, alignment=Qt.AlignTop)

        # Create a new QVBoxLayout for the content of this section
        scroll_area = QScrollArea()  # Create a scroll area
        scroll_area.setAlignment(Qt.AlignTop)
        scroll_area.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        scroll_content = QWidget()  # Create a widget to hold the content

        exclude_layout = QVBoxLayout(scroll_content)  # Layout for the content widget

        for index, region in selected_regions_to_exclude.items():
            exclude = QLabel(f"[{index}]: {region}")
            exclude_layout.addWidget(exclude, alignment=Qt.AlignTop)

        # Set the content widget for the scroll area
        scroll_area.setWidget(scroll_content)
        adjust_scroll_area_height(scroll_area)

        # Add the scroll area to the parent widget
        layout.addWidget(scroll_area)

        label = QLabel(f"\nThese coding regions will be classified as non-coding areas.\n")
        layout.addWidget(label, alignment=Qt.AlignTop)

        # Adding formatted text to QLabel
        label_html = '''
        <p>The full sequence after selection is:
        </p>'''

        label = QLabel(label_html)
        layout.addWidget(label)

        # Adding formatted text to QLabel
        label_html = f'''
        <p>{SequenceUtils.highlight_sequences_to_html(selected_region_list)}</p>'''
        text_edit = add_text_edit_html(layout, "", label_html)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid lightgray;
            }
        """)

        QTimer.singleShot(50, self.scroll_to_bottom)  # Add this line

    def scroll_to_bottom(self):
        vertical_scroll_bar = self.scroll.verticalScrollBar()
        self.animation = QPropertyAnimation(vertical_scroll_bar, b'value')
        self.animation.setDuration(1000)
        self.animation.setStartValue(vertical_scroll_bar.value())
        self.animation.setEndValue(vertical_scroll_bar.maximum())
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

        # Install an event filter for the scroll area's viewport.
        self.scroll.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        # If the user scrolls, stop the animation.
        if event.type() == QEvent.Wheel and source == self.scroll.viewport():
            self.animation.stop()
            self.scroll.viewport().removeEventFilter(self)  # Remove event filter.
        return super(ProcessWindow, self).eventFilter(source, event)  # Allow other eventHandlers to respond.


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

    def init_ui(self, parent_widget):
        # Create a new QVBoxLayout for the parent widget
        parent_layout = QVBoxLayout(parent_widget)  # Assuming parent_widget already has a QVBoxLayout

        # Create the instructions label and add it to the parent layout
        instructions_label = QLabel("Please check the regions you want to exclude:")
        parent_layout.addWidget(instructions_label, alignment=Qt.AlignTop)

        # Create a new QVBoxLayout for the content of this section
        scroll_area = QScrollArea()  # Create a scroll area
        scroll_area.setAlignment(Qt.AlignTop)
        scroll_area.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        scroll_content = QWidget()  # Create a widget to hold the content

        layout = QVBoxLayout(scroll_content)  # Layout for the content widget

        for index, region in enumerate(self.original_coding_regions):
            checkbox = QCheckBox(f"[{index + 1}]: {region}")
            layout.addWidget(checkbox, alignment=Qt.AlignTop)
            self.checkboxes.append((checkbox, region))

        # Set the content widget for the scroll area
        scroll_area.setWidget(scroll_content)
        adjust_scroll_area_height(scroll_area)

        # Add the scroll area to the parent widget
        parent_layout.addWidget(scroll_area)

        self.submit_button = add_button(parent_layout, 'Submit Exclusions', Qt.AlignLeft, self.submit_exclusions,
                                        (parent_layout,), size=(200, 30))

    def submit_exclusions(self, layout):
        checked_indices = [index for index, (checkbox, region) in enumerate(self.checkboxes) if checkbox.isChecked()]
        if len(checked_indices) <= 0:
            QMessageBox.question(self.parentWidget(), 'Error',
                                 'You need to choose one coding region at least to continue',
                                 QMessageBox.Ok)
            return

        # Prompt the user for confirmation
        reply = QMessageBox.question(self.parentWidget(), 'Confirm',
                                     'Do you want to eliminate selected coding regions?',
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
        selected_region_list = DNAUtils.update_coding_regions(selected_region_list, self.coding_indexes,
                                                              coding_regions_to_exclude)

        return original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list

    def disable_checkboxes(self):
        for checkbox, region in self.checkboxes:
            checkbox.setEnabled(False)

import os

import webview
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton, QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem

from executions.execution_utils import mark_non_equal_codons, initialize_report
from executions.ui.layout_utils import add_button, add_code_block, add_text_edit


def quit_app():
    QApplication.instance().quit()


def show_preview_report(report_local_file_path):
    file_path = os.path.abspath(report_local_file_path)
    webview.create_window('Preview Report', url=f'file://{file_path}', width=1200, height=800, resizable=False)
    webview.start()


class ResultsWindow(QWidget):
    def __init__(self, dna_sequence, unwanted_patterns, original_coding_regions, original_region_list,
                 selected_regions_to_exclude, selected_region_list, target_seq, min_cost,
                 back_to_elimination_callback):
        super().__init__()
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = unwanted_patterns
        self.original_coding_regions = original_coding_regions
        self.original_region_list = original_region_list
        self.selected_regions_to_exclude = selected_regions_to_exclude
        self.selected_region_list = selected_region_list
        self.target_seq = target_seq
        self.min_cost = min_cost

        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None
        self.report = None

        self.init_ui(back_to_elimination_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)

        callback_args = (self.original_coding_regions, self.original_region_list,
                         self.selected_regions_to_exclude, self.selected_region_list)
        add_button(layout, 'Back', Qt.AlignLeft, callback, callback_args)

        self.display_info(layout)

    def display_info(self, layout):
        self.middle_layout = QVBoxLayout()
        self.middle_layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(self.middle_layout)

        # Adding formatted text to QLabel
        label_html = f"""
            <h2>Results:</h2>
        """

        label = QLabel(label_html)
        self.middle_layout.addWidget(label)

        # Adding formatted text to QLabel
        label_html = f"""
            <h3>DNA Sequences Difference:</h3>
        """

        label = QLabel(label_html)
        self.middle_layout.addWidget(label)

        # Mark non-equal codons and print the target sequence
        marked_input_seq, marked_target_seq, marked_seq = mark_non_equal_codons(self.dna_sequence,
                                                                                self.target_seq,
                                                                                self.selected_region_list)

        content = f'\n {marked_input_seq}\n\n {marked_target_seq}\n'
        text_edit = add_text_edit(self.middle_layout, "", content, wrap=QTextEdit.NoWrap)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid gray;
            }
        """)
        text_edit.setFixedHeight(110)  # Set fixed height

        # Adding formatted text to QLabel
        label_html = f"""
            <br>
            <br>
            <h3>Target DNA Sequences:</h3>
        """

        label = QLabel(label_html)
        self.middle_layout.addWidget(label)

        add_code_block(self.middle_layout, self.target_seq)

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
        done_button = QPushButton('Done')
        done_button.setFixedSize(60, 30)
        done_button.clicked.connect(lambda: quit_app())  # Connect to quit the application
        self.bottom_layout.addWidget(done_button, alignment=Qt.AlignRight)

    def prompt_report(self, layout, target_seq, marked_input_seq, marked_target_seq, original_coding_regions,
                      original_region_list, selected_regions_to_exclude, selected_region_list, min_cost):
        self.report = initialize_report(self.dna_sequence, target_seq, marked_input_seq, marked_target_seq,
                                        self.unwanted_patterns, original_coding_regions, original_region_list,
                                        selected_regions_to_exclude, selected_region_list,
                                        min_cost)

        report_local_file_path = self.report.create_report()

        if report_local_file_path:
            # Create a horizontal layout for the entire prompt
            prompt_layout = QHBoxLayout()
            prompt_layout.setSpacing(10)  # Adjust spacing between elements

            # Create and add the question label to the horizontal layout
            question_label = QLabel("Elimination report is now available")
            prompt_layout.addWidget(question_label)

            # Create the 'Save' button
            download_button = QPushButton('Save to downloads')
            download_button.setFixedSize(150, 30)
            download_button.clicked.connect(
                lambda: self.download_report(layout))

            # Create the 'Save' button
            save_as_button = QPushButton('Save as')
            save_as_button.setFixedSize(120, 30)
            save_as_button.clicked.connect(
                lambda: self.save_as_report(layout, report_local_file_path))

            # Create the 'Preview' button
            show_preview_button = QPushButton("Show Preview")
            show_preview_button.setFixedSize(120, 30)
            show_preview_button.clicked.connect(
                lambda: show_preview_report(report_local_file_path))

            # Add the buttons to the horizontal layout
            prompt_layout.addWidget(download_button)
            prompt_layout.addWidget(save_as_button)
            prompt_layout.addWidget(show_preview_button)

            # Add a spacer to push the buttons to the left
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            prompt_layout.addItem(spacer)

            # Add the entire horizontal layout to the parent layout
            layout.addLayout(prompt_layout)

    def download_report(self, layout):
        report_path = self.report.download_report()

        message_label = QLabel(report_path)
        layout.addWidget(message_label)

    def save_as_report(self, layout, local_pdf_path):
        # Get the path to the desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Show the "Save As" dialog with the desktop directory as the default location
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save As", desktop_dir, "HTML Files (*.html);;All Files (*)",
                                                   options=options)
        message_label = None

        if save_path:
            try:
                with open(local_pdf_path, 'rb') as file:
                    content = file.read()

                with open(save_path, 'wb') as file:
                    file.write(content)

                message_label = QLabel(f"File saved to: {save_path}")
            except Exception as e:
                message_label = QLabel(f"Failed to save file: {e}")

        layout.addWidget(message_label)


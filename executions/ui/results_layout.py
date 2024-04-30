import os

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QDialog, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem

from executions.execution_utils import mark_non_equal_codons, initialize_report
from executions.ui.layout_utils import add_button, add_code_block, add_text_edit


def quit_app():
    QApplication.instance().quit()


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
        self.report_local_file_path = None

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
        marked_input_seq, marked_target_seq, marked_seq, region_list_target = mark_non_equal_codons(
            self.selected_region_list, self.target_seq)

        content = f'\n {marked_input_seq}\n\n {marked_target_seq}\n'
        text_edit = add_text_edit(self.middle_layout, "", content, wrap=QTextEdit.NoWrap)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid gray;
            }
        """)
        text_edit.setFixedHeight(100)  # Set fixed height

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

        self.report_local_file_path = self.report.create_report()

        # Create a horizontal layout for the entire prompt
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(10)  # Adjust spacing between elements

        # Create and add the question label to the horizontal layout
        question_label = QLabel("Elimination report is now available")
        prompt_layout.addWidget(question_label)

        # Create the 'Yes' button
        download_button = QPushButton('Download')
        download_button.setFixedSize(100, 30)
        download_button.clicked.connect(
            lambda: self.download_report(layout))

        # Create the 'No' button
        show_preview_button = QPushButton("Show Preview")
        show_preview_button.setFixedSize(120, 30)
        show_preview_button.clicked.connect(
            lambda: self.show_preview_report())

        # Add the buttons to the horizontal layout
        prompt_layout.addWidget(download_button)
        prompt_layout.addWidget(show_preview_button)

        # Add a spacer to push the buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        prompt_layout.addItem(spacer)

        # Add the entire horizontal layout to the parent layout
        layout.addLayout(prompt_layout)

    def download_report(self, layout):
        report_path = self.report.save_report()
        report_path += "\nReport saved successfully!"

        message_label = QLabel(report_path)
        layout.addWidget(message_label)

    def show_preview_report(self):
        # Create the dialog as a floating window
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle('Elimination Report Preview')
        preview_dialog.setFixedSize(1200, 800)

        # Create a QWebEngineView as the HTML container
        web_view = QWebEngineView(preview_dialog)
        settings = web_view.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        web_view.load(QUrl.fromLocalFile(os.path.abspath(self.report_local_file_path)))

        # Layout for the dialog
        layout = QVBoxLayout(preview_dialog)
        layout.addWidget(web_view)

        # Set layout and show the dialog
        preview_dialog.setLayout(layout)
        preview_dialog.exec_()  # Show the dialog window modally



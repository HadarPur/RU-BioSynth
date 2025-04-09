
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QVBoxLayout

from executions.controllers.ui.elimination_window import EliminationWindow
from executions.controllers.ui.settings_window import SettingsWindow
from executions.controllers.ui.results_window import ResultsWindow
from executions.controllers.ui.upload_window import UploadWindow
from executions.controllers.ui.window_utils import add_text_edit_html, add_text_edit
from executions.execution_utils import is_valid_dna, is_valid_patterns, is_valid_codon_usage
from utils.file_utils import read_codon_usage_map
from utils.dna_utils import DNAUtils
from data.app_data import InputData, CostData, OutputData


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedLayout = QStackedWidget()
        self.dna_file_content = None
        self.patterns_file_content = None
        self.codon_usage_file_content = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🧬 BioBliss App")
        self.setGeometry(100, 100, 1000, 700)
        self.setFixedSize(self.size())
        self.setCentralWidget(self.stackedLayout)
        self.show_upload_window()

    def show_upload_window(self):
        upload_window = UploadWindow(self.switch_to_process_window, self.dna_file_content, self.patterns_file_content, self.codon_usage_file_content)
        self.stackedLayout.addWidget(upload_window)
        self.stackedLayout.setCurrentWidget(upload_window)

    def show_process_window(self):
        process_window = SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def show_elimination_window(self, updated_coding_positions):
        elimination_window = EliminationWindow(self.switch_to_results_window, updated_coding_positions, self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

    def switch_to_results_window(self, updated_coding_positions):
        results_window = ResultsWindow(self.show_elimination_window, updated_coding_positions)
        self.stackedLayout.addWidget(results_window)
        self.stackedLayout.setCurrentWidget(results_window)

    def switch_to_process_window(self, dna_sequence, unwanted_patterns, codon_usage):
        self.dna_file_content = dna_sequence
        if not dna_sequence:
            QMessageBox.warning(self, "Error", "Target sequence file is missing")
            return

        if not is_valid_dna(dna_sequence):
            QMessageBox.warning(self, "Error",
                                f"The sequence:\n{dna_sequence}\n\nis not valid, please check and try again later.")
            return

        if not unwanted_patterns:
            QMessageBox.warning(self, "Error", "Patterns file is missing")
            return

        self.patterns_file_content = unwanted_patterns
        unwanted_patterns = set(unwanted_patterns.split())
        if len(unwanted_patterns) == 0:
            QMessageBox.warning(self, "Error",
                                "There is an issue with the patterns file, please check and try again later.")
            return

        if not is_valid_patterns(unwanted_patterns):
            QMessageBox.warning(self, "Error",
                                f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
            return

        if not codon_usage:
            QMessageBox.warning(self, "Error", "Codon Usage file is missing")
            return

        self.codon_usage_file_content = codon_usage
        codon_usage = read_codon_usage_map(codon_usage.splitlines())
        if len(codon_usage) == 0:
            QMessageBox.warning(self, "Error",
                                "There is an issue with the codon usage file, please check and try again later.")
            return

        if not is_valid_codon_usage(codon_usage):
            QMessageBox.warning(self, "Error",
                                f"The codon usage:\n{codon_usage}\n\nare not valid, please check and try again later.")
            return

        has_overlaps, overlaps = DNAUtils.find_overlapping_regions(dna_sequence)
        if has_overlaps:
            self.show_overlapping_msg(dna_sequence, overlaps)
            return

        InputData.dna_sequence = dna_sequence
        InputData.unwanted_patterns = unwanted_patterns
        CostData.codon_usage = codon_usage

        process_window = SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)

        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def switch_to_elimination_window(self, updated_coding_positions):
        elimination_window = EliminationWindow(self.switch_to_results_window, updated_coding_positions, self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

    def show_overlapping_msg(self, dna_sequence, overlaps):
        # Create a dialog to show detailed information
        dialog = QDialog(self)
        dialog.setWindowTitle('❌ Error')
        dialog.setFixedSize(1000, 400)

        # Set the window flags to make the dialog non-modal and always on top
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        dialog.setWindowModality(Qt.NonModal)  # Allow interaction with the parent

        layout = QVBoxLayout()

        content = "The input sequence contains overlapping coding regions:"
        text_edit = add_text_edit(layout, "", content)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
            }
        """)

        label_html = '''<pre>''' + DNAUtils.get_overlapping_regions(dna_sequence, overlaps) + '''</pre>'''
        text_edit = add_text_edit_html(layout, "", label_html)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
            }
        """)
        text_edit.setFixedHeight(200)  # Set fixed height

        content = "Please make sure that the input seq will not contains any overlapping regions."
        text_edit = add_text_edit(layout, "", content)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
            }
        """)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        # Add a stretch to push all elements to the top
        layout.addStretch()

        dialog.setLayout(layout)
        dialog.exec_()

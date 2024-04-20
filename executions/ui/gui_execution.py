import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon
from executions.ui.upload_layout import UploadWindow
from executions.ui.processing_layout import ProcessWindow
from executions.ui.elimination_layout import EliminationWindow


class DNASequenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedLayout = QStackedWidget()
        self.dna_file_content = None
        self.patterns_file_content = None

        self.dna_sequence = None
        self.unwanted_patterns = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DNA Sequence Elimination App")
        self.setGeometry(100, 100, 1000, 800)
        self.setCentralWidget(self.stackedLayout)
        self.show_upload_window()

    def show_upload_window(self):
        upload_window = UploadWindow(self.switch_to_process_window, self.dna_file_content, self.patterns_file_content)
        self.stackedLayout.addWidget(upload_window)
        self.stackedLayout.setCurrentWidget(upload_window)

    def show_process_window(self):
        process_window = ProcessWindow(self.switch_to_elimination_window, self.dna_sequence, self.unwanted_patterns, self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def switch_to_process_window(self, dna_sequence, unwanted_patterns):
        # TODO: add check if the seq and unwanted_patterns as expected
        if not dna_sequence:
            QMessageBox.warning(self, "Error", "Please upload valid DNA sequence file.")
            return

        if not unwanted_patterns:
            QMessageBox.warning(self, "Error", "Please upload valid Patterns files.")
            return

        self.dna_sequence = dna_sequence
        self.unwanted_patterns = unwanted_patterns

        self.dna_file_content = dna_sequence
        self.patterns_file_content = unwanted_patterns
        process_window = ProcessWindow(self.switch_to_elimination_window, dna_sequence, unwanted_patterns, self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def switch_to_elimination_window(self, original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list):
        process_window = EliminationWindow(self.dna_sequence, self.unwanted_patterns, original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list, self.show_process_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)


class GUI:
    @staticmethod
    def execute():
        app = QApplication(sys.argv)
        ex = DNASequenceApp()
        ex.show()
        app.setWindowIcon(QIcon('images/logo.png'))
        sys.exit(app.exec_())


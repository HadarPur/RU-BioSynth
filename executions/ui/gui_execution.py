import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from executions.ui.elimination_layout import EliminationWindow
from executions.ui.processing_layout import ProcessWindow
from executions.ui.results_layout import ResultsWindow
from executions.ui.upload_layout import UploadWindow

from executions.execution_utils import is_valid_dna, is_valid_patterns
from utils.file_utils import resource_path


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
        self.setGeometry(100, 100, 800, 800)
        self.setCentralWidget(self.stackedLayout)
        self.show_upload_window()

    def show_upload_window(self):
        upload_window = UploadWindow(self.switch_to_process_window, self.dna_file_content, self.patterns_file_content)
        self.stackedLayout.addWidget(upload_window)
        self.stackedLayout.setCurrentWidget(upload_window)

    def show_process_window(self):
        process_window = ProcessWindow(self.switch_to_elimination_window, self.dna_sequence, self.unwanted_patterns,
                                       self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def show_elimination_window(self, original_coding_regions, original_region_list, selected_regions_to_exclude,
                                selected_region_list):
        elimination_window = EliminationWindow(self.switch_to_results_window, self.dna_sequence, self.unwanted_patterns,
                                               original_coding_regions, original_region_list,
                                               selected_regions_to_exclude, selected_region_list, self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

    def switch_to_process_window(self, dna_sequence, unwanted_patterns):
        if not dna_sequence:
            QMessageBox.warning(self, "Error", "DNA sequence file is missing")
            return

        if not is_valid_dna(dna_sequence):
            QMessageBox.warning(self, "Error", f"The sequence:\n{dna_sequence}\n\nis not valid, please check and try again later.")
            return

        if not unwanted_patterns:
            QMessageBox.warning(self, "Error", "Patterns file is missing")
            return

        unwanted_patterns = set(unwanted_patterns.split())
        if len(unwanted_patterns) == 0:
            QMessageBox.warning(self, "Error", "There is an issue with the patterns file, please check and try again later.")
            return

        if not is_valid_patterns(unwanted_patterns):
            QMessageBox.warning(self, "Error", f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
            return

        self.dna_sequence = dna_sequence
        self.unwanted_patterns = unwanted_patterns

        self.dna_file_content = dna_sequence
        self.patterns_file_content = unwanted_patterns
        process_window = ProcessWindow(self.switch_to_elimination_window, dna_sequence, unwanted_patterns,
                                       self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def switch_to_elimination_window(self, original_coding_regions, original_region_list, selected_regions_to_exclude,
                                     selected_region_list):
        elimination_window = EliminationWindow(self.switch_to_results_window, self.dna_sequence, self.unwanted_patterns,
                                               original_coding_regions, original_region_list,
                                               selected_regions_to_exclude,
                                               selected_region_list, self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

    def switch_to_results_window(self, original_coding_regions, original_region_list, selected_regions_to_exclude,
                                 selected_region_list, target_seq, min_cost):
        results_window = ResultsWindow(self.dna_sequence, self.unwanted_patterns,
                                       original_coding_regions, original_region_list, selected_regions_to_exclude,
                                       selected_region_list, target_seq, min_cost, self.show_elimination_window)
        self.stackedLayout.addWidget(results_window)
        self.stackedLayout.setCurrentWidget(results_window)


class GUI:
    @staticmethod
    def execute():
        stylesheet = """

        p {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QCheckBox {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QLabel {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QTextEdit {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QScrollArea {
            border: none;
            background: white; /* This will be the color of the 'margin' */
        }

        QScrollBar:vertical {
            border: none;
            background: lightgray; /* This should match the QScrollArea background */
            width: 2px;
        }

        QScrollBar::handle:vertical {
            background: gray;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            border: none;
            background: lightgray; /* This should match the QScrollArea background */
            height: 6px;
            margin: 4px 0 0 0; /* Vertical margin space */

        }
    
        QScrollBar::handle:horizontal {
            background: gray;
            min-width: 20px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            width: 0px;
        }

        
        """

        app = QApplication(sys.argv)
        ex = DNASequenceApp()
        ex.show()
        icon_path = resource_path('images/logo.png')
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        app.setStyleSheet(stylesheet)
        sys.exit(app.exec_())

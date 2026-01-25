from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QVBoxLayout

from biosynth.data.app_data import InputData, CostData
from biosynth.executions.controllers.ui.elimination_window import EliminationWindow
from biosynth.executions.controllers.ui.results_window import ResultsWindow
from biosynth.executions.controllers.ui.settings_window import SettingsWindow
from biosynth.executions.controllers.ui.upload_window import UploadWindow
from biosynth.executions.controllers.ui.window_utils import add_text_edit_html, add_text_edit
from biosynth.utils.dna_utils import DNAUtils
from biosynth.utils.cost_utils import normalize_codon_usage

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedLayout = QStackedWidget()
        self.dna_file_content = None
        self.patterns_file_content = None
        self.codon_usage_file_content = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🧬 BioSynth App")
        self.setGeometry(100, 100, 1000, 700)
        self.setFixedSize(self.size())
        self.setCentralWidget(self.stackedLayout)

        self.show_upload_window()

    def show_upload_window(self):
        upload_window = UploadWindow(self.switch_to_process_window)
        self.stackedLayout.addWidget(upload_window)
        self.stackedLayout.setCurrentWidget(upload_window)

    def show_process_window(self):
        process_window = SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def show_elimination_window(self):
        elimination_window = EliminationWindow(self.switch_to_results_window,
                                               self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

    def switch_to_results_window(self):
        results_window = ResultsWindow(self.show_elimination_window)
        self.stackedLayout.addWidget(results_window)
        self.stackedLayout.setCurrentWidget(results_window)

    def switch_to_process_window(self, dna_sequence, unwanted_patterns, codon_usage):
        if not dna_sequence:
            QMessageBox.warning(self, "Error", "Target Sequence file is missing")
            return

        if not unwanted_patterns:
            QMessageBox.warning(self, "Error", "Unwanted Patterns file is missing")
            return

        if not codon_usage:
            QMessageBox.warning(self, "Error", "Codon Usage file is missing")
            return

        InputData.dna_sequence = dna_sequence
        InputData.unwanted_patterns = unwanted_patterns
        CostData.codon_usage = normalize_codon_usage(codon_usage)

        InputData.start_codon_identified, InputData.cleaned_dna_sequence = DNAUtils.find_start_codon(InputData.dna_sequence)
        process_window = SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)

        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def switch_to_elimination_window(self):
        elimination_window = EliminationWindow(self.switch_to_results_window,
                                               self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

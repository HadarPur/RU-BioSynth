from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QVBoxLayout

from biosynth.data.app_data import InputData, CostData
from biosynth.executions.execution_utils import is_valid_dna, is_valid_patterns, is_valid_codon_usage
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
        # Validation
        is_target_seq_valid, start_codon_identified, cleaned_dna_sequence = self.target_sequence_validation(dna_sequence)
        is_unwanted_patterns_valid = self.unwanted_patterns_validation(unwanted_patterns)
        is_codon_usage_valid = self.codon_usage_validation(codon_usage)
        is_cost_valid = self.cost_validation(CostData.alpha, CostData.beta, CostData.w)

        if not is_target_seq_valid or not is_unwanted_patterns_valid or not is_codon_usage_valid or not is_cost_valid:
            return

        InputData.dna_sequence = dna_sequence
        InputData.start_codon_identified = start_codon_identified
        InputData.cleaned_dna_sequence = cleaned_dna_sequence
        InputData.unwanted_patterns = unwanted_patterns
        CostData.codon_usage = normalize_codon_usage(codon_usage)

        process_window = SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)

        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)

    def target_sequence_validation(self, dna_sequence):
        if dna_sequence is None:
            QMessageBox.critical(self, "Error", "Target sequence file is missing")
            return False, None, None

        if len(dna_sequence) == 0:
            QMessageBox.critical(self, "Error", "Target sequence file is empty")
            return False, None, None

        if not is_valid_dna(dna_sequence):
            QMessageBox.critical(self, "Error", "Invalid target sequence format in file")
            return False, None, None

        try:
            # Check for start codon
            start_codon_identified, cleaned_dna_sequence = DNAUtils.find_start_codon(dna_sequence)
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Start codon validation failed:\n{e}")
            return False, None, None

        return True, start_codon_identified, cleaned_dna_sequence

    def unwanted_patterns_validation(self, unwanted_patterns):
        if unwanted_patterns is None:
            QMessageBox.critical(self, "Error", "Unwanted patterns file is missing")
            return False

        if len(unwanted_patterns) == 0:
            QMessageBox.critical(self, "Error", "Unwanted patterns file is empty")
            return False

        if not is_valid_patterns(unwanted_patterns):
            QMessageBox.critical(self, "Error", "Invalid unwanted patterns format in file")
            return False

        return True

    def codon_usage_validation(self, codon_usage):
        if codon_usage is None:
            QMessageBox.critical(self, "Error", "Codon usage file is missing")
            return False

        if len(codon_usage) == 0:
            QMessageBox.critical(self, "Error", "Codon usage file is empty")
            return False

        if not is_valid_codon_usage(codon_usage):
            QMessageBox.critical(self, "Error", "Invalid codon usage table format in file")
            return False

        return True

    def cost_validation(self, alpha, beta, w):
        if not (isinstance(alpha, (int, float)) and alpha > 0):
            QMessageBox.critical(self, "Error", f"Invalid alpha value: α = {alpha}. Must be a positive number.")
            return False

        if not (isinstance(beta, (int, float)) and beta > 0):
            QMessageBox.critical(self, "Error", f"Invalid beta value: β = {beta}. Must be a positive number.")
            return False

        if not (isinstance(w, (int, float)) and w > 0):
            QMessageBox.critical(self, "Error", f"Invalid w value: w = {w}. Must be a positive number.")
            return False

        if not (alpha < beta):
            QMessageBox.critical(self, "Error", f"Biological Constraint violated: α < β required "
                                                f"(α={alpha}, β={beta}).")
            return False

        MUCH_LESS_FACTOR = 10  # Define a factor to ensure beta is significantly smaller than w
        if not (beta * MUCH_LESS_FACTOR < w):
            QMessageBox.critical(self, "Error", f"Constraint violated: β ≪ w required "
                                                f"(β={beta}, w={w}, factor={MUCH_LESS_FACTOR}).")
            return False

        return True


    def switch_to_elimination_window(self):
        elimination_window = EliminationWindow(self.switch_to_results_window,
                                               self.show_process_window)
        self.stackedLayout.addWidget(elimination_window)
        self.stackedLayout.setCurrentWidget(elimination_window)

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from biosynth.data.app_data import CostData, InputData
from biosynth.executions.controllers.ui.theme import LABELS, SIZES, TITLES
from biosynth.executions.controllers.ui.utils import EliminationWorker, GuiValidator
from biosynth.executions.controllers.ui.widgets import BusyDialog
from biosynth.executions.controllers.ui.windows.elimination_window import EliminationWindow
from biosynth.executions.controllers.ui.windows.results_window import ResultsWindow
from biosynth.executions.controllers.ui.windows.settings_window import SettingsWindow
from biosynth.executions.controllers.ui.windows.upload_window import UploadWindow
from biosynth.utils.cost_utils import normalize_codon_usage


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedLayout = QStackedWidget()
        self.validator = GuiValidator(self)
        self._busy_dialog = None
        self._elim_thread = None
        self._elim_worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(TITLES.app)
        self.setGeometry(
            SIZES.window_x, SIZES.window_y,
            SIZES.window_width, SIZES.window_height,
        )
        self.setFixedSize(self.size())
        self.setCentralWidget(self.stackedLayout)
        self.show_upload_window()

    def _show_page(self, widget):
        self.stackedLayout.addWidget(widget)
        self.stackedLayout.setCurrentWidget(widget)

    def show_upload_window(self):
        self._show_page(UploadWindow(self.switch_to_process_window))

    def show_process_window(self):
        self._show_page(
            SettingsWindow(self.switch_to_elimination_window, self.show_upload_window)
        )

    def show_elimination_window(self):
        self._show_page(
            EliminationWindow(self.switch_to_results_window, self.show_process_window)
        )

    def switch_to_results_window(self):
        self._show_page(ResultsWindow(self.show_elimination_window))

    def switch_to_elimination_window(self):
        """Run the elimination algorithm on a worker thread.

        Stays on the current page (SettingsWindow) and shows a modal busy
        dialog while the algorithm runs. Only when the worker emits
        ``finished`` does the UI transition to :class:`EliminationWindow`.
        """
        self._busy_dialog = BusyDialog(parent=self, message=LABELS.busy_message)
        self._busy_dialog.show()

        self._elim_thread = QThread(self)
        self._elim_worker = EliminationWorker(
            InputData.cleaned_dna_sequence,
            InputData.unwanted_patterns,
            InputData.coding_positions,
        )
        self._elim_worker.moveToThread(self._elim_thread)

        self._elim_thread.started.connect(self._elim_worker.run)
        self._elim_worker.finished.connect(self._on_elimination_finished)
        self._elim_worker.failed.connect(self._on_elimination_failed)
        self._elim_worker.finished.connect(self._elim_thread.quit)
        self._elim_worker.failed.connect(self._elim_thread.quit)
        self._elim_thread.finished.connect(self._elim_worker.deleteLater)
        self._elim_thread.finished.connect(self._elim_thread.deleteLater)

        self._elim_thread.start()

    def _close_busy_dialog(self):
        if self._busy_dialog is not None:
            self._busy_dialog.close()
            self._busy_dialog = None

    def _on_elimination_finished(self):
        self._close_busy_dialog()
        self.show_elimination_window()

    def _on_elimination_failed(self, error_message: str):
        self._close_busy_dialog()
        QMessageBox.critical(
            self, LABELS.elimination_failed,
            f"{LABELS.elimination_failed}:\n{error_message}",
        )

    def switch_to_process_window(self, dna_sequence, unwanted_patterns, codon_usage):
        ok_seq, start_codon_identified, cleaned_dna_sequence = (
            self.validator.validate_target_sequence(dna_sequence)
        )
        ok_patterns = self.validator.validate_unwanted_patterns(unwanted_patterns)
        ok_codon = self.validator.validate_codon_usage(codon_usage)
        ok_cost = self.validator.validate_cost(CostData.alpha, CostData.beta, CostData.w)

        if not (ok_seq and ok_patterns and ok_codon and ok_cost):
            return

        InputData.dna_sequence = dna_sequence
        InputData.start_codon_identified = start_codon_identified
        InputData.cleaned_dna_sequence = cleaned_dna_sequence
        InputData.unwanted_patterns = unwanted_patterns
        CostData.codon_usage = normalize_codon_usage(codon_usage)

        self.show_process_window()

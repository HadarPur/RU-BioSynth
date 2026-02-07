from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox, QTabWidget
from PyQt5.QtWidgets import (QHBoxLayout, QGridLayout, QWidget, QMessageBox, QFileDialog, QTableWidgetItem)
from biorun.parser import next_count

from biosynth.data.app_data import InputData, UploadData, CostData
from biosynth.executions.controllers.ui.window_utils import add_button, CircularButton
from biosynth.executions.controllers.ui.window_utils import add_intro, add_png_logo, add_drop_text_edit, \
    add_spinbox, add_drop_table
from biosynth.executions.execution_utils import is_valid_dna, is_valid_patterns, is_valid_codon_usage
from biosynth.utils.file_utils import CodonUsageReader, PatternReader, SequenceReader
from biosynth.utils.info_utils import get_info_usage, get_elimination_info


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback):
        super().__init__()
        self.dna_text_edit = None
        self.patterns_text_edit = None
        self.codon_usage_table = None

        self.alpha_spinbox = None
        self.beta_spinbox = None
        self.w_spinbox = None

        self.init_ui(switch_to_process_callback)

    def init_ui(self, next_callback):
        layout = QVBoxLayout(self)

        # Top Layout (Intro & Logo)
        self.add_top_layout(layout)

        # Middel layout - Main Inputs Grid
        self.add_middle_layout(layout)

        # Bottom layout - Info & Next Button
        self.add_bottom_layout(layout, next_callback)

        # Restore content if exists
        self.restore_content()

    def add_top_layout(self, layout):
        top_layout = QGridLayout()
        top_layout.setContentsMargins(20, 20, 20, 5)
        layout.addLayout(top_layout)

        add_intro(top_layout, 0, 0)
        add_png_logo(top_layout, 0, 1)

    def add_middle_layout(self, layout):
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(grid_layout)

        # DNA input
        dna_layout = QVBoxLayout()
        grid_layout.addLayout(dna_layout, 0, 0)
        self.dna_text_edit = add_drop_text_edit(
            layout=dna_layout,
            placeholder="Upload Target Sequence/Drag&Drop Target Sequence file (.txt)",
            drop_callback=self.load_dna_file_from_file_path
        )
        self.dna_text_edit.textChanged.connect(self.dna_text_edit_changed)
        add_button(dna_layout, 'Load Target Sequence', Qt.AlignCenter, self.load_dna_file, size=(200, 30))

        # Patterns input
        pattern_layout = QVBoxLayout()
        grid_layout.addLayout(pattern_layout, 1, 0)
        self.patterns_text_edit = add_drop_text_edit(
            layout=pattern_layout,
            placeholder="Upload Patterns file/Drag&Drop Patterns file (.txt)",
            drop_callback=self.load_patterns_file_from_file_path
        )
        self.patterns_text_edit.textChanged.connect(self.patterns_text_edit_changed)
        add_button(pattern_layout, 'Load Patterns', Qt.AlignCenter, self.load_patterns_file, size=(200, 30))

        # Codon Usage File Upload
        codon_usage_layout = QVBoxLayout()
        grid_layout.addLayout(codon_usage_layout, 0, 1)
        self.codon_usage_table = add_drop_table(
            layout=codon_usage_layout,
            placeholder="Upload Codon Usage file/Drag&Drop Codon Usage file (.txt)",
            columns=2,
            headers=["Codon", "Frequency"],
            drop_callback=self.load_codon_usage_from_file_path
        )
        self.codon_usage_table.itemChanged.connect(self.codon_usage_table_changed)
        add_button(codon_usage_layout, 'Load Codon Usage', Qt.AlignCenter, self.load_codon_usage_file, size=(200, 30))

        # Custom Scores
        custom_scores_layout = QVBoxLayout()
        grid_layout.addLayout(custom_scores_layout, 1, 1)
        self.alpha_spinbox = add_spinbox(custom_scores_layout, default_value=CostData.alpha,
                    callback=lambda val: setattr(CostData, 'alpha', val), args=("Transition substitution cost",),
                    alignment=Qt.AlignCenter)
        self.beta_spinbox = add_spinbox(custom_scores_layout, default_value=CostData.beta,
                    callback=lambda val: setattr(CostData, 'beta', val), args=("Transversion substitution cost",),
                    alignment=Qt.AlignCenter)
        self.w_spinbox = add_spinbox(custom_scores_layout, default_value=CostData.w,
                    callback=lambda val: setattr(CostData, 'w', val), args=("Non-synonymous substitution cost",),
                    alignment=Qt.AlignCenter)
        custom_scores_layout.addStretch(1)

    def add_bottom_layout(self, layout, next_callback):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(bottom_layout)

        info_button = CircularButton('ⓘ', self)
        info_button.clicked.connect(self.show_info)

        bottom_layout.addWidget(info_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch(1)
        add_button(bottom_layout, 'Reset', Qt.AlignRight, self.reset)
        add_button(bottom_layout, 'Next', Qt.AlignRight, next_callback, self.get_input_data)

    # Reset all fields
    def reset(self):
        UploadData.reset()
        CostData.reset()

        self.dna_text_edit.clear()
        self.patterns_text_edit.clear()
        self.codon_usage_table.setRowCount(0)
        self.codon_usage_table.update_placeholder()

        self.alpha_spinbox.setValue(CostData.alpha)
        self.beta_spinbox.setValue(CostData.beta)
        self.w_spinbox.setValue(CostData.w)

    # Gather input data to move forward
    def get_input_data(self):
        return (
            UploadData.dna_sequence_content_file,
            UploadData.unwanted_patterns_content_file,
            UploadData.codon_usage_content_file,
        )

    def restore_content(self):
        if UploadData.dna_sequence_content_file:
            self.dna_text_edit.setPlainText(UploadData.dna_sequence_content_file)
        if UploadData.unwanted_patterns_content_file:
            self.patterns_text_edit.setPlainText("\n".join(UploadData.unwanted_patterns_content_file))
        if UploadData.codon_usage_content_file:
            self.update_codon_usage_table_from_dict(UploadData.codon_usage_content_file)

    # File loaders
    def load_dna_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Target Sequence File", "", "Text Files (*.txt)")

        if not file_name:
            return

        self.load_dna_file_from_file_path(file_name)

    def load_dna_file_from_file_path(self, file_path):
        try:
            content = SequenceReader(file_path).read_sequence()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {e}")
            return  # Exit if file couldn't be read

        # Validate content after successful read
        if content and is_valid_dna(content):
            UploadData.dna_sequence_content_file = content
            self.dna_text_edit.setPlainText(content)
        else:
            QMessageBox.critical(self, "Error", "Invalid target sequence format in file")

    def dna_text_edit_changed(self):
        content = self.dna_text_edit.toPlainText()
        UploadData.dna_sequence_content_file = content

    def load_patterns_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Unwanted Patterns File", "", "Text Files (*.txt)")

        if not file_name:
            return

        self.load_patterns_file_from_file_path(file_name)

    def load_patterns_file_from_file_path(self, file_path):
        try:
            content = PatternReader(file_path).read_patterns()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {e}")
            return  # Exit if file couldn't be read

        # Validate content after successful read
        if content and is_valid_patterns(content):
            UploadData.unwanted_patterns_content_file = content
            self.patterns_text_edit.setPlainText("\n".join(content))
        else:
            QMessageBox.critical(self, "Error", "Invalid unwanted patterns format in file")

    def patterns_text_edit_changed(self):
        content = self.patterns_text_edit.toPlainText().splitlines()
        UploadData.unwanted_patterns_content_file = content

    def load_codon_usage_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Codon Usage File", "", "Text Files (*.txt)")

        if not file_name:
            return

        self.load_codon_usage_from_file_path(file_name)

    def load_codon_usage_from_file_path(self, file_path):
        try:
            content = CodonUsageReader(file_path).read_codon_usage()
            CostData.codon_usage_filename = CodonUsageReader(file_path).get_filename()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {e}")
            return

        if content and is_valid_codon_usage(content):
            UploadData.codon_usage_content_file = content
            self.update_codon_usage_table_from_dict(content)
        else:
            QMessageBox.critical(self, "Error", f"Invalid codon usage table format in file.")

    # Table updater
    def update_codon_usage_table_from_dict(self, codon_usage_content):
        self.codon_usage_table.setRowCount(len(codon_usage_content))
        for row_idx, (codon, freq) in enumerate(codon_usage_content.items()):
            self.codon_usage_table.setItem(row_idx, 0, QTableWidgetItem(codon))
            self.codon_usage_table.setItem(row_idx, 1, QTableWidgetItem(str(freq)))

        self.codon_usage_table.update_placeholder()

    def codon_usage_table_changed(self):
        codon_usage = {}

        rows = self.codon_usage_table.rowCount()

        for row in range(rows):
            codon_item = self.codon_usage_table.item(row, 0)
            freq_item = self.codon_usage_table.item(row, 1)

            if codon_item is None or freq_item is None:
                continue  # skip incomplete rows

            codon = codon_item.text().strip()
            freq_text = freq_item.text().strip()

            try:
                freq = float(freq_text)  # or int(freq_text) if appropriate
            except ValueError:
                continue  # skip invalid numbers

            codon_usage[codon] = freq

        UploadData.codon_usage_content_file = codon_usage

    def show_info(self):
        usage_text = get_info_usage().replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;")
        elimination_text = get_elimination_info().replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;").replace("  ", "&nbsp;&nbsp;&nbsp;")

        dialog = QDialog(self)
        dialog.setWindowTitle('Information')
        dialog.setFixedSize(1000, 400)
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        dialog.setWindowModality(Qt.NonModal)

        layout = QVBoxLayout()

        # Create tab widget
        tabs = QTabWidget()

        # First tab - Usage info
        usage_tab = QTextEdit()
        usage_tab.setReadOnly(True)
        usage_tab.setHtml(usage_text)
        usage_tab.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                font-size: 15px;
                line-height: 5px;
                padding: 2px;
            }
        """)
        tabs.addTab(usage_tab, "Coding Region Criteria")

        # Second tab - Elimination info
        elimination_tab = QTextEdit()
        elimination_tab.setReadOnly(True)
        elimination_tab.setHtml(elimination_text)
        elimination_tab.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                font-size: 15px;
                line-height: 5px;
                padding: 2px;
            }
        """)
        tabs.addTab(elimination_tab, "Substitution Costs")

        layout.addWidget(tabs)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.show()

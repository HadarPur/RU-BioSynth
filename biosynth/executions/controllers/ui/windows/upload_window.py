from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from biosynth.data.app_data import CostData, UploadData
from biosynth.executions.controllers.ui.theme import LABELS, MARGINS, SIZES, TITLES
from biosynth.executions.controllers.ui.utils import (
    add_button,
    add_drop_table,
    add_drop_text_edit,
    add_intro,
    add_png_logo,
    add_spinbox,
    add_toggle,
)
from biosynth.executions.controllers.ui.widgets import CircularButton, InfoDialog
from biosynth.executions.execution_utils import (
    is_valid_codon_usage,
    is_valid_dna,
    is_valid_patterns,
)
from biosynth.utils.file_utils import CodonUsageReader, PatternReader, SequenceReader
from biosynth.utils.descriptions import get_elimination_info, get_info_usage


class UploadWindow(QWidget):
    """First wizard page — collects DNA sequence, patterns, codon usage, and costs."""

    def __init__(self, switch_to_process_callback):
        super().__init__()
        self.dna_text_edit = None
        self.patterns_text_edit = None
        self.codon_usage_table = None

        self.alpha_spinbox = None
        self.beta_spinbox = None
        self.w_spinbox = None
        self.optimized_codon_toggle = None

        self.init_ui(switch_to_process_callback)

    def init_ui(self, next_callback):
        """Assemble the page layout and restore any previously entered content."""
        layout = QVBoxLayout(self)

        self.add_top_layout(layout)
        self.add_middle_layout(layout)
        self.add_bottom_layout(layout, next_callback)
        self.restore_content()

    def add_top_layout(self, layout):
        """Add the welcome blurb (left) and the logo (right) to the top row."""
        top_layout = QGridLayout()
        top_layout.setContentsMargins(*MARGINS.page_top_compact)
        layout.addLayout(top_layout)

        add_intro(top_layout, 0, 0)
        add_png_logo(top_layout, 0, 1)

    def add_middle_layout(self, layout):
        """Add the 2x2 grid of upload inputs (DNA, patterns, codon usage, costs)."""
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(*MARGINS.page_top_bottom)
        layout.addLayout(grid_layout)

        # DNA input
        dna_layout = QVBoxLayout()
        grid_layout.addLayout(dna_layout, 0, 0)
        self.dna_text_edit = add_drop_text_edit(
            layout=dna_layout,
            placeholder=LABELS.placeholder_target_sequence,
            drop_callback=self.load_dna_file_from_file_path,
        )
        self.dna_text_edit.textChanged.connect(self.dna_text_edit_changed)
        add_button(
            dna_layout, LABELS.load_target_sequence, Qt.AlignCenter, self.load_dna_file,
            size=(SIZES.button_xlarge_w, SIZES.button_h),
        )

        # Patterns input
        pattern_layout = QVBoxLayout()
        grid_layout.addLayout(pattern_layout, 1, 0)
        self.patterns_text_edit = add_drop_text_edit(
            layout=pattern_layout,
            placeholder=LABELS.placeholder_patterns,
            drop_callback=self.load_patterns_file_from_file_path,
        )
        self.patterns_text_edit.textChanged.connect(self.patterns_text_edit_changed)
        add_button(
            pattern_layout, LABELS.load_patterns, Qt.AlignCenter, self.load_patterns_file,
            size=(SIZES.button_xlarge_w, SIZES.button_h),
        )

        # Codon Usage File Upload
        codon_usage_layout = QVBoxLayout()
        grid_layout.addLayout(codon_usage_layout, 0, 1)
        self.codon_usage_table = add_drop_table(
            layout=codon_usage_layout,
            placeholder=LABELS.placeholder_codon_usage,
            columns=2,
            headers=list(LABELS.codon_columns),
            drop_callback=self.load_codon_usage_from_file_path,
        )
        self.codon_usage_table.itemChanged.connect(self.codon_usage_table_changed)
        add_button(
            codon_usage_layout, LABELS.load_codon_usage, Qt.AlignCenter, self.load_codon_usage_file,
            size=(SIZES.button_xlarge_w, SIZES.button_h),
        )

        # Custom Scores
        custom_scores_layout = QVBoxLayout()
        grid_layout.addLayout(custom_scores_layout, 1, 1)
        self.alpha_spinbox = add_spinbox(
            custom_scores_layout, default_value=CostData.alpha,
            callback=lambda val: setattr(CostData, 'alpha', val),
            args=(LABELS.spin_alpha,), alignment=Qt.AlignCenter,
        )
        self.beta_spinbox = add_spinbox(
            custom_scores_layout, default_value=CostData.beta,
            callback=lambda val: setattr(CostData, 'beta', val),
            args=(LABELS.spin_beta,), alignment=Qt.AlignCenter,
        )
        self.w_spinbox = add_spinbox(
            custom_scores_layout, default_value=CostData.w,
            callback=lambda val: setattr(CostData, 'w', val),
            args=(LABELS.spin_w,), alignment=Qt.AlignCenter,
        )
        self.optimized_codon_toggle = add_toggle(
            custom_scores_layout, default_value=CostData.optimized_codon,
            callback=lambda val: setattr(CostData, 'optimized_codon', val),
            args=(LABELS.toggle_optimized_codon,), alignment=Qt.AlignCenter,
        )

        custom_scores_layout.addStretch(1)

    def add_bottom_layout(self, layout, next_callback):
        """Add the bottom bar with the Info, Reset, and Next buttons."""
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(*MARGINS.page_top_bottom)
        layout.addLayout(bottom_layout)

        info_button = CircularButton(LABELS.info_glyph, self)
        info_button.clicked.connect(self.show_info)
        bottom_layout.addWidget(info_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch(1)
        add_button(bottom_layout, LABELS.reset, Qt.AlignRight, self.reset)
        add_button(bottom_layout, LABELS.next, Qt.AlignRight, next_callback, self.get_input_data)

    def reset(self):
        """Clear all uploaded inputs and restore default cost/toggle values."""
        UploadData.reset()
        CostData.reset()

        self.dna_text_edit.clear()
        self.patterns_text_edit.clear()
        self.codon_usage_table.setRowCount(0)
        self.codon_usage_table.update_placeholder()

        self.alpha_spinbox.setValue(CostData.alpha)
        self.beta_spinbox.setValue(CostData.beta)
        self.w_spinbox.setValue(CostData.w)

        self.optimized_codon_toggle.setChecked(CostData.optimized_codon)

    def get_input_data(self):
        """Return the current ``(dna, patterns, codon_usage)`` tuple from UploadData."""
        return (
            UploadData.dna_sequence_content_file,
            UploadData.unwanted_patterns_content_file,
            UploadData.codon_usage_content_file,
        )

    def restore_content(self):
        """Repopulate the inputs from any previously cached UploadData values."""
        if UploadData.dna_sequence_content_file:
            self.dna_text_edit.setPlainText(UploadData.dna_sequence_content_file)
        if UploadData.unwanted_patterns_content_file:
            self.patterns_text_edit.setPlainText(
                "\n".join(UploadData.unwanted_patterns_content_file)
            )
        if UploadData.codon_usage_content_file:
            self.update_codon_usage_table_from_dict(UploadData.codon_usage_content_file)

    def load_dna_file(self):
        """Open a file picker to choose a target-sequence ``.txt`` file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Sequence File", "", "Text Files (*.txt)"
        )
        if not file_name:
            return
        self.load_dna_file_from_file_path(file_name)

    def load_dna_file_from_file_path(self, file_path):
        """Read and validate a DNA file, then populate the target-sequence editor."""
        try:
            content = SequenceReader(file_path).read_sequence()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {e}")
            return

        if content and is_valid_dna(content):
            UploadData.dna_sequence_content_file = content
            self.dna_text_edit.setPlainText(content)
        else:
            QMessageBox.critical(self, "Error", "Invalid sequence format in file")

    def dna_text_edit_changed(self):
        """Mirror the DNA text edit's current content back into UploadData."""
        UploadData.dna_sequence_content_file = self.dna_text_edit.toPlainText()

    def load_patterns_file(self):
        """Open a file picker to choose an unwanted-patterns ``.txt`` file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Unwanted Patterns File", "", "Text Files (*.txt)"
        )
        if not file_name:
            return
        self.load_patterns_file_from_file_path(file_name)

    def load_patterns_file_from_file_path(self, file_path):
        """Read and validate a patterns file, then populate the patterns editor."""
        try:
            content = PatternReader(file_path).read_patterns()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {e}")
            return

        if content and is_valid_patterns(content):
            UploadData.unwanted_patterns_content_file = content
            self.patterns_text_edit.setPlainText("\n".join(content))
        else:
            QMessageBox.critical(self, "Error", "Invalid unwanted patterns format in file")

    def patterns_text_edit_changed(self):
        """Mirror the patterns editor's lines back into UploadData."""
        content = self.patterns_text_edit.toPlainText().splitlines()
        UploadData.unwanted_patterns_content_file = content

    def load_codon_usage_file(self):
        """Open a file picker to choose a codon-usage ``.txt`` file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Codon Usage File", "", "Text Files (*.txt)"
        )
        if not file_name:
            return
        self.load_codon_usage_from_file_path(file_name)

    def load_codon_usage_from_file_path(self, file_path):
        """Read and validate a codon-usage file, then fill the codon-usage table."""
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
            QMessageBox.critical(self, "Error", "Invalid codon usage table format in file.")

    def update_codon_usage_table_from_dict(self, codon_usage_content):
        """Replace the codon-usage table's rows from a ``{codon: freq}`` dict."""
        self.codon_usage_table.setRowCount(len(codon_usage_content))
        for row_idx, (codon, freq) in enumerate(codon_usage_content.items()):
            self.codon_usage_table.setItem(row_idx, 0, QTableWidgetItem(codon))
            self.codon_usage_table.setItem(row_idx, 1, QTableWidgetItem(str(freq)))
        self.codon_usage_table.update_placeholder()

    def codon_usage_table_changed(self):
        """Sync UploadData with the codon-usage table after a user edit."""
        codon_usage = {}
        for row in range(self.codon_usage_table.rowCount()):
            codon_item = self.codon_usage_table.item(row, 0)
            freq_item = self.codon_usage_table.item(row, 1)
            if codon_item is None or freq_item is None:
                continue
            codon = codon_item.text().strip()
            freq_text = freq_item.text().strip()
            try:
                codon_usage[codon] = float(freq_text)
            except ValueError:
                continue

        UploadData.codon_usage_content_file = codon_usage

    def show_info(self):
        """Open the help dialog with coding-region and substitution-cost tabs."""
        usage_text = (
            get_info_usage()
            .replace("\n", "<br>")
            .replace("\t", "&nbsp;&nbsp;&nbsp;")
        )
        elimination_text = (
            get_elimination_info()
            .replace("\n", "<br>")
            .replace("\t", "&nbsp;&nbsp;&nbsp;")
            .replace("  ", "&nbsp;&nbsp;&nbsp;")
        )

        dialog = InfoDialog.from_html(
            parent=self,
            title=TITLES.info_dialog,
            tabs=[
                (LABELS.tab_coding_region, usage_text),
                (LABELS.tab_substitution_costs, elimination_text),
            ],
            fixed_size=(SIZES.info_dialog_w, SIZES.info_dialog_h_short),
        )
        dialog.show()

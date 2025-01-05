from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem, QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QVBoxLayout

from executions.controllers.ui.window_utils import add_button, CircularButton
from executions.controllers.ui.window_utils import add_intro, add_png_logo, add_drop_text_edit, add_text_edit_html
from utils.text_utils import format_text_bold_for_output


def get_info_usage():
    return f"{format_text_bold_for_output('Information:')}\n" \
           "The elimination program via terminal is designed to run automatically without any user intervention.\n" \
           "Please be advised that the program makes the following decisions:\n" \
           "\t - The minimum length of a coding region is 5 codons (excluding start and stop codons).\n" \
           "\t - If a coding region contains another coding region, the longer region will be selected.\n" \
           "\t - If a coding region overlaps another coding region, the program will raise an error message and stop.\n"


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback, dna_file_content=None, patterns_file_content=None, codon_usage_file_content=None):
        super().__init__()
        self.switch_to_process_callback = switch_to_process_callback
        self.dna_file_content = dna_file_content
        self.patterns_file_content = '\n'.join(sorted(patterns_file_content)) if patterns_file_content else ''
        self.codon_usage_file_content = '\n'.join(codon_usage_file_content) if codon_usage_file_content else ''

        self.dna_text_edit = None
        self.patterns_text_edit = None
        self.codon_usage_text_edit = None

        self.init_ui(switch_to_process_callback)

    def init_ui(self, next_callback):
        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 5)
        layout.addLayout(top_layout)

        add_intro(top_layout)

        fixed_width_spacer = QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        top_layout.addSpacerItem(fixed_width_spacer)

        add_png_logo(top_layout)

        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(middle_layout)

        self.dna_text_edit = add_drop_text_edit(middle_layout, "Upload Target Sequence/Drag&Drop Target Sequence file (.txt)",
                                                self.dna_file_content)
        add_button(middle_layout, 'Load Target Sequence', Qt.AlignCenter, self.load_file, (self.dna_text_edit,),
                   size=(200, 30))

        self.patterns_text_edit = add_drop_text_edit(middle_layout,
                                                     "Upload Patterns file/Drag&Drop Patterns file (.txt)",
                                                     self.patterns_file_content)
        add_button(middle_layout, 'Load Patterns', Qt.AlignCenter, self.load_file, (self.patterns_text_edit,),
                   size=(200, 30))

        self.codon_usage_text_edit = add_drop_text_edit(middle_layout,
                                                     "Upload Codon Usage file/Drag&Drop Codon Usage file (.txt)",
                                                     self.patterns_file_content)
        add_button(middle_layout, 'Load Codon Usage', Qt.AlignCenter, self.load_file, (self.codon_usage_text_edit,),
                   size=(200, 30))

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(bottom_layout)

        # Create the info button
        info_button = CircularButton('ⓘ', self)
        info_button.clicked.connect(self.show_info)
        bottom_layout.addWidget(info_button, alignment=Qt.AlignLeft)

        add_button(bottom_layout, 'Next', Qt.AlignRight, next_callback,
                   lambda: (self.dna_text_edit.toPlainText().strip(),
                            self.patterns_text_edit.toPlainText().strip(),
                            self.codon_usage_text_edit.toPlainText().strip()))

    def load_file(self, text_edit):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if fileName:
            try:
                with open(fileName, 'r') as file:
                    text_edit.setPlainText(file.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read the file: {e}")
        else:
            QMessageBox.information(self, "No File Selected", "No file was selected.")

    def show_info(self):
        info_text = get_info_usage()
        info_text = info_text.replace("\n", "<br><br>")
        info_text = info_text.replace("\t", "&nbsp;&nbsp;&nbsp;")

        # Create a dialog to show detailed information
        dialog = QDialog(self)
        dialog.setWindowTitle('Info')
        dialog.setFixedSize(1000, 400)

        # Set the window flags to make the dialog non-modal and always on top
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        dialog.setWindowModality(Qt.NonModal)  # Allow interaction with the parent

        layout = QVBoxLayout()
        text_edit = add_text_edit_html(layout, "", info_text)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                font-size: 15px;
                line-height: 5px;
                padding: 2px; /* Top, Right, Bottom, Left */
            }
        """)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.show()

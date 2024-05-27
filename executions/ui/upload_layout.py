from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

from executions.ui.layout_utils import add_intro, add_svg_logo, add_button, add_drop_text_edit


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback, dna_file_content=None, patterns_file_content=None):
        super().__init__()
        self.switch_to_process_callback = switch_to_process_callback
        self.dna_file_content = dna_file_content
        self.patterns_file_content = '\n'.join(sorted(patterns_file_content)) if patterns_file_content else ''

        self.dna_text_edit = None
        self.patterns_text_edit = None

        self.init_ui(switch_to_process_callback)

    def init_ui(self, next_callback):
        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 5)
        layout.addLayout(top_layout)

        add_intro(top_layout)

        fixed_width_spacer = QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        top_layout.addSpacerItem(fixed_width_spacer)

        add_svg_logo(top_layout)

        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(middle_layout)

        self.dna_text_edit = add_drop_text_edit(middle_layout, "Upload DNA Sequence/Drag&Drop DNA Sequence file (.txt)", self.dna_file_content)
        add_button(middle_layout, 'Load DNA Sequence', Qt.AlignCenter, self.load_file, (self.dna_text_edit,),
                   size=(200, 30))

        self.patterns_text_edit = add_drop_text_edit(middle_layout, "Upload Patterns file/Drag&Drop Patterns file (.txt)", self.patterns_file_content)
        add_button(middle_layout, 'Load Patterns', Qt.AlignCenter, self.load_file, (self.patterns_text_edit,), size=(200, 30))

        add_button(layout, 'Next', Qt.AlignRight, next_callback, lambda: (self.dna_text_edit.toPlainText().strip(),
                                                                          self.patterns_text_edit.toPlainText().strip()))

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

from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QHBoxLayout
from executions.ui.layout_utils import add_svg_logo, add_next_button


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback, dna_file_content=None, patterns_file_content=None):
        super().__init__()
        self.switch_to_process_callback = switch_to_process_callback
        self.dna_file_content = dna_file_content
        self.patterns_file_content = patterns_file_content

        self.dna_text_edit = None
        self.patterns_text_edit = None

        self.init_ui(switch_to_process_callback)

    def init_ui(self, next_callback):
        layout = QVBoxLayout(self)

        # Create top layout for title and logo
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        self.create_title(top_layout)

        # Adding a fixed-width empty label for spacing
        space_label = QLabel(" ")
        space_label.setFixedWidth(50)  # You can adjust the width as needed
        top_layout.addWidget(space_label)

        add_svg_logo(top_layout)

        middle_layout = QVBoxLayout()
        layout.addLayout(middle_layout)

        self.dna_text_edit = self.create_text_edit(middle_layout, "Upload DNA Sequence (.txt):", self.dna_file_content)
        self.create_load_button(middle_layout, self.dna_text_edit, "Load DNA Sequence")
        self.patterns_text_edit = self.create_text_edit(middle_layout, "Upload Patterns (.txt):", self.patterns_file_content)
        self.create_load_button(middle_layout, self.patterns_text_edit, "Load Patterns")

        # Correct way: Directly integrate dynamic action in the lambda
        add_next_button(layout, next_callback, lambda: (self.dna_text_edit.toPlainText().strip(),
                                                        self.patterns_text_edit.toPlainText().strip()))

    def create_title(self, layout):
        content = "Hi,"
        content += "\nWelcome to the DNA Sequence Elimination App."
        content += "\nTo eliminate unwanted patterns from a specific DNA sequence, please upload the DNA sequence file " \
                   "along with the patterns file you wish to remove."
        content += "\n"
        content += "\nThe DNA sequence file should contain only one continuous sequence."
        content += "\nThe patterns file should list each pattern on a new line, containing only standard characters" \
                   " without any special symbols."
        content += "\n"
        title = QLabel(content)
        layout.addWidget(title)
        return title

    def create_text_edit(self, layout, placeholder, content):
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        if content:
            text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        return text_edit

    def create_load_button(self, layout, text_edit, button_text):
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.load_file(text_edit))
        layout.addWidget(button)

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

from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QVBoxLayout


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback, dna_file_content=None, patterns_file_content=None):
        super().__init__()
        self.switch_to_process_callback = switch_to_process_callback
        self.dna_file_content = dna_file_content
        self.patterns_file_content = patterns_file_content

        self.layout = None
        self.dna_text_edit = None
        self.patterns_text_edit = None

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.dna_text_edit = self.create_text_edit("Upload DNA Sequence (.txt):", self.dna_file_content)
        self.load_button(self.dna_text_edit, "Load DNA Sequence")
        self.patterns_text_edit = self.create_text_edit("Upload Patterns (.txt):", self.patterns_file_content)
        self.load_button(self.patterns_text_edit, "Load Patterns")
        self.proceed_button()

    def create_text_edit(self, placeholder, content):
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        if content:
            text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        self.layout.addWidget(text_edit)
        return text_edit

    def load_button(self, text_edit, button_text):
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.load_file(text_edit))
        self.layout.addWidget(button)

    def proceed_button(self):
        button = QPushButton('Next')
        button.clicked.connect(lambda: self.switch_to_process_callback(
            self.dna_text_edit.toPlainText().strip(), self.patterns_text_edit.toPlainText().strip()
        ))
        self.layout.addWidget(button)

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

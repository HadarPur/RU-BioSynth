from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QVBoxLayout


class UploadWindow(QWidget):
    def __init__(self, switch_to_process_callback):
        super().__init__()
        self.switch_to_process_callback = switch_to_process_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        dnaTextEdit = QTextEdit()
        dnaTextEdit.setPlaceholderText("Upload DNA Sequence (.txt):")
        dnaTextEdit.setReadOnly(True)
        layout.addWidget(dnaTextEdit)

        loadDNAButton = QPushButton('Load DNA Sequence')
        loadDNAButton.clicked.connect(lambda: self.loadFile(dnaTextEdit))
        layout.addWidget(loadDNAButton)

        patternsTextEdit = QTextEdit()
        patternsTextEdit.setPlaceholderText("Upload Patterns (.txt):")
        patternsTextEdit.setReadOnly(True)
        layout.addWidget(patternsTextEdit)

        loadPatternsButton = QPushButton('Load Patterns')
        loadPatternsButton.clicked.connect(lambda: self.loadFile(patternsTextEdit))
        layout.addWidget(loadPatternsButton)

        proceedButton = QPushButton('Proceed')
        proceedButton.clicked.connect(lambda: self.switch_to_process_callback(
            dnaTextEdit.toPlainText().strip(), patternsTextEdit.toPlainText().strip()
        ))
        layout.addWidget(proceedButton)

    def loadFile(self, textEdit):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if not fileName:
            QMessageBox.information(self, "No File Selected", "No file was selected.")
            return
        try:
            with open(fileName, 'r') as file:
                textEdit.setText(file.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read the file: {e}")


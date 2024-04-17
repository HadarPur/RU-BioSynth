import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget
from executions.ui.upload_layout import UploadWindow
from executions.ui.processing_layout import ProcessWindow


class DNASequenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedLayout = QStackedWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DNA Sequence Elimination App")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(self.stackedLayout)
        self.showUploadWindow()

    def showUploadWindow(self):
        upload_window = UploadWindow(self.switchToProcessWindow)
        self.stackedLayout.addWidget(upload_window)
        self.stackedLayout.setCurrentWidget(upload_window)

    def switchToProcessWindow(self, dna_sequence, unwanted_patterns):
        if not dna_sequence:
            QMessageBox.warning(self, "Error", "Please upload valid DNA sequence file.")
            return

        if not unwanted_patterns:
            QMessageBox.warning(self, "Error", "Please upload valid Patterns files.")
            return

        process_window = ProcessWindow(dna_sequence, unwanted_patterns, self.showUploadWindow)
        self.stackedLayout.addWidget(process_window)
        self.stackedLayout.setCurrentWidget(process_window)


class GUI:
    @staticmethod
    def execute():
        app = QApplication(sys.argv)
        ex = DNASequenceApp()
        ex.show()
        sys.exit(app.exec_())


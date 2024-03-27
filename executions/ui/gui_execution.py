import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QFormLayout


class GUI:
    def __init__(self):
        self.seq = ""

    def execute(self):
        app = QApplication([])

        widget = Ui_Form()
        widget.resize(800, 600)
        widget.show()

        return sys.exit(app.exec())

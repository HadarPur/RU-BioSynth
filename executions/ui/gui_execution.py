import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel


class GUI:
    def __init__(self):
        self.seq = ""

    def execute(self):
        app = QApplication(sys.argv)
        label = QLabel("Hello World", alignment=Qt.AlignCenter)
        label.show()
        return sys.exit(app.exec_())

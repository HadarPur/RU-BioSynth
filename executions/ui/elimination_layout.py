from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QVBoxLayout


class EliminationWindow(QWidget):
    def __init__(self, original_coding_regions, selected_regions_to_exclude, selected_region_list, back_to_processing_callback):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)


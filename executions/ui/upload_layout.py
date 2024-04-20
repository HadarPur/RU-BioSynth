from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt


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

        # Create top layout for title and logo
        top_layout = QHBoxLayout()
        self.create_title(top_layout)

        # Adding a fixed-width empty label for spacing
        space_label = QLabel(" ")
        space_label.setFixedWidth(150)  # You can adjust the width as needed
        top_layout.addWidget(space_label)

        self.add_svg_logo(top_layout)
        self.layout.addLayout(top_layout)

        self.dna_text_edit = self.create_text_edit("Upload DNA Sequence (.txt):", self.dna_file_content)
        self.load_button(self.dna_text_edit, "Load DNA Sequence")
        self.patterns_text_edit = self.create_text_edit("Upload Patterns (.txt):", self.patterns_file_content)
        self.load_button(self.patterns_text_edit, "Load Patterns")
        self.proceed_button()

    def create_title(self, layout):
        content = "Hi,"
        content += "\nWelcome to the DNA Sequence Elimination App."
        content += "\nTo eliminate unwanted patterns from a specific DNA sequence, please upload the DNA sequence file along with the patterns file you wish to remove."
        content += "\n"
        content += "\nThe DNA sequence file should contain only one continuous sequence."
        content += "\nThe patterns file should list each pattern on a new line, containing only standard characters without any special symbols."
        content += "\n"
        title = QLabel(content)
        layout.addWidget(title)
        return title

    def add_svg_logo(self, layout):
        # Create a frame to hold the logo
        frame = QFrame()
        frame_layout = QHBoxLayout(frame)  # Use a QHBoxLayout within the frame
        frame_layout.setContentsMargins(10, 10, 10, 10)  # Set padding: left, top, right, bottom

        # Create and set up the SVG logo widget
        logo = QSvgWidget("report/ru.svg")
        logo.setFixedSize(120, 60)  # Adjust the size as needed

        # Add the logo to the frame's layout
        frame_layout.addWidget(logo)

        # Add the frame to the main layout
        layout.addWidget(frame, alignment=Qt.AlignTop)

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

from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QPlainTextEdit, QApplication


def add_svg_logo(layout):
    # Create a frame to hold the logo
    frame = QFrame()
    frame_layout = QHBoxLayout(frame)  # Use a QHBoxLayout within the frame
    frame_layout.setContentsMargins(5, 5, 5, 5)  # Set padding: left, top, right, bottom

    # Create and set up the SVG logo widget
    logo = QSvgWidget("images/ru.svg")
    logo.setFixedSize(100, 50)  # Adjust the size as needed

    # Add the logo to the frame's layout
    frame_layout.addWidget(logo)

    # Add the frame to the main layout
    layout.addWidget(frame, alignment=Qt.AlignTop)


def add_text_edit(layout, placeholder, content):
    text_edit = QTextEdit()
    text_edit.setPlaceholderText(placeholder)
    if content:
        text_edit.setPlainText(content)
    text_edit.setReadOnly(True)
    layout.addWidget(text_edit)
    return text_edit


def add_code_block(parent_layout, text):
    layout = QVBoxLayout()
    parent_layout.addLayout(layout)

    # Create a QPlainTextEdit to display the code
    code_display = QPlainTextEdit(text)
    code_display.setReadOnly(True)
    code_display.setLineWrapMode(QPlainTextEdit.NoWrap)
    layout.addWidget(code_display)

    # Button layout
    button_layout = QHBoxLayout()
    button_layout.addStretch(1)  # Push the button to the right

    # Copy button
    copy_button = QPushButton("Copy")
    copy_button.clicked.connect(lambda: copy_to_clipboard(code_display))
    button_layout.addWidget(copy_button)

    # Adding the button layout to the main layout
    layout.addLayout(button_layout)


def add_button(layout, text, alignment, callback, args=()):
    bottom_layout = QHBoxLayout()
    layout.addLayout(bottom_layout)

    button = QPushButton(text)
    button.setFixedSize(60, 30)
    button.setFocusPolicy(Qt.NoFocus)

    # Check if 'args' is callable or not and connect accordingly
    if callable(args):
        button.clicked.connect(lambda: callback(*args()))
    else:
        button.clicked.connect(lambda: callback(*args))

    bottom_layout.addWidget(button, alignment=alignment)


def remove_item_at(layout, index):
    # Take the item out of the layout
    item = layout.takeAt(index)
    if item:
        # Check if the item is a widget and handle accordingly
        if item.widget():
            item.widget().deleteLater()
        # If the item is a spacer, delete it
        elif item.spacerItem():
            # The spacer item can be deleted if it will no longer be used
            del item
        # If the item is another layout, handle it recursively
        else:
            # Recursively clear out layout items
            remove_item_at(item.layout(), 0)  # Example: start with the first item
            item.layout().deleteLater()


def copy_to_clipboard(code_display):
    text = code_display.toPlainText()
    QApplication.clipboard().setText(text)

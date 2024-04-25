from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QTextEdit


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


def add_back_button(layout, callback, args=()):
    top_layout = QHBoxLayout()
    layout.addLayout(top_layout)

    # Add button to the top layout
    button = QPushButton('Back')
    button.setFixedSize(60, 30)
    button.setFocusPolicy(Qt.NoFocus)  # Disable focus outline
    button.clicked.connect(lambda: callback(*args))
    top_layout.addWidget(button, alignment=Qt.AlignLeft)


def add_next_button(layout, callback, args=()):
    bottom_layout = QHBoxLayout()
    layout.addLayout(bottom_layout)

    button = QPushButton('Next')
    button.setFixedSize(60, 30)
    button.setFocusPolicy(Qt.NoFocus)
    button.clicked.connect(lambda: callback(*args()))
    bottom_layout.addWidget(button, alignment=Qt.AlignRight)


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

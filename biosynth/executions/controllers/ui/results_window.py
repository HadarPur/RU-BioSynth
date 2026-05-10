import os
from datetime import datetime

import webview
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem, QDialog, QTextEdit, QDialogButtonBox, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

from biosynth.data.app_data import InputData, OutputData, EliminationData
from biosynth.executions.controllers.ui.window_utils import add_button, add_code_block, add_text_edit_html, \
    CircularButton, create_table_from_data
from biosynth.executions.execution_utils import mark_non_equal_codons, initialize_report

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


def quit_app():
    QApplication.instance().quit()


def show_preview_report(report_local_file_path):
    file_path = os.path.abspath(report_local_file_path)
    webview.create_window('Preview Report', url=f'file://{file_path}', width=1200, height=800, resizable=False)
    webview.start()


class ResultsWindow(QWidget):
    def __init__(self, back_to_elimination_callback):
        super().__init__()
        self.report = None

        self.status_label = None
        self.fade_in_animation = None
        self.fade_out_animation = None
        self.status_opacity = None

        self.init_ui(back_to_elimination_callback)

    def init_ui(self, back_callback):
        layout = QVBoxLayout(self)

        # Top Layout
        self.add_top_layout(layout, back_callback)

        # Middle layout with information
        self.add_middle_layout(layout)

        # Bottom layout
        self.add_bottom_layout(layout)


    def add_top_layout(self, layout, back_callback):
        # Top-level layout
        add_button(layout, 'Back', Qt.AlignLeft, back_callback, ())
        return layout

    def add_middle_layout(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(middle_layout)

        # Adding formatted text to QLabel
        label_html = f"""
            <h2>Results:</h2>
        """

        label = QLabel(label_html)
        middle_layout.addWidget(label)

        info_layout = QHBoxLayout()
        middle_layout.addLayout(info_layout)

        # Adding formatted text to QLabel
        label_html = f"""
            <h3>DNA Sequences Difference:</h3>
        """

        label = QLabel(label_html)
        info_layout.addWidget(label)

        # Create the info button
        info_button = CircularButton('ⓘ', self)
        info_button.clicked.connect(self.show_info)
        info_layout.addWidget(info_button, alignment=Qt.AlignRight)

        # Mark non-equal codons and print the optimized sequence
        index_seq_str, marked_input_seq, marked_optimized_seq = mark_non_equal_codons(InputData.cleaned_dna_sequence,
                                                                                      OutputData.optimized_sequence, InputData.coding_positions)

        content = '''<pre>''' + index_seq_str + '''<br></pre>'''
        content += '''<pre>''' + marked_input_seq + '''<br><br>''' + marked_optimized_seq + '''</pre>'''

        content = content.replace("\n", "<br>")
        content = content.replace(" ", "&nbsp;")

        text_edit = add_text_edit_html(middle_layout, "", content)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: 1px solid gray;
                padding: 10px; /* Top, Right, Bottom, Left */
            }
        """)
        text_edit.setFixedHeight(150)  # Set fixed height

        # Adding formatted text to QLabel
        label_html = f"""
            <h3>Optimized Sequence:</h3>
        """

        label = QLabel(label_html)
        middle_layout.addWidget(label)

        # Create a report summarizing the processing and save if the user chooses to
        file_date = datetime.today().strftime("%d-%b-%Y, %H-%M-%S")

        add_code_block(middle_layout, OutputData.optimized_sequence, file_date, self.update_status)

        # Spacer to push other widgets to the top
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.prompt_report(middle_layout, file_date)

    def add_bottom_layout(self, layout):
        # Create a horizontal layout for the bottom section
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(bottom_layout)

        # Add next button to the bottom layout
        done_button = add_button(bottom_layout, 'Done', Qt.AlignRight)
        done_button.clicked.connect(lambda: quit_app())

        # Create floating status label (as a child of the main widget, not in layout)
        # This should be called after the main widget is created
        self.init_floating_status(self)

    def init_floating_status(self, parent_widget):
        """
        Initialize the floating status label.
        Call this after your main widget/window is set up.

        Args:
            parent_widget: The main widget/window to overlay the status on
        """
        self.status_label = QLabel(parent_widget)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #000000;
                background-color: transparent;
                border: transparent;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
        """)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.status_label.raise_()  # Ensure it's on top

        # Set up opacity effect for fade animation
        self.status_opacity = QGraphicsOpacityEffect()
        self.status_label.setGraphicsEffect(self.status_opacity)

    def prompt_report(self, layout, file_date):
        self.report = initialize_report()

        report_local_file_path = self.report.create_report(file_date)

        if report_local_file_path:
            # Create a horizontal layout for the entire prompt
            prompt_layout = QHBoxLayout()
            prompt_layout.setSpacing(10)  # Adjust spacing between elements

            # Create and add the question label to the horizontal layout
            question_label = QLabel("Elimination report is now available")
            prompt_layout.addWidget(question_label)

            # Create the 'Save' button
            download_button = QPushButton('Download')
            download_button.setFixedSize(120, 30)
            download_button.clicked.connect(
                lambda: self.download_report())

            # Create the 'Save' button
            save_as_button = QPushButton('Save as')
            save_as_button.setFixedSize(120, 30)
            save_as_button.clicked.connect(
                lambda: self.save_as_report())

            # Create the 'Preview' button
            show_preview_button = QPushButton("Show Preview")
            show_preview_button.setFixedSize(120, 30)
            show_preview_button.clicked.connect(
                lambda: show_preview_report(report_local_file_path))

            # Add the buttons to the horizontal layout
            prompt_layout.addWidget(download_button)
            prompt_layout.addWidget(save_as_button)
            prompt_layout.addWidget(show_preview_button)

            # Add a spacer to push the buttons to the left
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            prompt_layout.addItem(spacer)

            # Add the entire horizontal layout to the parent layout
            layout.addLayout(prompt_layout)

    def show_info(self):
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle('Info')
        dialog.setFixedSize(1000, 500)

        dialog.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.WindowCloseButtonHint
        )

        dialog.setWindowModality(Qt.NonModal)

        layout = QVBoxLayout()

        # Tabs
        tabs = QTabWidget()

        # First tab - cost_contribution
        contribution_tab = QWidget()
        contribution_layout = QVBoxLayout()

        contribution_table = create_table_from_data(
            EliminationData.cost_contribution
        )

        contribution_layout.addWidget(contribution_table)
        contribution_tab.setLayout(contribution_layout)

        # Second tab - cost_substitution
        substitution_tab = QWidget()
        substitution_layout = QVBoxLayout()

        substitution_table = create_table_from_data(
            EliminationData.cost_substitution
        )

        substitution_layout.addWidget(substitution_table)
        substitution_tab.setLayout(substitution_layout)

        # Add tabs
        tabs.addTab(contribution_tab, "Cost Contribution")
        tabs.addTab(substitution_tab, "Cost Substitution")

        layout.addWidget(tabs)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)

        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.show()

    def download_report(self):
        report_path = f"Report downloaded to: {self.report.download_report()}"

        # Update status label when the report is downloaded
        self.update_status(report_path)

    def update_status(self, message):
        # Update the label text
        self.status_label.setText(f"{message}")

        # Set dimensions (adjust these values as needed)
        label_width = 890
        self.status_label.setFixedWidth(label_width)
        self.status_label.adjustSize()  # Let height auto-adjust to content

        # Position the label at bottom-left (floating above the bottom layout)
        parent = self.status_label.parent()
        x = 20  # Left margin
        y = parent.height() - self.status_label.height() - 15  # Above the bottom
        self.status_label.move(x, y)

        # Fade in animation
        self.fade_in_animation = QPropertyAnimation(self.status_opacity, b"opacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.status_label.show()
        self.status_label.raise_()  # Make sure it's on top
        self.fade_in_animation.start()

        # Auto-hide after 5 seconds with fade out
        QTimer.singleShot(5000, self.hide_download_status)

    def hide_download_status(self):
        """Hide the status label with fade out animation"""
        if self.status_label is None or not self.status_label.isVisible():
            return

        # Fade out animation
        self.fade_out_animation = QPropertyAnimation(self.status_opacity, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out_animation.finished.connect(self.status_label.hide)
        self.fade_out_animation.start()

    def save_as_report(self):
        # Get the path to the desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Show the "Save As" dialog with the desktop directory as the default location
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save As", desktop_dir, "HTML Files (*.html);",
                                                   options=options)
        if save_path:
            try:
                report_path = self.report.download_report(save_path)
                self.update_status(f"Report saved as: {report_path}")
            except Exception as e:
                self.update_status(f"Failed to save report with error: {e}")

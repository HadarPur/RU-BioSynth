from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QSizePolicy, QHBoxLayout

from biosynth.data.app_data import InputData, EliminationData
from biosynth.executions.controllers.ui.window_utils import FloatingScrollIndicator, add_button
from biosynth.executions.execution_utils import eliminate_unwanted_patterns
from biosynth.utils.output_utils import Logger


class EliminationWindow(QWidget):
    def __init__(self, switch_to_results_callback, back_to_processing_callback):
        super().__init__()
        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None

        self.yes_button = None
        self.no_button = None
        self.next_button = None
        self.floating_btn = None

        self.init_ui(back_to_processing_callback, switch_to_results_callback)

    def init_ui(self, back_callback, next_callback):
        layout = QVBoxLayout(self)

        # Top-level layout
        self.add_top_layout(layout, back_callback)

        # Middle layout with information
        self.add_middle_layout(layout)

        # Bottom layout
        self.add_bottom_layout(layout, next_callback)

    def add_top_layout(self, layout, back_callback):
        # Top-level layout
        add_button(layout, 'Back', Qt.AlignLeft, back_callback, ())
        return layout

    def add_middle_layout(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(middle_layout)

        eliminate_unwanted_patterns(InputData.cleaned_dna_sequence, InputData.unwanted_patterns, InputData.coding_positions)

        wrapped_info = Logger.get_formated_text(EliminationData.info).replace("\n", "<br>")
        html = f"""
            <h2>Elimination Process</h2>
            <div style="margin-right: 25px;">{wrapped_info}</div>
        """

        text_browser = QTextBrowser()
        text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: transparent;
            }
        """)
        text_browser.setHtml(html)
        text_browser.setOpenExternalLinks(False)

        # Disable the internal scroll bars
        text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        text_browser.setMinimumHeight(550)

        text_browser.setAlignment(Qt.AlignTop)

        # Optionally, force the QTextBrowser to adjust to the content.
        text_browser.document().setTextWidth(text_browser.viewport().width())
        text_browser.adjustSize()

        middle_layout.addWidget(text_browser)

        # Add floating button
        self.floating_btn = FloatingScrollIndicator(parent=self, scroll_area=text_browser)
        self.floating_btn.on_scroll(text_browser.verticalScrollBar().value())

    def add_bottom_layout(self, layout, next_callback):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 5, 20, 20)
        layout.addLayout(bottom_layout)

        next_button = add_button(bottom_layout, 'Next', Qt.AlignRight)
        next_button.clicked.connect(
            lambda: next_callback())

    def resizeEvent(self, event):
        self.floating_btn.raise_()  # Bring to front
        self.floating_btn.reposition()

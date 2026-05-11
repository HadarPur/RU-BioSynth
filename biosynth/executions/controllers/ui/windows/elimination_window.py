from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QTextBrowser, QVBoxLayout

from biosynth.data.app_data import EliminationData
from biosynth.executions.controllers.ui.theme import MARGINS, SIZES, transparent_text_edit_qss
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.utils.output_utils import Logger


class EliminationWindow(WizardPage):
    """Renders the elimination output. Assumes `EliminationData` is already
    populated by ``BaseWindow.switch_to_elimination_window`` before this
    page is shown.
    """

    def __init__(self, switch_to_results_callback, back_to_processing_callback):
        super().__init__(
            back_callback=back_to_processing_callback,
            next_callback=switch_to_results_callback,
        )
        self.build()

    def build_body(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(*MARGINS.page_padded)
        layout.addLayout(middle_layout)

        wrapped_info = Logger.get_formated_text(EliminationData.info).replace(
            "\n", "<br>"
        )
        html = (
            f'<h2>Elimination Process</h2>'
            f'<div style="margin-right: 25px;">{wrapped_info}</div>'
        )

        text_browser = QTextBrowser()
        text_browser.setStyleSheet(
            transparent_text_edit_qss(with_border=False, margin_right_px=0)
        )
        text_browser.setHtml(html)
        text_browser.setOpenExternalLinks(False)
        text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        text_browser.setMinimumHeight(SIZES.scroll_area_height)
        text_browser.setAlignment(Qt.AlignTop)
        text_browser.document().setTextWidth(text_browser.viewport().width())
        text_browser.adjustSize()

        middle_layout.addWidget(text_browser)
        self.attach_floating_indicator(text_browser)

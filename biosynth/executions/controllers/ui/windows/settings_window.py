from PyQt5.QtWidgets import QLabel, QVBoxLayout

from biosynth.data.app_data import InputData
from biosynth.executions.controllers.ui.theme import MARGINS, transparent_text_edit_qss
from biosynth.executions.controllers.ui.utils import (
    add_text_edit_html,
    adjust_text_edit_height,
    create_scroll_area,
)
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils


class SettingsWindow(WizardPage):
    def __init__(self, switch_to_eliminate_callback, back_to_upload_callback):
        super().__init__(
            back_callback=back_to_upload_callback,
            next_callback=switch_to_eliminate_callback,
        )
        self.build()

    def build_body(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(*MARGINS.page_middle)
        layout.addLayout(middle_layout)

        scroll_area, _content_widget, content_layout = create_scroll_area(middle_layout)

        self._add_target_sequence(content_layout)
        self._add_unwanted_patterns(content_layout)

        content_layout.addStretch(1)
        self.attach_floating_indicator(scroll_area)

    def _add_target_sequence(self, content_layout):
        content_layout.addWidget(QLabel("<h2>Input</h2><h3>Target Sequence:</h3>"))

        InputData.coding_positions, InputData.coding_indexes = (
            DNAUtils.get_coding_and_non_coding_regions_positions(
                InputData.cleaned_dna_sequence, InputData.start_codon_identified
            )
        )

        highlighted_sequence = (
            "<pre>"
            + SequenceUtils.highlight_sequences_to_html(
                InputData.cleaned_dna_sequence,
                InputData.coding_indexes,
                line_length=96,
                returnBr=True,
            )
            + "</pre>"
        )

        if InputData.coding_indexes is not None and len(InputData.coding_indexes) > 0:
            description = (
                f"<p>A coding region was identified in the target sequence at "
                f"positions {InputData.coding_indexes[0] + 1} - "
                f"{InputData.coding_indexes[1]}:</p>"
            )
        else:
            description = "<p>A coding region identified in the provided target sequence</p>"

        content_layout.addWidget(QLabel(description))

        text_edit = add_text_edit_html(content_layout, "", highlighted_sequence)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet(transparent_text_edit_qss())

    def _add_unwanted_patterns(self, content_layout):
        content_layout.addWidget(QLabel("<h3>Unwanted Patterns:</h3>"))

        unwanted_pattern_html = f"<p>{SequenceUtils.get_patterns(InputData.unwanted_patterns)}</p>"
        text_edit = add_text_edit_html(content_layout, "", unwanted_pattern_html)
        adjust_text_edit_height(text_edit)
        text_edit.setStyleSheet(transparent_text_edit_qss())

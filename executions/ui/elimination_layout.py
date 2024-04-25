from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout, QScrollArea

from executions.execution_utils import eliminate_unwanted_patterns
from executions.ui.layout_utils import add_back_button, add_next_button


class EliminationWindow(QWidget):
    def __init__(self, switch_to_results_callback, dna_sequence, unwanted_patterns, original_coding_regions,
                 original_region_list,
                 selected_regions_to_exclude,
                 selected_region_list, back_to_processing_callback):
        super().__init__()
        self.switch_to_results_callback = switch_to_results_callback
        self.dna_sequence = dna_sequence
        self.unwanted_patterns = set(unwanted_patterns.split())
        self.original_coding_regions = original_coding_regions
        self.original_region_list = original_region_list
        self.selected_regions_to_exclude = selected_regions_to_exclude
        self.selected_region_list = selected_region_list

        self.top_layout = None
        self.middle_layout = None
        self.bottom_layout = None

        self.yes_button = None
        self.no_button = None
        self.next_button = None

        self.init_ui(back_to_processing_callback)

    def init_ui(self, callback):
        layout = QVBoxLayout(self)
        add_back_button(layout, callback)
        self.display_info(layout)

    def display_info(self, layout):
        middle_layout = QVBoxLayout()
        layout.addLayout(middle_layout)

        scroll = QScrollArea()
        middle_layout.addWidget(scroll, alignment=Qt.AlignTop)

        content_widget = QWidget()
        scroll.setWidget(content_widget)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setAlignment(Qt.AlignTop)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(650)

        content_layout = QVBoxLayout(content_widget)

        info, target_seq, min_cost = eliminate_unwanted_patterns(self.dna_sequence, self.unwanted_patterns,
                                                                 self.selected_region_list)
        info = info.replace("\n", "<br>")
        # Adding formatted text to QLabel
        label_html = f"""
            <h3>Elimination Process:</h3>
            <p>{info}</p>
        """

        label = QLabel(label_html)
        label.setWordWrap(True)
        content_layout.addWidget(label)

        # Spacer to push other widgets to the top
        content_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add next button to the bottom layout
        add_next_button(layout, self.switch_to_results_callback, lambda: (self.original_coding_regions,
                                                                          self.original_region_list,
                                                                          self.selected_regions_to_exclude,
                                                                          self.selected_region_list, target_seq,
                                                                          min_cost))

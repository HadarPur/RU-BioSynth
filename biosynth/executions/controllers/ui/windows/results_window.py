import os
from datetime import datetime

import webview
from PyQt5 import QtCore
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)

from biosynth.data.app_data import EliminationData, InputData, OutputData
from biosynth.executions.controllers.ui.theme import (
    COLORS,
    LABELS,
    MARGINS,
    SIZES,
    TITLES,
    status_label_qss,
    transparent_text_edit_qss,
)
from biosynth.executions.controllers.ui.utils import (
    add_code_block,
    add_text_edit_html,
    create_table_from_data,
)
from biosynth.executions.controllers.ui.widgets import CircularButton, InfoDialog
from biosynth.executions.controllers.ui.windows.wizard_page import WizardPage
from biosynth.executions.execution_utils import initialize_report, mark_non_equal_codons

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


def quit_app():
    QApplication.instance().quit()


def show_preview_report(report_local_file_path):
    file_path = os.path.abspath(report_local_file_path)
    webview.create_window(
        TITLES.preview_window,
        url=f'file://{file_path}',
        width=1200,
        height=800,
        resizable=False,
    )
    webview.start()


class ResultsWindow(WizardPage):
    def __init__(self, back_to_elimination_callback):
        super().__init__(
            back_callback=back_to_elimination_callback,
            next_callback=quit_app,
            next_label=LABELS.done,
        )
        self.report = None
        self.status_label = None
        self.fade_in_animation = None
        self.fade_out_animation = None
        self.status_opacity = None

        self.build()
        self._init_floating_status(self)

    def build_body(self, layout):
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(*MARGINS.page_padded)
        layout.addLayout(middle_layout)

        middle_layout.addWidget(QLabel("<h2>Results:</h2>"))

        info_layout = QHBoxLayout()
        middle_layout.addLayout(info_layout)
        info_layout.addWidget(QLabel("<h3>DNA Sequences Difference:</h3>"))

        info_button = CircularButton(LABELS.info_glyph, self)
        info_button.clicked.connect(self.show_info)
        info_layout.addWidget(info_button, alignment=Qt.AlignRight)

        index_seq_str, marked_input_seq, marked_optimized_seq = mark_non_equal_codons(
            InputData.cleaned_dna_sequence,
            OutputData.optimized_sequence,
            InputData.coding_positions,
        )

        content = f"<pre>{index_seq_str}<br></pre>"
        content += f"<pre>{marked_input_seq}<br><br>{marked_optimized_seq}</pre>"
        content = content.replace("\n", "<br>").replace(" ", "&nbsp;")

        text_edit = add_text_edit_html(middle_layout, "", content)
        text_edit.setStyleSheet(
            transparent_text_edit_qss(
                border_color=COLORS.border_medium,
                padding_px=10,
                margin_right_px=0,
            )
        )
        text_edit.setFixedHeight(SIZES.sequence_diff_height)

        middle_layout.addWidget(QLabel("<h3>Optimized Sequence:</h3>"))

        file_date = datetime.today().strftime("%d-%b-%Y, %H-%M-%S")
        add_code_block(
            middle_layout,
            OutputData.optimized_sequence,
            file_date,
            self.update_status,
        )

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self._prompt_report(middle_layout, file_date)

    def _init_floating_status(self, parent_widget):
        self.status_label = QLabel(parent_widget)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_label.setStyleSheet(status_label_qss())
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.status_label.raise_()

        self.status_opacity = QGraphicsOpacityEffect()
        self.status_label.setGraphicsEffect(self.status_opacity)

    def _prompt_report(self, layout, file_date):
        self.report = initialize_report()
        report_local_file_path = self.report.create_report(file_date)

        if not report_local_file_path:
            return

        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(10)
        prompt_layout.addWidget(QLabel(LABELS.report_available))

        for label, slot in (
            (LABELS.download, self.download_report),
            (LABELS.save_as, self.save_as_report),
            (LABELS.show_preview, lambda: show_preview_report(report_local_file_path)),
        ):
            button = QPushButton(label)
            button.setFixedSize(SIZES.button_large_w, SIZES.button_h)
            button.clicked.connect(slot)
            prompt_layout.addWidget(button)

        prompt_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        layout.addLayout(prompt_layout)

    def show_info(self):
        contribution_table = create_table_from_data(EliminationData.cost_contribution)
        substitution_table = create_table_from_data(EliminationData.cost_substitution)

        dialog = InfoDialog.from_widgets(
            parent=self,
            title=TITLES.results_info_dialog,
            tabs=[
                (LABELS.tab_cost_contribution, contribution_table),
                (LABELS.tab_cost_substitution, substitution_table),
            ],
            fixed_size=(SIZES.info_dialog_w, SIZES.info_dialog_h_tall),
        )
        dialog.show()

    def download_report(self):
        report_path = f"Report downloaded to: {self.report.download_report()}"
        self.update_status(report_path)

    def update_status(self, message):
        self.status_label.setText(f"{message}")
        self.status_label.setFixedWidth(SIZES.status_label_width)
        self.status_label.adjustSize()

        parent = self.status_label.parent()
        x = SIZES.status_label_left_margin
        y = parent.height() - self.status_label.height() - SIZES.status_label_bottom_margin
        self.status_label.move(x, y)

        self.fade_in_animation = QPropertyAnimation(self.status_opacity, b"opacity")
        self.fade_in_animation.setDuration(SIZES.fade_anim_ms)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.status_label.show()
        self.status_label.raise_()
        self.fade_in_animation.start()

        QTimer.singleShot(SIZES.status_visible_ms, self.hide_download_status)

    def hide_download_status(self):
        if self.status_label is None or not self.status_label.isVisible():
            return

        self.fade_out_animation = QPropertyAnimation(self.status_opacity, b"opacity")
        self.fade_out_animation.setDuration(SIZES.fade_anim_ms)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out_animation.finished.connect(self.status_label.hide)
        self.fade_out_animation.start()

    def save_as_report(self):
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save As", desktop_dir, "HTML Files (*.html);", options=options
        )
        if not save_path:
            return
        try:
            report_path = self.report.download_report(save_path)
            self.update_status(f"Report saved as: {report_path}")
        except Exception as e:
            self.update_status(f"Failed to save report with error: {e}")

"""Custom Qt widgets used across the BioSynth GUI.

Each widget pulls its visual constants and QSS from the :mod:`ui.theme`
package — adjust the theme tokens or QSS factories there to retheme.
"""

from PyQt5.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    pyqtProperty,
)
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QRegion
from PyQt5.QtWidgets import (
    QAbstractButton,
    QPushButton,
    QTableWidget,
    QTextEdit,
)

from biosynth.executions.controllers.ui.theme import (
    COLORS,
    SIZES,
    circular_button_qss,
    floating_indicator_qss,
)


class ToggleSwitch(QAbstractButton):
    def __init__(self, parent=None, width=None, height=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)

        self._width = width if width is not None else SIZES.toggle_w
        self._height = height if height is not None else SIZES.toggle_h
        self._margin = 3

        self._offset = self._margin
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(SIZES.toggle_anim_ms)

        self.toggled.connect(self._start_transition)

    def get_offset(self):
        return self._offset

    def set_offset(self, value):
        self._offset = value
        self.update()

    offset = pyqtProperty(float, get_offset, set_offset)

    def sizeHint(self):
        return QSize(self._width, self._height)

    def minimumSizeHint(self):
        return QSize(self._width, self._height)

    def _start_transition(self, checked):
        self._anim.stop()
        if checked:
            end = self._width - self._height + self._margin
        else:
            end = self._margin
        self._anim.setStartValue(self._offset)
        self._anim.setEndValue(end)
        self._anim.start()

    def paintEvent(self, event):
        radius = self._height / 2
        knob_radius = radius - self._margin

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_color = QColor(COLORS.toggle_on if self.isChecked() else COLORS.toggle_off)

        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self._width, self._height, radius, radius)

        painter.setBrush(QBrush(QColor(COLORS.toggle_knob)))
        painter.drawEllipse(
            QRectF(self._offset, self._margin, knob_radius * 2, knob_radius * 2)
        )

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
        event.accept()


class CircularButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(SIZES.circular_btn, SIZES.circular_btn)
        self.setStyleSheet(circular_button_qss())

    def paintEvent(self, event):
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        super().paintEvent(event)


class DropTextEdit(QTextEdit):
    def __init__(self, parent=None, drop_callback=None):
        super().__init__(parent)
        self.drop_callback = drop_callback
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.endswith('.txt') and self.drop_callback:
                self.drop_callback(file_path)

        event.acceptProposedAction()


class DropTableWidget(QTableWidget):
    def __init__(self, parent=None, drop_callback=None):
        super().__init__(parent)
        self.drop_callback = drop_callback
        self.setAcceptDrops(True)
        self.setDragDropMode(QTableWidget.DropOnly)
        self.viewport().setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".txt") and self.drop_callback:
                self.drop_callback(file_path)
        event.accept()


class FloatingScrollIndicator(QPushButton):
    def __init__(self, parent=None, scroll_area=None, direction="bottom"):
        super().__init__("▼", parent)
        self.animation = None
        self.scroll_area = scroll_area
        self.direction = direction

        self.setFixedSize(SIZES.floating_indicator, SIZES.floating_indicator)
        self.setStyleSheet(floating_indicator_qss())
        self.hide()

        if self.scroll_area:
            self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.clicked.connect(self.scroll)

    def on_scroll(self, value):
        scrollbar = self.scroll_area.verticalScrollBar()
        if scrollbar.maximum() == 0:
            self.hide()
        elif value < scrollbar.maximum() - 10:
            self.show()
        else:
            self.hide()

    def scroll(self, **kwargs):
        bar = self.scroll_area.verticalScrollBar()
        start_value = bar.value()
        if self.direction == "top":
            end_value = 0
        elif self.direction == "bottom":
            end_value = bar.maximum()
        else:
            return

        self.animation = QPropertyAnimation(bar, b"value")
        self.animation.setDuration(SIZES.scroll_anim_ms)
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def reposition(self):
        if not self.parent():
            return
        margin = SIZES.floating_indicator_margin_bottom
        x = self.parent().width() / 2
        y = self.parent().height() - self.height() - margin
        self.move(int(x), int(y))

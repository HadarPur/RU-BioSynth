import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from biosynth.executions.controllers.ui.theme import global_app_qss
from biosynth.executions.controllers.ui.windows import BaseWindow
from biosynth.utils.file_utils import resource_path

sys.stderr = open(os.devnull, 'w')


class GUIController:
    """Controller that boots the PyQt5 GUI application."""

    @staticmethod
    def execute():
        """Launch the Qt application.

        Creates the ``QApplication``, instantiates the main ``BaseWindow``,
        applies the BioSynth icon and global stylesheet, and enters the Qt
        event loop. Calls ``sys.exit`` with the loop's return code.
        """
        app = QApplication(sys.argv)
        ex = BaseWindow()
        ex.show()
        icon_path = resource_path('images/BioSynth.png')
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        app.setStyleSheet(global_app_qss())
        sys.exit(app.exec_())

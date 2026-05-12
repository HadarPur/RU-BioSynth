import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from biosynth.executions.controllers.ui.theme import global_app_qss
from biosynth.executions.controllers.ui.windows import BaseWindow
from biosynth.utils.file_utils import resource_path

sys.stderr = open(os.devnull, 'w')


class GUIController:
    @staticmethod
    def execute():
        app = QApplication(sys.argv)
        ex = BaseWindow()
        ex.show()
        icon_path = resource_path('images/BioSynth.png')
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        app.setStyleSheet(global_app_qss())
        sys.exit(app.exec_())

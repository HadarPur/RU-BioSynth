import os
import sys
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from biosynth.executions.controllers.ui.base_window import BaseWindow
from biosynth.utils.file_utils import resource_path

# Platform-specific Qt configuration
def configure_qt_platform():
    """Configure Qt platform based on the operating system and available plugins."""
    system = platform.system().lower()
    
    if system == "linux":
        # On Linux, try to use xcb first, then fallback to other platforms
        available_platforms = ['xcb', 'wayland', 'minimal']
        
        for platform_name in available_platforms:
            try:
                os.environ['QT_QPA_PLATFORM'] = platform_name
                # Test if the platform works by creating a minimal QApplication
                test_app = QApplication.instance()
                if test_app is None:
                    test_app = QApplication([])
                test_app.quit()
                print(f"Using Qt platform: {platform_name}")
                return platform_name
            except Exception as e:
                print(f"Platform {platform_name} failed: {e}")
                continue
        
        # If all platforms fail, use the default
        print("Warning: All Qt platforms failed, using default")
        if 'QT_QPA_PLATFORM' in os.environ:
            del os.environ['QT_QPA_PLATFORM']
    
    elif system == "darwin":  # macOS
        # On macOS, let Qt choose the best platform
        if 'QT_QPA_PLATFORM' in os.environ:
            del os.environ['QT_QPA_PLATFORM']
    
    elif system == "windows":
        # On Windows, let Qt choose the best platform
        if 'QT_QPA_PLATFORM' in os.environ:
            del os.environ['QT_QPA_PLATFORM']

# Configure Qt platform before creating the application
configure_qt_platform()

sys.stderr = open(os.devnull, 'w')


class GUIController:
    @staticmethod
    def execute():
        stylesheet = """

        pre {
            font-size: 15px;
            line-height: 20px;
            max-width: 90%; /* Adjust this value as needed */
            margin-right: auto;
            overflow-wrap: break-word;
        }
        
        p {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QCheckBox {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QLabel {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QTextEdit {
            font-size: 15px;
            line-height: 5px;
            padding: 2px; /* Top, Right, Bottom, Left */
        }
        
        QScrollArea {
            border: none;
            background: white; /* This will be the color of the 'margin' */
        }

        QScrollBar:vertical {
            border: none;
            background: lightgray; /* This should match the QScrollArea background */
            width: 2px;
        }

        QScrollBar::handle:vertical {
            background: gray;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            border: none;
            background: lightgray; /* This should match the QScrollArea background */
            height: 6px;
            margin: 4px 0 0 0; /* Vertical margin space */

        }
    
        QScrollBar::handle:horizontal {
            background: gray;
            min-width: 20px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            width: 0px;
        }

        
        """

        app = QApplication(sys.argv)
        
        ex = BaseWindow()
        ex.show()
        icon_path = resource_path('images/BioSynth.png')
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        app.setStyleSheet(stylesheet)
        sys.exit(app.exec_())

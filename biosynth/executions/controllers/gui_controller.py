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
        # Check if we're in a headless environment (like CI/CD)
        if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
            print("Warning: No display server detected. This appears to be a headless environment.")
            print("Setting Qt platform to 'minimal' for headless operation.")
            os.environ['QT_QPA_PLATFORM'] = 'minimal'
            return
        
        # On Linux with display, set xcb as the preferred platform
        # If it fails, Qt will automatically fall back to other available platforms
        os.environ['QT_QPA_PLATFORM'] = 'xcb'
        
        # Also set some helpful environment variables for debugging
        os.environ['QT_LOGGING_RULES'] = 'qt.qpa.*=true'
        
        # Force Qt to use X11 backend if available
        if 'DISPLAY' in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'xcb'
        elif 'WAYLAND_DISPLAY' in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'wayland'
        else:
            # Fallback to minimal platform for headless environments
            os.environ['QT_QPA_PLATFORM'] = 'minimal'
    
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

        try:
            app = QApplication(sys.argv)
            
            ex = BaseWindow()
            ex.show()
            icon_path = resource_path('images/BioSynth.png')
            icon = QIcon(icon_path)
            app.setWindowIcon(icon)
            app.setStyleSheet(stylesheet)
            sys.exit(app.exec_())
            
        except Exception as e:
            error_msg = str(e).lower()
            if ("platform plugin" in error_msg or "qt.qpa" in error_msg or 
                "could not load" in error_msg or "failed to start" in error_msg):
                
                print(f"Qt platform error detected: {e}")
                print("\nThis is a common issue on Ubuntu/Linux systems.")
                
                # Check if we're in a CI environment
                if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS') or os.environ.get('RUNNER_OS'):
                    print("\n=== CI/CD Environment Detected ===")
                    print("You appear to be running in a CI/CD environment (GitHub Actions, etc.).")
                    print("GUI applications typically cannot run in headless CI environments.")
                    print("\nFor testing purposes, consider:")
                    print("1. Running only CLI tests in CI")
                    print("2. Using a headless Qt platform: export QT_QPA_PLATFORM=offscreen")
                    print("3. Skipping GUI tests in CI environment")
                    print("\nIf you need to test GUI functionality, consider using a service like:")
                    print("- GitHub Actions with Xvfb (virtual display)")
                    print("- Docker containers with display forwarding")
                    sys.exit(1)
                
                print("Attempting to use alternative platform...")
                
                # Try with minimal platform as fallback
                try:
                    print("Retrying with minimal platform...")
                    os.environ['QT_QPA_PLATFORM'] = 'minimal'
                    
                    app = QApplication(sys.argv)
                    ex = BaseWindow()
                    ex.show()
                    icon_path = resource_path('images/BioSynth.png')
                    icon = QIcon(icon_path)
                    app.setWindowIcon(icon)
                    app.setStyleSheet(stylesheet)
                    sys.exit(app.exec_())
                    
                except Exception as e2:
                    print(f"Minimal platform also failed: {e2}")
                    print("\n=== Qt Platform Plugin Issue ===")
                    print("Available platforms: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb")
                    print("\n=== Solution ===")
                    print("Please install the required system packages:")
                    print("sudo apt update")
                    print("sudo apt install -y python3-pyqt5 python3-pyqt5.qtcore python3-pyqt5.qtgui python3-pyqt5.qtwidgets")
                    print("sudo apt install -y libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xfixes0")
                    print("sudo apt install -y libxcb-shape0 libxcb-sync1 libxcb-xkb1 libxkbcommon-x11-0")
                    print("\nAfter installation, try running the application again.")
                    sys.exit(1)
            else:
                # Re-raise if it's not a platform issue
                raise e

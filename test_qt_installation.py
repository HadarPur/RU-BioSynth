#!/usr/bin/env python3
"""
Simple Qt installation test script for BioSynth
This script helps diagnose Qt platform plugin issues on Linux systems.
"""

import os
import sys
import platform

def test_qt_installation():
    """Test Qt installation and available platforms."""
    print("=== Qt Installation Test for BioSynth ===\n")
    
    # Check system information
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    
    # Check environment variables
    print(f"\nDisplay Environment:")
    print(f"  DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    print(f"  WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'Not set')}")
    print(f"  QT_QPA_PLATFORM: {os.environ.get('QT_QPA_PLATFORM', 'Not set')}")
    
    # Try to import PyQt6
    try:
        print("\n=== PyQt6 Import Test ===")
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QCoreApplication
        print("✓ PyQt6 imported successfully")
        
        # Check available platforms
        print("\n=== Available Qt Platforms ===")
        platforms = QCoreApplication.instance().availablePlatforms() if QCoreApplication.instance() else []
        if platforms:
            for platform in platforms:
                print(f"  - {platform}")
        else:
            print("  No platforms detected")
        
        # Test platform creation
        print("\n=== Platform Creation Test ===")
        try:
            # Try to create a minimal application
            app = QApplication([])
            print("✓ QApplication created successfully")
            app.quit()
            print("✓ QApplication destroyed successfully")
        except Exception as e:
            print(f"✗ QApplication creation failed: {e}")
            
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        print("\nTo install PyQt6, run:")
        print("pip install PyQt6")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    return True

def test_specific_platform(platform_name):
    """Test a specific Qt platform."""
    print(f"\n=== Testing Platform: {platform_name} ===")
    
    try:
        os.environ['QT_QPA_PLATFORM'] = platform_name
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication([])
        print(f"✓ Platform '{platform_name}' works")
        app.quit()
        return True
    except Exception as e:
        print(f"✗ Platform '{platform_name}' failed: {e}")
        return False

if __name__ == "__main__":
    success = test_qt_installation()
    
    if success:
        print("\n=== Platform-Specific Tests ===")
        # Test common platforms
        platforms_to_test = ['xcb', 'wayland', 'minimal', 'offscreen']
        for platform in platforms_to_test:
            test_specific_platform(platform)
    
    print("\n=== Recommendations ===")
    if platform.system().lower() == "linux":
        print("If you're experiencing Qt platform issues on Linux:")
        print("1. Install system packages:")
        print("   sudo apt install python3-pyqt5 python3-pyqt5.qtcore python3-pyqt5.qtgui python3-pyqt5.qtwidgets")
        print("   sudo apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xfixes0")
        print("   sudo apt install libxcb-shape0 libxcb-sync1 libxcb-xkb1 libxkbcommon-x11-0")
        print("2. Ensure you have a display server running (X11 or Wayland)")
        print("3. Try setting QT_QPA_PLATFORM environment variable:")
        print("   export QT_QPA_PLATFORM=xcb  # for X11")
        print("   export QT_QPA_PLATFORM=wayland  # for Wayland")
        print("   export QT_QPA_PLATFORM=minimal  # for headless")

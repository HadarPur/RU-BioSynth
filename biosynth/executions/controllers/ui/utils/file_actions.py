"""File-IO callbacks wired into UI buttons (download, save-as, copy)."""

import os

from PyQt5.QtWidgets import QApplication, QFileDialog

from biosynth.utils.file_utils import save_file


def download_file(code_display, file_date, update_status):
    filename = f'Optimized-Sequence_{file_date}.txt'
    text = code_display.toPlainText()
    path = f"Optimized sequence downloaded to: {save_file(text, filename)}"
    update_status(path)


def save_to_file(code_display, update_status):
    text = code_display.toPlainText()
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(
        None, "Save File", download_path, "Text Files (*.txt);", options=options
    )

    if filename:
        try:
            with open(filename, 'w') as file:
                file.write(text)
                update_status(filename)
        except Exception as e:
            update_status(f"Failed to save file: {e}")


def copy_to_clipboard(code_display, update_status):
    text = code_display.toPlainText()
    QApplication.clipboard().setText(text)
    update_status("Sequence copied to clipboard")

import os
import shutil
import sys


# Define a base class for reading data from a file.
class FileDataReader:
    def __init__(self, file_path):
        """
        Initializes a FileDataReader object.

        :param: file_path: Path to the file to be read.
        """
        self.file_path = file_path

    def read_lines(self):
        """
        Reads the lines from the specified file.

        :return: A list containing the lines read from the file.
        """
        with open(self.file_path, 'r') as file:
            return file.readlines()


# Inherit from FileDataReader to read sequences from a file.
class SequenceReader(FileDataReader):
    def read_sequence(self):
        """
        Reads a sequence from the file, removing leading/trailing whitespace.

        :return: A string representing a sequence, or None if no valid sequence is found.
        """
        raw_seq = self.read_lines()
        for line in raw_seq:
            if line.isspace():
                continue
            return line.strip()
        return None


# Inherit from FileDataReader to read patterns from a file.
class PatternReader(FileDataReader):
    def read_patterns(self):
        """
        Reads patterns from the file, splitting them by commas and adding to a set.

        :return: A set containing the extracted patterns.
        """
        res = set()
        raw_patterns = self.read_lines()
        for line in raw_patterns:
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.update(patterns)
        return res


def create_dir(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as error:
        return f"Creation of the directory '{directory}' failed because of {error}"


def delete_dir(directory):
    try:
        shutil.rmtree(directory)
    except OSError as error:
        return f"Deleting of the directory '{directory}' failed because of {error}"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
import os
import re
import shutil
import sys
from pathlib import Path

import numpy as np


def read_codon_usage_map(raw_lines):
    """
    Reads the codon usage table from the file and parses it into a dictionary.

    :return: A dictionary where keys are codons and values are dictionaries with frequency and epsilon.
    """

    # Read all lines from the file
    codon_usage_data = {}

    # Parse each line to extract codon and frequency data
    for line in raw_lines:
        parts = line.split()
        if len(parts) in {4, 5, 6}:  # Process lines with valid lengths
            codon = parts[-4]  # Codon is always the 4th element from the end
            frequency = float(parts[-1])  # Frequency is always the last element

        codon_data = {
            "frequency": frequency,
            "epsilon": np.log(frequency) if frequency > 0 else float('-inf')  # Handle log(0) case
        }
        codon_usage_data[codon] = frequency

    return codon_usage_data


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

        if self.file_path is None:
            return None

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

        if self.file_path is None:
            return None

        res = set()
        raw_patterns = self.read_lines()
        for line in raw_patterns:
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.update(patterns)
        return res


# Inherit from FileDataReader to read the codon usage table from a file.
class CodonUsageReader(FileDataReader):
    def read_codon_usage(self):
        """
        Reads the codon usage table from the file and parses it into a dictionary.

        :return: A dictionary where keys are codons and values are dictionaries with frequency and epsilon.
        """
        if self.file_path is None:
            return None

        # Read all lines from the file
        raw_lines = self.read_lines()
        return read_codon_usage_map(raw_lines)


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


def save_file(output, filename, path=None):
    try:
        # Convert path to Path object if it's not None
        if path:
            output_path = Path(path) / 'BioSynth Outputs'
        else:
            downloads_path = Path.home() / 'Downloads'
            output_path = downloads_path / 'BioSynth Outputs'

        # Replace colons with underscores in the filename
        filename = re.sub(':', '_', filename)

        # Create the directory if it doesn't exist
        create_dir(output_path)

        # Save the file
        output_file_path = output_path / filename
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(output)

        return f"File saved successfully at: {output_file_path}"

    except FileNotFoundError:
        return "Error: File not found."
    except PermissionError:
        return "Error: Permission denied."
    except IsADirectoryError:
        return "Error: The specified path is a directory, not a file."
    except Exception as e:
        return f"An error occurred: {e}"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import os
import re
import shutil
import sys
from pathlib import Path

from biosynth.utils.output_utils import Logger


def read_codon_freq_file(raw_lines, convert_to_dna=True):
    """
    Reads a codon-frequency file with 2 columns: codon and frequency.
    Example of valid line: ATG 0.02

    :param raw_lines: Iterable of lines (e.g., file.readlines()).
    :param convert_to_dna: If True, replaces 'U' with 'T' in codons (RNA to DNA).
    :return: Dictionary {codon: frequency}
    """
    codon_usage = {}

    for line_num, line in enumerate(raw_lines, start=1):
        line = line.strip()
        if not line:
            continue  # allow blank lines

        parts = line.split()
        if len(parts) != 2:
            Logger.error(f"Invalid format in codon usage file at line {line_num}: '{line}'. "
                         "Expected format: CODON FREQUENCY (e.g., ACG 0.02)")
            sys.exit(2)

        codon = parts[0].upper()
        if convert_to_dna:
            codon = codon.replace("U", "T")

        # Validate codon: must be exactly 3 chars, only A/T/C/G
        if len(codon) != 3 or any(base not in "ATCGU" for base in codon):
            Logger.error(f"Invalid codon '{codon}' at line {line_num}. Must be 3 letters A/T/C/G (or U before conversion).")
            sys.exit(2)

        try:
            freq = float(parts[1])
        except ValueError:
            Logger.error(f"Invalid frequency value '{parts[1]}' for codon '{codon}' at line {line_num}. Must be a float.")
            sys.exit(2)

        codon_usage[codon] = freq

    return codon_usage



# Define a base class for reading data from a file.
class FileDataReader:
    def __init__(self, file_path):
        """
        Initializes a FileDataReader object.

        :param file_path: Path to the file to be read.
        """
        self.file_path = file_path

    def read_lines(self):
        """
        Reads the lines from the specified file.

        :return: A list containing the lines read from the file.
        """
        try:
            with open(self.file_path, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            error_msg = f"File not found - {self.file_path}. Please check if the path is correct."
            Logger.error(error_msg)
            sys.exit(2)

# Inherit from FileDataReader to read sequences from a file.
class SequenceReader(FileDataReader):
    def read_sequence(self):
        """
        Reads a sequence from the file, removing leading/trailing whitespace.

        :return: A string representing a sequence, or None if no valid sequence is found.
        """

        if self.file_path is None:
            Logger.error("Target sequence file path is not set. Cannot proceed without a valid file.")
            sys.exit(2)

        raw_seq = [line.strip() for line in self.read_lines() if not line.isspace()]

        if len(raw_seq) == 0:
            Logger.error(f"No valid sequence found in {self.file_path}. File must contain exactly one sequence line.")
            sys.exit(2)

        if len(raw_seq) > 1:
            Logger.error(f"Invalid format in {self.file_path}: multiple lines detected. "
                         "Sequence file must contain exactly one line without line breaks.")
            sys.exit(2)

        return raw_seq[0]

# Inherit from FileDataReader to read patterns from a file.
class PatternReader(FileDataReader):
    def read_patterns(self):
        """
        Reads patterns from the file, splitting them by commas and adding to a set.

        :return: A set containing the extracted patterns.
        """

        if self.file_path is None:
            Logger.error("Unwanted patterns file path is not set. Cannot proceed without a valid file.")
            sys.exit(2)

        res = set()
        raw_patterns = self.read_lines()

        for line_num, line in enumerate(raw_patterns, start=1):
            if line.isspace():
                continue

            pattern = line.strip()

            # invalid if contains spaces or commas
            if " " in pattern or "," in pattern:
                Logger.error(
                    f"Invalid format in {self.file_path} at line {line_num}: "
                    f"'{pattern}'. Each pattern must be a single token with no spaces or commas."
                )
                sys.exit(2)

            res.add(pattern)

        return res


# Inherit from FileDataReader to read the codon usage table from a file.
class CodonUsageReader(FileDataReader):
    def read_codon_usage(self):
        """
        Reads the codon usage table from the file and parses it into a dictionary.

        :return: A dictionary where keys are codons and values are dictionaries with frequency and epsilon.
        """

        if self.file_path is None:
            Logger.error("Codon usage file path is not set. Cannot proceed without a valid file.")
            sys.exit(2)

        raw_lines = self.read_lines()
        return read_codon_freq_file(raw_lines)

    def get_filename(self):
        """
        Returns the name of the file (excluding the path).

        :return: Filename as a string.
        """
        return os.path.basename(self.file_path)


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
            output_path = Path(path) / 'BioSynth-Outputs'
        else:
            downloads_path = Path.home() / 'Downloads'
            output_path = downloads_path / 'BioSynth-Outputs'

        # Replace colons with underscores in the filename
        filename = re.sub(':', '_', filename)
        base_name = filename.split('-')[0].strip()

        # Create the directory if it doesn't exist
        create_dir(output_path)

        # Save the file
        output_file_path = output_path / filename
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(output)

        return f"* {output_file_path}\n"

    except FileNotFoundError:
        return "An error occurred while saving the file - File not found."
    except PermissionError:
        return "An error occurred while saving the file - Permission denied."
    except IsADirectoryError:
        return "An error occurred while saving the file - the specified path is a directory, not a file."
    except Exception as e:
        return f"An error occurred while saving the file - {e}"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

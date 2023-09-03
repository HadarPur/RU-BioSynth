import re
from typing import Set
import sys


class DNASequencePrinter:
    """Utility class for printing DNA sequences, patterns, and cost tables."""

    def _find_color_boundaries(input_string: str):
        """Find the start and end positions of color codes in a given input string.

        Args:
            input_string (str): The string containing color codes.

        Returns:
            Tuple[list[int], list[int]]: Lists of start and end positions of color codes.
        """
        color_start_positions = []
        color_end_positions = []

        color_pattern = re.compile(r'\033\[\d+m')  # Regular expression for ANSI color codes
        matches = color_pattern.finditer(input_string)

        for match in matches:
            color_start_positions.append(match.start())
            color_end_positions.append(match.end())

        return color_start_positions, color_end_positions

    @staticmethod
    def print_sequence(S: str):
        """Print a DNA sequence, broken into groups of three bases.

        Args:
            S (str): DNA sequence to be printed.
        """
        title = "DNA sequence"
        print(f'\n{title}:\n\t' + ' '.join(S[i:i + 3] for i in range(0, len(S), 3)))

    @staticmethod
    def print_target_sequence(S: str):
        """Print a target DNA sequence, broken into groups of three bases.

        Args:
            S (str): Target DNA sequence to be printed.
        """
        title = "DNA target sequence"
        print(f'{title}:\n\t' + ' '.join(S[i:i + 3] for i in range(0, len(S), 3)))

    @staticmethod
    def print_patterns(unwanted_patterns: Set[str]):
        """Print a set of unwanted DNA patterns.

        Args:
            unwanted_patterns (Set[str]): Set of unwanted DNA patterns to be printed.
        """
        print(f"\nPattern list:\n\t{unwanted_patterns}")

    def split_string_every_n_chars(S: str, n: int):
        """Split a string into chunks of given length.

        Args:
            S (str): Input string to be split.
            n (int): Length of each chunk.

        Returns:
            List[str]: List of chunks.
        """
        return [S[i:i + n] for i in range(0, len(S), n)]

    @staticmethod
    def print_cost_table(S: str, C: list[dict[str, float]]):
        """Print a cost table for DNA sequences.

        Args:
            S (str): DNA sequence for which the cost table is generated.
            C (list[dict[str, float]]): List of dictionaries containing cost values.
        """
        if len(C) > 0:
            print("\nScoring scheme:")
            codons = DNASequencePrinter.split_string_every_n_chars(S, 3)
            colored_separator = "\033[91m{:<10}\033[0m".format("||")  # ANSI escape code for red text
            codon_table = "\t{:<13}{}".format(" ", colored_separator)
            for item in codons:
                codon_table += "{:<8} {:<8} {:<8}{} ".format(*item, colored_separator)

            print(codon_table)
            print('-' * ((3 * len(codon_table) // 4) + 6))

            for sigma in C[0].keys():
                for i in range(0, len(C), len(C)):
                    line = f"\tcost(i, {sigma}) = {colored_separator}"
                    line += ' '.join(["{:<8}".format("{:.6g}".format(c[sigma])) + (f'{colored_separator}' if (index + 1) % 3 == 0 and index < len(C)-1 else '') for index, c in enumerate(C[i: i + len(C)])])
                    line += "{}".format(colored_separator)
                    print(line)
                print('-' * ((3 * len(codon_table) // 4) + 6))

    @staticmethod
    def print_highlighted_sequence(S: str):
        """Print a DNA sequence with highlighted coding regions.

        Args:
            S (str): DNA sequence with color-coded regions.
        """
        title = "Highlighted coding regions for the above DNA sequence"

        color_starts, color_ends = DNASequencePrinter._find_color_boundaries(S)

        chunk_size = 3
        colored_chunks = []
        prev_end = 0

        for start, end in zip(color_starts, color_ends):
            colored_chunks.append(S[prev_end:start])
            colored_chunks.append(S[start:end])
            prev_end = end

        colored_chunks.append(S[prev_end:])

        # Insert a space after each entry in colored_chunks
        spaced_chunks = [
            " ".join(chunk[i:i + chunk_size] for i in range(0, len(chunk), chunk_size))
            if idx % 2 == 0
            else chunk
            for idx, chunk in enumerate(colored_chunks)
        ]

        print(f'\n{title}:\n\t' + ''.join(spaced_chunks))

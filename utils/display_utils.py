import re


def get_color_for_coding_region(color_counter):
    colors = ["red", "blue", "green", "orange", "purple"]
    color = colors[color_counter % len(colors)]
    color_counter += 1
    return color_counter, color


class SequenceUtils:
    """Utility class for printing DNA sequences, patterns, and cost tables."""

    @staticmethod
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
    def get_sequence(title: str, S: str):
        """Return a DNA sequence, broken into groups of three bases.

        Args:
            S (str): DNA sequence to be printed.
            title (str): The kind of the seq
        """
        return f'\n{title}:\n\t{S}'

    @staticmethod
    def get_patterns(unwanted_patterns: set):
        """Return a set of unwanted DNA patterns.

        Args:
            unwanted_patterns (set): Set of unwanted DNA patterns to be printed.
        """
        if unwanted_patterns:  # Check if the set is not empty
            formatted_patterns = ', '.join(
                sorted(unwanted_patterns))  # Convert set to a sorted list and join with commas
        else:
            formatted_patterns = "None"  # If the set is empty, indicate that there are no patterns
        return formatted_patterns

    @staticmethod
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
    def mark_non_equal_characters(input_seq, optimized_seq, coding_positions):
        """
        Marks non-equal characters between two sequences, distinguishing coding and non-coding regions.

        Args:
            input_seq (str): Original input sequence.
            optimized_seq (str): Optimized sequence to compare against the input sequence.
            coding_positions (list): Precomputed array where each index contains 0 for non-coding
                                    or 1, 2, 3 for coding positions.

        Returns:
            tuple: index_seq, marked_seq1, marked_seq2
                - index_seq: String representation of sequence indices.
                - marked_seq1: Marked input sequence with differences highlighted.
                - marked_seq2: Marked optimized sequence with differences highlighted.
        """
        if len(input_seq) != len(optimized_seq):
            raise ValueError("Input sequence and optimized sequence must be of the same length")

        marked_seq1 = []
        marked_seq2 = []
        index_seq = []

        i = 0
        while i < len(coding_positions):
            if coding_positions[i] != 0:
                # Coding region: process in codons (3 characters at a time)
                start = i
                while i < len(coding_positions) and coding_positions[i] != 0:
                    i += 1
                end = i

                for j in range(start, end, 3):
                    index_seq.append(f"{j + 1}-{j + 3}")
                    codon_input = input_seq[j:j + 3]
                    codon_optimized = optimized_seq[j:j + 3]
                    if codon_input != codon_optimized:
                        marked_seq1.append(f"[{codon_input}]")
                        marked_seq2.append(f"[{codon_optimized}]")
                    else:
                        marked_seq1.append(codon_input)
                        marked_seq2.append(codon_optimized)
            else:
                # Non-coding region: process single characters
                start = i
                while i < len(coding_positions) and coding_positions[i] == 0:
                    i += 1
                end = i

                for j in range(start, end):
                    index_seq.append(f"{j + 1}")
                    char_input = input_seq[j]
                    char_optimized = optimized_seq[j]
                    if char_input != char_optimized:
                        marked_seq1.append(f"[{char_input}]")
                        marked_seq2.append(f"[{char_optimized}]")
                    else:
                        marked_seq1.append(char_input)
                        marked_seq2.append(char_optimized)

        # Create formatted strings for output
        index_seq = ''.join([f'{i:12}' for i in index_seq])
        marked_seq1 = ''.join([f'{i:12}' for i in marked_seq1])
        marked_seq2 = ''.join([f'{i:12}' for i in marked_seq2])

        return index_seq, marked_seq1, marked_seq2

    @staticmethod
    def highlight_sequences_to_html(seq, coding_indexes):
        """
        Converts a DNA sequence to HTML markup with highlighted coding regions.

        Parameters:
            seq (str): The full DNA sequence.
            coding_indexes (list of tuples): List of (start, end) tuples representing coding regions.

        Returns:
            str: HTML markup with highlighted coding regions.
        """
        html_output = ""
        color_counter = 0

        # Define a list of colors for coding regions
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FF00FF', '#00FFFF', '#FFA500']

        last_end = 0  # Track the end of the last processed region

        for start, end in coding_indexes:
            # Add non-coding region before the current coding region
            if last_end < start:
                html_output += seq[last_end:start]

            # Add coding region with highlighted color
            coding_sequence = seq[start:end]
            spaced_triplets = ' '.join(coding_sequence[i:i + 3] for i in range(0, len(coding_sequence), 3))
            color = colors[color_counter % len(colors)]
            color_counter += 1
            html_output += f'<span style="color: {color};">&nbsp;&nbsp;{spaced_triplets}&nbsp;&nbsp;</span>'

            last_end = end

        # Add any remaining non-coding region after the last coding region
        if last_end < len(seq):
            html_output += seq[last_end:]

        return html_output

    @staticmethod
    def highlight_sequences_to_terminal(seq, coding_indexes):
        """
        Converts DNA sequences to terminal output with highlighted coding regions based on coding index ranges.

        Parameters:
            seq (str): The full DNA sequence.
            coding_indexes (list of tuples): List of (start, end) tuples representing coding regions.

        Returns:
            str: String with terminal escape codes for colorized coding regions.
        """
        output = ""
        color_counter = 0

        # ANSI color codes for highlighting coding regions
        colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

        # Process the sequence by iterating over coding and non-coding regions
        last_end = 0  # Track the end of the last processed region
        for start, end in coding_indexes:
            # Add non-coding region before the current coding region
            if last_end < start:
                output += seq[last_end:start]

            # Add coding region with highlighting
            subsequence = seq[start:end]
            color = colors[color_counter % len(colors)]
            color_counter += 1
            spaced_triplets = " ".join(subsequence[j:j + 3] for j in range(0, len(subsequence), 3))
            output += f" {color}{spaced_triplets}\033[0m "
            last_end = end

        # Add any remaining non-coding region after the last coding region
        if last_end < len(seq):
            output += seq[last_end:]

        return output

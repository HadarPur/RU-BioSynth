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
    def mark_non_equal_characters(input_seq, optimized_seq, region_list):
        if len(input_seq) != len(optimized_seq):
            raise ValueError("Target sequence and Optimized sequence must be of the same length")

        marked_seq1 = []
        marked_seq2 = []
        index_seq = []

        region_index = 0
        i = 0  # Initialize i outside the loop

        while i < len(input_seq):  # Use a while loop to allow flexible increment of i
            if region_index < len(region_list):
                seq = region_list[region_index]['seq']
                is_coding_region = region_list[region_index]['is_coding_region']

                j = 0  # Initialize j inside the loop
                while j < len(seq) and i + j < len(
                        input_seq):  # Ensure j doesn't exceed seq length or input_seq length
                    if is_coding_region:
                        index_seq.append(f"{i + j + 1}-{i + j + 3}")
                        # Compare 3 characters at a time
                        if input_seq[i + j:i + j + 3] != optimized_seq[i + j:i + j + 3]:
                            marked_seq1.append(f"[{input_seq[i + j:i + j + 3]}]")
                            marked_seq2.append(f"[{optimized_seq[i + j:i + j + 3]}]")
                        else:
                            marked_seq1.append(f"{input_seq[i + j:i + j + 3]}")
                            marked_seq2.append(f"{optimized_seq[i + j:i + j + 3]}")
                        j += 3
                    else:
                        index_seq.append(f"{i + j + 1}")
                        # Compare 1 character at a time
                        if input_seq[i + j] != optimized_seq[i + j]:
                            marked_seq1.append(f"[{input_seq[i + j]}]")
                            marked_seq2.append(f"[{optimized_seq[i + j]}]")
                        else:
                            marked_seq1.append(f"{input_seq[i + j]}")
                            marked_seq2.append(f"{optimized_seq[i + j]}")
                        j += 1

                # Move to the next region if applicable
                i += j

                # Increment region_index
                region_index += 1

        # Create the index sequence string
        index_seq = ''.join([f'{i:12}' for i in index_seq])
        marked_seq1 = ''.join([f'{i:12}' for i in marked_seq1])
        marked_seq2 = ''.join([f'{i:12}' for i in marked_seq2])

        return index_seq, marked_seq1, marked_seq2

    @staticmethod
    def highlight_sequences_to_html(sequences):
        """
        Converts DNA sequences to HTML markup with highlighted coding regions.

        Parameters:
            sequences (list of dict): List of dictionaries containing sequences and flags for coding regions.

        Returns:
            str: HTML markup with highlighted coding regions.
        """
        html_output = ""
        color_counter = 0

        for seq_info in sequences:
            if seq_info['is_coding_region']:
                coding_sequence = seq_info["seq"]
                coding_sequence_with_spaces = ''.join(
                    coding_sequence[i:i + 3] for i in range(0, len(coding_sequence), 3))
                color_counter, color = get_color_for_coding_region(color_counter)
                html_output += f'<span style="color: {color};">&nbsp;&nbsp;&nbsp;&nbsp;{coding_sequence_with_spaces}&nbsp;&nbsp;&nbsp;&nbsp;</span>'
            else:
                html_output += f"{seq_info['seq']}"

        return html_output

    @staticmethod
    def highlight_sequences_to_terminal(sequences):
        """
        Converts DNA sequences to terminal output with highlighted coding regions.

        Parameters:
            sequences (list of dict): List of dictionaries containing sequences and flags for coding regions.

        Returns:
            str: String with terminal escape codes for colorized coding regions.
        """
        output = ""
        color_counter = 0

        # ANSI color codes
        colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

        for seq_info in sequences:
            if seq_info['is_coding_region']:
                coding_sequence = seq_info["seq"]
                coding_sequence_with_spaces = ''.join(
                    coding_sequence[i:i + 3] for i in range(0, len(coding_sequence), 3))
                # Get the next color from the colors list, and wrap around if needed
                color = colors[color_counter % len(colors)]
                color_counter += 1
                # Append the colorized sequence
                output += f' {color}{coding_sequence_with_spaces}\033[0m '  # Reset color at the end
            else:
                # Non-coding regions will not be colorized
                output += seq_info['seq']

        return output


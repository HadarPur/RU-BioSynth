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
    def get_pattern_occurrences(sequence: str, unwanted_patterns: set, per_line: int = 6):
        """Return per-pattern occurrence rows (overlapping matches, 1-based positions).

        Args:
            sequence (str): DNA sequence to scan.
            unwanted_patterns (set): Patterns to locate in the sequence.
            per_line (int): Number of position ranges per line in the "Positions" cell.

        Returns:
            list[dict]: Rows with keys "Pattern", "Count", "Positions".
        """
        rows = []
        for pattern in sorted(unwanted_patterns):
            ranges = []
            start = 0
            while True:
                idx = sequence.find(pattern, start)
                if idx == -1:
                    break
                ranges.append((idx + 1, idx + len(pattern)))
                start = idx + 1  # overlapping matches

            tokens = []
            if ranges:
                tokens = [f"{s}-{e}" for s, e in ranges]

            rows.append({
                "Pattern": pattern,
                "Count": len(ranges),
                "Positions": tokens,
            })
        return rows

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
            raise ValueError(
                f"Input sequence and optimized sequence must be of the same length:\nlen(input_seq) = {len(input_seq)} != len(optimized_seq) = {len(optimized_seq)}")

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
    def highlight_sequences_to_html(seq, coding_index, line_length=96, returnBr=False, addressable=False, highlight_ranges=None):
        """
        Highlights a single coding region in an HTML-formatted DNA sequence.

        Args:
            seq (str): DNA sequence
            coding_index (tuple[int, int] | None): (start, end) coding region indices (end exclusive)
            line_length (int): characters per line
            returnBr (bool): whether to insert <br> between lines
            addressable (bool): when True, wrap every base in a <span class="base"
                data-pos="N"> so client-side JS can target individual positions
                (1-based).
            highlight_ranges (list[tuple[int, int]] | None): optional list of
                (start, end) 1-based inclusive ranges to render with a
                background highlight. Use this for non-JS renderers (e.g. Qt's
                limited HTML subset) that cannot toggle styles dynamically.

        Returns:
            str: HTML-formatted sequence
        """
        base_colors = [''] * len(seq)
        base_highlight = [False] * len(seq)

        if coding_index is not None:
            start, end = coding_index
            coding_color = "#b03a48"

            for j in range(start, end):
                base_colors[j] = coding_color

        if highlight_ranges:
            for s, e in highlight_ranges:
                for j in range(max(0, s - 1), min(len(seq), e)):
                    base_highlight[j] = True

        html_lines = []
        for i in range(0, len(seq), line_length):
            line = ""
            for j in range(i, min(i + line_length, len(seq))):
                base = seq[j]
                color = base_colors[j]
                highlighted = base_highlight[j]

                if addressable:
                    style = f' style="color: {color};"' if color else ''
                    line += f'<span class="base" data-pos="{j + 1}"{style}>{base}</span>'
                elif highlighted:
                    color_css = f'color: {color}; ' if color else ''
                    line += f'<span style="{color_css}background: #ffe066;">{base}</span>'
                elif color:
                    line += f'<span style="color: {color};">{base}</span>'
                else:
                    line += base

            html_lines.append(line)

        return '<br>'.join(html_lines) if returnBr else ''.join(html_lines)

    @staticmethod
    def highlight_differences_with_coding_html(
            input_seq,
            optimized_seq,
            coding_positions,
            line_length=96
    ):
        if len(input_seq) != len(optimized_seq):
            raise ValueError(
                f"input_seq and optimized_seq must be the same length:\n"
                f"len(input_seq)={len(input_seq)}, "
                f"len(optimized_seq)={len(optimized_seq)}"
            )

        marked_seq = []
        expanded_coding_region = None

        i = 0
        marked_index = 0  # index in expanded (bracketed) string

        while i < len(coding_positions):

            # ===============================
            # FULL CODING REGION
            # ===============================
            if coding_positions[i] != 0:
                start = i
                while i < len(coding_positions) and coding_positions[i] != 0:
                    i += 1
                end = i

                # coding region start in expanded string
                coding_start_marked = marked_index

                for j in range(start, end, 3):
                    codon_input = input_seq[j:j + 3]
                    codon_optimized = optimized_seq[j:j + 3]

                    # Partial codon safety
                    if len(codon_optimized) < 3:
                        for k in range(len(codon_optimized)):
                            if codon_input[k] != codon_optimized[k]:
                                marked_seq.append(f"[{codon_optimized[k]}]")
                                marked_index += 3
                            else:
                                marked_seq.append(codon_optimized[k])
                                marked_index += 1
                        continue

                    if codon_input != codon_optimized:
                        marked_seq.append(f"[{codon_optimized}]")
                        marked_index += 5  # [XYZ]
                    else:
                        marked_seq.append(codon_optimized)
                        marked_index += 3

                # coding region end in expanded string
                coding_end_marked = marked_index

                # EXACTLY ONE CODING REGION
                expanded_coding_region = (coding_start_marked, coding_end_marked)

            # ===============================
            # NON-CODING REGION
            # ===============================
            else:
                start = i
                while i < len(coding_positions) and coding_positions[i] == 0:
                    i += 1
                end = i

                for j in range(start, end):
                    if input_seq[j] != optimized_seq[j]:
                        marked_seq.append(f"[{optimized_seq[j]}]")
                        marked_index += 3
                    else:
                        marked_seq.append(optimized_seq[j])
                        marked_index += 1

        marked_optimized = ''.join(marked_seq)

        return SequenceUtils.highlight_sequences_to_html(
            marked_optimized,
            expanded_coding_region,
            line_length
        )

    @staticmethod
    def highlight_sequence_to_terminal(seq, coding_range):
        """
        Converts a DNA sequence to terminal output with a highlighted coding region.

        Parameters:
            seq (str): The full DNA sequence.
            coding_range (tuple): (start, end) tuple representing the coding region (0-based, end-exclusive).

        Returns:
            str: String with terminal escape codes for the highlighted coding region.
        """
        start, end = coding_range

        # ANSI color code for highlighting the coding region
        color = '\033[36m'  # green
        reset = '\033[0m'

        # Non-coding before coding region
        before_coding = seq[:start]

        # coding region with triplet spacing
        coding_region = seq[start:end]

        # Non-coding after coding region
        after_coding = seq[end:]

        output = f"{before_coding}{color}{coding_region}{reset}{after_coding}"

        return output

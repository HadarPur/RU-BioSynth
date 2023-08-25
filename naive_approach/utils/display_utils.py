import re
from typing import Set


class DNASequencePrinter:
    def __init__(self):
        pass

    def _find_color_boundaries(input_string: str):
        color_start_positions = []
        color_end_positions = []

        color_pattern = re.compile(r'\033\[\d+m')
        matches = color_pattern.finditer(input_string)

        for match in matches:
            color_start_positions.append(match.start())
            color_end_positions.append(match.end())

        return color_start_positions, color_end_positions

    @staticmethod
    def print_sequence(S: str):
        title = "DNA sequence"
        print(f'\n{title}:\n\t' + ' '.join(S[i:i + 3] for i in range(0, len(S), 3)))

    @staticmethod
    def print_target_sequence(S: str):
        title = "DNA target sequence"
        print(f'\n{title}:\n\t' + ' '.join(S[i:i + 3] for i in range(0, len(S), 3)))

    @staticmethod
    def print_patterns(unwanted_patterns: Set[str]):
        print(f"\nPattern list:\n\t{unwanted_patterns}")

    @staticmethod
    def print_cost_table(C: list[dict[str, float]]):
        """print Cost

        Args:
            C (list[dict[str, float]]): Cost
        """
        if len(C) > 0:
            print("\ncost:")
            for sigma in C[0].keys():
                for i in range(0, len(C), 12):
                    print(
                        f"\tcost(i, {sigma}) = {' '.join([f'{c[sigma]}' for c in C[i: i + 12]])}")
                print('-' * 100)

    @staticmethod
    def print_highlighted_sequence(S: str):
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

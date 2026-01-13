from pathlib import Path


class InputData:
    # Input Data
    dna_sequence = None
    cleaned_dna_sequence = None
    unwanted_patterns = None

    orf_sequence = None
    orf_indexes = None

    coding_positions = None

    @staticmethod
    def reset():
        InputData.dna_sequence = None
        InputData.cleaned_dna_sequence = None
        InputData.unwanted_patterns = None
        InputData.orf_sequence = None
        InputData.orf_indexes = None
        InputData.coding_positions = None

class CostData:
    codon_usage = None
    codon_usage_filename = None

    alpha = 1.0
    beta = 2.0
    w = 100.
    stop_codon = float('inf')


class EliminationData:
    info = None
    detailed_changes = None
    min_cost = None


class OutputData:
    output_path = Path.home() / 'Downloads'
    optimized_sequence = None

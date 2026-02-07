from pathlib import Path


class InputData:
    # Input Data
    dna_sequence = None
    cleaned_dna_sequence = None

    unwanted_patterns = None

    start_codon_identified = None
    coding_indexes = None

    coding_positions = None

    @staticmethod
    def reset():
        InputData.dna_sequence = None
        InputData.cleaned_dna_sequence = None
        InputData.unwanted_patterns = None
        InputData.coding_indexes = None
        InputData.coding_positions = None

# Only for gui uploads
class UploadData:
    # Uploaded files
    dna_sequence_content_file = None
    unwanted_patterns_content_file = None
    codon_usage_content_file = None

    @staticmethod
    def reset():
        UploadData.dna_sequence_content_file = None
        UploadData.unwanted_patterns_content_file = None
        UploadData.codon_usage_content_file = None

class CostData:
    codon_usage = None
    codon_usage_filename = None

    alpha = 1.0
    beta = 2.0
    w = 100.
    stop_codon = float('inf')

    @staticmethod
    def reset():
        CostData.codon_usage = None
        CostData.codon_usage_filename = None

        CostData.alpha = 1.0
        CostData.beta = 2.0
        CostData.w = 100.
        CostData.stop_codon = float('inf')

class EliminationData:
    info = None
    detailed_changes = None
    min_cost = None


class OutputData:
    output_path = Path.home() / 'Downloads'
    optimized_sequence = None

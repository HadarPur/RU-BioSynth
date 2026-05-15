from pathlib import Path

from biosynth.utils.logger import Logger


class InputData:
    """Holds the raw and cleaned DNA input, unwanted patterns, and detected coding region metadata."""

    # Input Data
    dna_sequence = None
    cleaned_dna_sequence = None

    unwanted_patterns = None
    unwanted_patterns_occurrences = None

    start_codon_identified = None
    coding_indexes = None

    coding_positions = None

    @staticmethod
    def reset():
        """Clear all stored input fields back to ``None``."""
        InputData.dna_sequence = None
        InputData.cleaned_dna_sequence = None
        InputData.unwanted_patterns = None
        InputData.unwanted_patterns_occurrences = None
        InputData.coding_indexes = None
        InputData.coding_positions = None

# Only for gui uploads
class UploadData:
    """Holds the raw file contents uploaded through the GUI for sequence, patterns, and codon usage."""

    # Uploaded files
    dna_sequence_content_file = None
    unwanted_patterns_content_file = None
    codon_usage_content_file = None

    @staticmethod
    def reset():
        """Clear all uploaded file contents back to ``None``."""
        UploadData.dna_sequence_content_file = None
        UploadData.unwanted_patterns_content_file = None
        UploadData.codon_usage_content_file = None

class CostData:
    """Holds the codon usage table and cost-function parameters (alpha, beta, w, stop codon penalty)."""

    codon_usage = None
    codon_usage_filename = None

    alpha = 1.0
    beta = 2.0
    w = 100.
    stop_codon = float('inf')

    optimized_codon = True

    @staticmethod
    def reset():
        """Restore codon usage and cost-function parameters to their defaults."""
        CostData.codon_usage = None
        CostData.codon_usage_filename = None

        CostData.alpha = 1.0
        CostData.beta = 2.0
        CostData.w = 100.
        CostData.stop_codon = float('inf')

        CostData.optimized_codon = True

class EliminationData:
    """Holds elimination-algorithm outputs: process info, cost contributions, substitutions, and min cost."""

    info = None
    cost_contribution = None
    cost_substitution = None
    min_cost = None


class OutputData:
    """Holds the optimized sequence and the destination path for exported results."""

    output_path = Path.home() / 'Downloads'
    optimized_sequence = None

from biosynth.algorithm.eliminate_sequence import EliminationController
from biosynth.data.app_data import EliminationData, OutputData
from biosynth.report.report_builder import ReportBuilder
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.logger import Logger


def is_valid_dna(sequence):
    """Return ``True`` if every character in ``sequence`` is one of A/T/C/G/U/* (case-insensitive)."""
    valid_bases = set('ATCGU*')
    return all(base in valid_bases for base in sequence.upper())


def is_valid_patterns(patterns):
    """Return ``True`` if every pattern contains only A/T/C/G/U bases (case-insensitive)."""
    valid_bases = set('ATCGU')
    for pattern in patterns:
        if not all(base in valid_bases for base in pattern.upper()):
            return False
    return True


def is_valid_codon_usage(codon_usage):
    """
    Validates the codon usage data.

    :param codon_usage: A dictionary where keys are codons and values are dictionaries with 'aa' and 'freq'.
                        Example: {"AAA": {"aa": "K", "freq": 0.5}}
    :return: True if the codon usage data is valid, otherwise False.
    """
    valid_bases = set('ATCG')

    if len(codon_usage) != 64:
        return False

    for codon, freq in codon_usage.items():
        # Validate codon format
        if not (isinstance(codon, str) and len(codon) == 3 and all(base in valid_bases for base in codon.upper())):
            return False

        # Validate 'freq' field
        if not (isinstance(freq, (float, int)) and freq >= 0):
            return False

    return True


def is_valid_input(sequence, unwanted_patterns, codon_usage_table):
    """Validate the three primary inputs and log specific errors for any failure.

    Args:
        sequence: Target DNA sequence string.
        unwanted_patterns: Iterable of pattern strings to eliminate.
        codon_usage_table: Codon usage mapping to validate.

    Returns:
        True if all inputs are present and well-formed, otherwise False.
    """
    if sequence is None:
        Logger.error(f"Sequence file is missing.")
        return False

    if len(sequence) == 0:
        Logger.error(f"Invalid sequence format in file.")
        return False

    if not is_valid_dna(sequence):
        Logger.error(f"Invalid sequence format in file.")
        return False

    if unwanted_patterns is None:
        Logger.error(f"Unwanted Patterns file is missing.")
        return False

    if len(unwanted_patterns) == 0:
        Logger.error(f"Invalid unwanted patterns format in file.")
        return False

    if not is_valid_patterns(unwanted_patterns):
        Logger.error(f"Invalid unwanted patterns format in file.")
        return False

    if codon_usage_table is None:
        Logger.error(f"Codon Usage file is missing.")
        return False

    if len(codon_usage_table) == 0:
        Logger.error(f"Invalid codon usage table format in file.")
        return False

    if not is_valid_codon_usage(codon_usage_table):
        Logger.error(f"Invalid codon usage table format in file.")
        return False

    return True


def is_valid_cost(alpha=None, beta=None, w=None):
    """Validate cost-function parameters and the biological constraints ``alpha < beta`` and ``beta << w``.

    Args:
        alpha: Coding-region cost weight; must be a positive number.
        beta: Pattern-occurrence cost weight; must be a positive number.
        w: Non-coding-region cost weight; must be a positive number much larger than ``beta``.

    Returns:
        True if all values are positive and satisfy the required ordering, otherwise False.
    """
    if not (isinstance(alpha, (int, float)) and alpha > 0):
        Logger.error(f"Invalid alpha value: α = {alpha}. Must be a positive number.")
        return False

    if not (isinstance(beta, (int, float)) and beta > 0):
        Logger.error(f"Invalid beta value: β = {beta}. Must be a positive number.")
        return False

    if not (isinstance(w, (int, float)) and w > 0):
        Logger.error(f"Invalid w value: w = {w}. Must be a positive number.")
        return False

    if not (alpha < beta):
        Logger.error(f"Biological Constraint violated: α < β required "
                     f"(α={alpha}, β={beta}).")
        return False

    MUCH_LESS_FACTOR = 10  # Define a factor to ensure beta is significantly smaller than w
    if not (beta * MUCH_LESS_FACTOR < w):
        Logger.error(
            f"Constraint violated: β ≪ w required "
            f"(β={beta}, w={w}, factor={MUCH_LESS_FACTOR})."
        )
        return False

    return True

import time

def eliminate_unwanted_patterns(seq, unwanted_patterns, coding_positions):
    """Run the elimination algorithm and persist its outputs into ``EliminationData`` and ``OutputData``."""
    # Start elimination
    start_time = time.perf_counter()

    EliminationData.info, EliminationData.cost_contribution, EliminationData.cost_substitution, OutputData.optimized_sequence, EliminationData.min_cost = EliminationController.eliminate(
        seq, unwanted_patterns, coding_positions)

    end_time = time.perf_counter()
    Logger.critical(f"Total execution time: {end_time - start_time:.3f} seconds")


def mark_non_equal_codons(input_seq, optimized_seq, coding_positions):
    """Compute a marked diff between input and optimized sequences.

    Returns:
        Tuple of (index string, marked input sequence, marked optimized sequence).
    """
    index_seq_str, marked_input_seq, marked_optimized_seq = SequenceUtils.mark_non_equal_characters(input_seq,
                                                                                                    optimized_seq,
                                                                                                    coding_positions)
    return index_seq_str, marked_input_seq, marked_optimized_seq


def initialize_report():
    """Construct and return a fresh ``ReportBuilder`` initialized from current app data."""
    report = ReportBuilder()
    return report

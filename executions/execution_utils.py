from algorithm.eliminate_sequence import EliminationController
from data.app_data import EliminationData, OutputData
from report.html_report_utils import ReportController
from utils.display_utils import SequenceUtils
from utils.output_utils import Logger


def is_valid_dna(sequence):
    valid_bases = set('ATCG')
    return all(base in valid_bases for base in sequence.upper())


def is_valid_patterns(patterns):
    valid_bases = set('ATCG')
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

    for codon, data in codon_usage.items():
        # Validate codon format
        if not (isinstance(codon, str) and len(codon) == 3 and all(base in valid_bases for base in codon.upper())):
            return False

        # Validate 'aa' field
        aa = data.get('aa')
        if not (isinstance(aa, str) and len(aa) == 3 and aa.isalpha()):
            return False

        # Validate 'freq' field
        freq = data.get('freq')
        if not (isinstance(freq, (float, int)) and freq >= 0):
            return False

    return True

def is_valid_input(sequence, unwanted_patterns, codon_usage_table):
    if sequence is None:
        Logger.error("Unfortunately, we couldn't find any sequence file. Please insert one and try again.")
        return False

    if len(sequence) == 0:
        Logger.error("Unfortunately, the sequence file is empty. Please insert fully one and try again.")
        return False

    if not is_valid_dna(sequence):
        Logger.error(f"The sequence:\n{sequence}\n\nis not valid, please check and try again later.")
        return False

    if unwanted_patterns is None:
        Logger.error("Unfortunately, we couldn't find any patterns file. Please insert one and try again.")
        return False

    if len(unwanted_patterns) == 0:
        Logger.error("Unfortunately, the patterns file is empty. Please insert fully one and try again.")
        return False

    if not is_valid_patterns(unwanted_patterns):
        Logger.error(f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
        return False

    if codon_usage_table is None:
        Logger.error("Unfortunately, we couldn't find any codon usage file. Please insert one and try again.")
        return False

    if len(codon_usage_table) == 0:
        Logger.error("Unfortunately, the codon usage file is empty. Please insert fully one and try again.")
        return False

    if not is_valid_codon_usage(codon_usage_table):
        Logger.error(f"The codon_usage_table:\n{codon_usage_table}\n\nare not valid, please check and try again later.")
        return False

    return True


def eliminate_unwanted_patterns(seq, unwanted_patterns, coding_positions):
    # Start elimination
    EliminationData.info, EliminationData.detailed_changes, OutputData.optimized_sequence, EliminationData.min_cost = EliminationController.eliminate(
        seq, unwanted_patterns, coding_positions)


def mark_non_equal_codons(input_seq, optimized_seq, coding_positions):
    # Mark non-equal codons between the original and optimized sequences
    index_seq_str, marked_input_seq, marked_optimized_seq = SequenceUtils.mark_non_equal_characters(input_seq,
                                                                                                    optimized_seq,
                                                                                                    coding_positions)
    return index_seq_str, marked_input_seq, marked_optimized_seq


def initialize_report(updated_coding_positions):
    report = ReportController(updated_coding_positions)
    return report

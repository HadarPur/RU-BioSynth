from algorithm.eliminate_sequence import EliminationController
from report.pdf_report_utils import ReportController
from utils.cost_utils import CodonScorerFactory
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


def is_valid_input(sequence, unwanted_patterns):
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

    if len(sequence) == 0:
        Logger.error("Unfortunately, the patterns file is empty. Please insert fully one and try again.")
        return False

    if not is_valid_patterns(unwanted_patterns):
        Logger.error(f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
        return False

    return True


def eliminate_unwanted_patterns(seq, unwanted_patterns, selected_region_list):
    # Calculate scores for the regions using the CodonScorer
    scorer = CodonScorerFactory()
    cost_table = scorer.calculate_scores(selected_region_list)

    # Start elimination
    info, detailed_changes, target_seq, min_cost = EliminationController.eliminate(seq, unwanted_patterns, cost_table)

    return info, detailed_changes, target_seq, min_cost


def mark_non_equal_codons(input_seq, target_seq, region_list):
    # Mark non-equal codons between the original and target sequences
    index_seq_str, marked_input_seq, marked_target_seq = SequenceUtils.mark_non_equal_characters(input_seq, target_seq,
                                                                                                 region_list)
    return index_seq_str, marked_input_seq, marked_target_seq


def initialize_report(seq,
                      target_seq,
                      index_seq_str,
                      marked_input_seq,
                      marked_target_seq,
                      unwanted_patterns,
                      original_coding_regions,
                      original_region_list,
                      selected_regions_to_exclude,
                      selected_region_list,
                      min_cost,
                      detailed_changes):
    report = ReportController(seq,
                              target_seq,
                              index_seq_str,
                              marked_input_seq,
                              marked_target_seq,
                              unwanted_patterns,
                              original_coding_regions,
                              original_region_list,
                              selected_regions_to_exclude,
                              selected_region_list,
                              min_cost,
                              detailed_changes)
    return report

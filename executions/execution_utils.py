from algorithm.eliminate_sequence import EliminateSequence
from report.pdf_report_utils import Report
from utils.cost_utils import CodonScorer
from utils.display_utils import SequenceUtils


def is_valid_dna(sequence):
    valid_bases = set('ATCG')
    return all(base in valid_bases for base in sequence.upper())


def is_valid_patterns(patterns):
    valid_bases = set('ATCG')
    for pattern in patterns:
        if not all(base in valid_bases for base in pattern.upper()):
            return False
    return True


def eliminate_unwanted_patterns(seq, unwanted_patterns, selected_region_list):
    # Calculate scores for the regions using the CodonScorer
    scorer = CodonScorer()
    cost_table = scorer.calculate_scores(selected_region_list)

    # Start elimination
    info, detailed_changes, target_seq, min_cost = EliminateSequence.eliminate(seq, unwanted_patterns, cost_table)

    return info, detailed_changes, target_seq, min_cost


def mark_non_equal_codons(input_seq, target_seq, region_list):
    # Mark non-equal codons between the original and target sequences
    marked_input_seq, marked_target_seq, marked_seq = SequenceUtils.mark_non_equal_characters(input_seq, target_seq, region_list)
    return marked_input_seq, marked_target_seq, marked_seq


def initialize_report(seq,
                      target_seq,
                      marked_input_seq,
                      marked_target_seq,
                      unwanted_patterns,
                      original_coding_regions,
                      original_region_list,
                      selected_regions_to_exclude,
                      selected_region_list,
                      min_cost,
                      detailed_changes):

    report = Report(seq,
                    target_seq,
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

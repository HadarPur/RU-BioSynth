from utils.cost_utils import CodonScorer
from report.pdf_report_utils import Report
from algorithm.eliminate_sequence import EliminateSequence
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAHighlighter


def eliminate_unwanted_patterns(seq, unwanted_patterns, selected_region_list):
    # Calculate scores for the regions using the CodonScorer
    scorer = CodonScorer()
    cost_table = scorer.calculate_scores(selected_region_list)

    # Start elimination
    info, target_seq, min_cost = EliminateSequence.eliminate(seq, unwanted_patterns, cost_table)

    return info, target_seq, min_cost


def mark_non_equal_codons(region_list, target_seq):
    region_list_target = DNAHighlighter.get_coding_and_non_coding_regions(target_seq)

    # Mark non-equal codons between the original and target sequences
    marked_input_seq, marked_target_seq, marked_seq = SequenceUtils.mark_non_equal_codons(region_list,
                                                                                          region_list_target)
    return marked_input_seq, marked_target_seq, marked_seq, region_list_target


def save_report_locally(seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                        original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list,
                        min_cost):
    report_path = Report(seq,
                         target_seq,
                         marked_input_seq,
                         marked_target_seq,
                         unwanted_patterns,
                         original_coding_regions,
                         original_region_list,
                         selected_regions_to_exclude,
                         selected_region_list,
                         min_cost).create_report()

    return report_path

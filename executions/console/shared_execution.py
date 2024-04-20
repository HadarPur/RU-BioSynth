from utils.dna_utils import DNAHighlighter
from utils.display_utils import SequenceUtils
from utils.input_utils import UserInputHandler
from utils.cost_utils import CodonScorer
from report.pdf_report_utils import Report
from algorithm.eliminate_sequence import EliminateSequence
import copy


class Shared:

    def __init__(self, seq, unwanted_patterns):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns

    def run(self):
        if self.seq is None or len(self.seq) == 0:
            print("The input sequence is empty, please try again")
            return

        # Print the original DNA sequence
        print(SequenceUtils.get_sequence("DNA sequence", self.seq))

        # Print the list of unwanted patterns
        print(SequenceUtils.get_patterns(self.unwanted_patterns))

        # Extract coding regions from the sequence
        region_list = DNAHighlighter.get_coding_and_non_coding_regions(self.seq)

        # Extract coding regions and their indexes from the highlighted sequence
        coding_regions, coding_indexes = DNAHighlighter.extract_coding_regions_with_indexes(region_list)

        # Highlight coding regions and print the sequence
        highlighted_sequence = DNAHighlighter.highlight_coding_regions(self.seq, coding_regions)
        print(SequenceUtils.get_highlighted_sequence(highlighted_sequence))

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(coding_regions)}")

        # Handle elimination of coding regions if the user chooses to
        if len(coding_regions) > 0:
            original_coding_regions, selected_regions_to_exclude, selected_region_list = self.handle_coding_region_elimination(region_list,
                                                                                                                               coding_indexes,
                                                                                                                               coding_regions)
        else:
            print("Continue without coding regions...")
            selected_region_list = region_list
            original_coding_regions = UserInputHandler.get_coding_regions_list(coding_regions)
            selected_regions_to_exclude = None

        # Calculate scores for the regions using the CodonScorer
        scorer = CodonScorer()
        cost_table = scorer.calculate_scores(selected_region_list)

        # Eliminate unwanted patterns and generate the resulting sequence
        target_seq, min_cost = self.eliminate_unwanted_patterns(cost_table)

        # Mark non-equal codons and print the target sequence
        region_list_target = DNAHighlighter.get_coding_and_non_coding_regions(target_seq)
        marked_input_seq, marked_target_seq = self.mark_and_print_non_equal_codons(selected_region_list,
                                                                                   region_list_target)
        SequenceUtils.get_sequence("Target DNA sequence",
                                   target_seq)

        # Create a report summarizing the processing and save if the user chooses to
        Report(self.seq,
               target_seq,
               marked_input_seq,
               marked_target_seq,
               self.unwanted_patterns,
               original_coding_regions,
               selected_regions_to_exclude,
               region_list,
               selected_region_list,
               min_cost).create_report()

    @staticmethod
    def handle_coding_region_elimination(region_list, coding_indexes, coding_regions):
        selected_region_list = copy.deepcopy(region_list)

        # Ask the user if they want to eliminate coding regions
        elimination_response = UserInputHandler.handle_elimination_input()
        if elimination_response is False:
            # If the response is negative, ask for coding regions to eliminate
            original_coding_regions, selected_regions_to_exclude, coding_regions_to_exclude = UserInputHandler.handle_elimination_coding_regions_input(coding_regions)
            # Update the coding regions based on user input
            selected_region_list = DNAHighlighter.update_coding_regions(selected_region_list, coding_indexes, coding_regions_to_exclude)

        else:
            original_coding_regions = UserInputHandler.get_coding_regions_list(coding_regions)
            selected_regions_to_exclude = None

        return original_coding_regions, selected_regions_to_exclude, selected_region_list

    def eliminate_unwanted_patterns(self, cost_table):
        target_seq, min_cost = EliminateSequence.eliminate(self.seq,
                                                           self.unwanted_patterns,
                                                           cost_table)
        return target_seq, min_cost

    @staticmethod
    def mark_and_print_non_equal_codons(region_list, region_list_target):
        # Mark non-equal codons between the original and target sequences
        marked_input_seq, marked_target_seq = SequenceUtils.mark_non_equal_codons(region_list,
                                                                                  region_list_target)
        return marked_input_seq, marked_target_seq

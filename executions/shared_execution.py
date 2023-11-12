from utils.dna_utils import DNAHighlighter
from utils.display_utils import DNASequencePrinter
from utils.input_utils import UserInputHandler
from utils.cost_utils import CodonScorer
from report.pdf_report_utils import Report
from algorithm.eliminate_sequence import EliminateSequence


class Shared:
    def __init__(self, seq, unwanted_patterns):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns

    def run(self):
        # Print the original DNA sequence
        self.print_original_sequence()

        # Print the list of unwanted patterns
        self.print_unwanted_patterns()

        # Initialize DNAHighlighter to process DNA sequences
        dna_highlighter = DNAHighlighter()

        # Extract coding regions from the sequence
        region_list = self.extract_coding_regions(dna_highlighter)

        # Extract coding regions and their indexes from the highlighted sequence
        coding_regions, coding_indexes = dna_highlighter.extract_coding_regions_with_indexes(region_list)

        # Highlight coding regions and print the sequence
        highlighted_sequence = self.highlight_coding_regions(dna_highlighter, coding_regions)

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(coding_regions)}")

        # Handle elimination of coding regions if the user chooses to
        if len(coding_regions) > 0:
            self.handle_coding_region_elimination(dna_highlighter, region_list, coding_indexes, coding_regions)
        else:
            print("Continue without coding regions")

        # Calculate scores for the regions using the CodonScorer
        scorer = CodonScorer()
        cost_table = scorer.calculate_scores(region_list)

        # Eliminate unwanted patterns and generate the resulting sequence
        target_seq = self.eliminate_unwanted_patterns(cost_table)

        # Mark non-equal codons and print the target sequence
        region_list_target = dna_highlighter.get_coding_and_non_coding_regions(target_seq)
        marked_input_seq, marked_target_seq = self.mark_and_print_non_equal_codons(region_list, region_list_target)
        DNASequencePrinter.print_sequence("Target DNA sequence", target_seq)

        # Create a report summarizing the processing and save if the user chooses to
        self.create_report_and_save(target_seq, marked_input_seq, marked_target_seq, highlighted_sequence)

    def print_original_sequence(self):
        # Print the original DNA sequence
        DNASequencePrinter.print_sequence("DNA sequence", self.seq)

    def print_unwanted_patterns(self):
        # Print the list of unwanted patterns
        DNASequencePrinter.print_patterns(self.unwanted_patterns)

    def extract_coding_regions(self, dna_highlighter):
        # Extract coding and non-coding regions from the DNA sequence
        region_list = dna_highlighter.get_coding_and_non_coding_regions(self.seq)
        return region_list

    def highlight_coding_regions(self, dna_highlighter, coding_regions):
        # Highlight coding regions in the sequence
        highlighted_sequence = dna_highlighter.highlight_coding_regions(self.seq, coding_regions)
        highlighted_sequence_str = DNASequencePrinter.print_highlighted_sequence(highlighted_sequence)
        return highlighted_sequence_str

    def handle_coding_region_elimination(self, dna_highlighter, region_list, coding_indexes, coding_regions):
        # Ask the user if they want to eliminate coding regions
        elimination_response = UserInputHandler.handle_elimination_input_response()

        if elimination_response is False:
            # If the response is negative, ask for coding regions to eliminate
            coding_regions_to_exclude = UserInputHandler.handle_elimination_coding_regions_input(coding_regions)
            # Update the coding regions based on user input
            region_list = dna_highlighter.update_coding_regions(region_list, coding_indexes, coding_regions_to_exclude)

    def eliminate_unwanted_patterns(self, cost_table):
        # Eliminate unwanted patterns based on the calculated cost table
        target_seq = EliminateSequence.eliminate(self.seq, self.unwanted_patterns, cost_table)
        return target_seq

    def mark_and_print_non_equal_codons(self, region_list, region_list_target):
        # Mark non-equal codons between the original and target sequences
        marked_input_seq, marked_target_seq = DNASequencePrinter.mark_non_equal_codons(region_list, region_list_target)
        return marked_input_seq, marked_target_seq

    def create_report_and_save(self, target_seq, marked_input_seq, marked_target_seq, highlighted_sequence):
        # Create a report summarizing the processing and save if the user chooses to
        Report(self.seq, target_seq, marked_input_seq, marked_target_seq, self.unwanted_patterns, highlighted_sequence).create_report()
        # Uncomment the following lines if you want to implement the save functionality
        # saving_response = UserInputHandler.handle_saving_input_response()
        # if saving_response:
        #     UserInputHandler.save_sequence_to_file(target_seq)

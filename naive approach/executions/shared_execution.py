from utils.input_utils import *
from utils.dna_utils import *
from utils.display_utils import *
from algorithms.eliminate_sequence import *


class Shared:
    def __init__(self, seq, unwanted_patterns, cost_table):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns
        self.cost_table = cost_table

    def run(self):
        """
        This method runs a sequence processing workflow.
        It prints the coding regions and their translations,
        eliminates coding regions if requested, and displays the
        resulting sequence.
        """

        # Print the original sequence
        DNASequencePrinter.print_sequence(self.seq)
        # Print the unwanted patterns list
        DNASequencePrinter.print_patterns(self.unwanted_patterns)

        # Extract coding regions from the sequence
        coding_regions = get_coding_region(self.seq)

        # Highlight coding regions and print the sequence
        highlighted_sequence = highlight_coding_regions(self.seq, coding_regions)
        DNASequencePrinter.print_highlighted_sequence(highlighted_sequence)

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(coding_regions)}")

        if len(coding_regions) > 0:
            # Ask the user if they want to eliminate coding regions
            elimination_response = handle_elimination_input_response()

            if elimination_response is False:
                # If the response is negative, ask for coding regions to eliminate
                coding_regions = handle_elimination_coding_regions_input(coding_regions)

        # Eliminate coding regions and get the resulting sequence
        target_seq = EliminateSequence.eliminate(self.seq, self.unwanted_patterns, self.cost_table)

        if target_seq is not None:
            # If a target sequence is obtained, print it
            DNASequencePrinter.print_target_sequence(target_seq)

        # Return control back, indicating the end of the method
        return

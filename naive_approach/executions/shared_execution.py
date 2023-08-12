from naive_approach.utils.dna_utils import *
from naive_approach.algorithms.eliminate_sequence import EliminateSequence
from naive_approach.utils.display_utils import DNASequencePrinter
from naive_approach.utils.input_utils import UserInputHandler


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

        dna_highlighter = DNAHighlighter(self.seq)

        # Extract coding regions from the sequence
        coding_regions = dna_highlighter.get_coding_regions()

        # Highlight coding regions and print the sequence
        highlighted_sequence = dna_highlighter.highlight_coding_regions(coding_regions)
        DNASequencePrinter.print_highlighted_sequence(highlighted_sequence)

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(coding_regions)}")

        if len(coding_regions) > 0:
            # Ask the user if they want to eliminate coding regions
            elimination_response = UserInputHandler.handle_elimination_input_response()

            if elimination_response is False:
                # If the response is negative, ask for coding regions to eliminate
                coding_regions = UserInputHandler.handle_elimination_coding_regions_input(coding_regions)

        # Eliminate coding regions and get the resulting sequence
        EliminateSequence.eliminate(self.seq, self.unwanted_patterns, self.cost_table)

        # Return control back, indicating the end of the method
        return

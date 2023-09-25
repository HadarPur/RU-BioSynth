from utils.dna_utils import DNAHighlighter
from utils.display_utils import DNASequencePrinter
from utils.input_utils import UserInputHandler
from utils.cost_utils import CodonScorer
from algorithm.eliminate_sequence import EliminateSequence


class Shared:
    def __init__(self, seq, unwanted_patterns):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns

    def run(self):
        """
        This method runs a sequence processing workflow.
        It prints the coding regions and their translations,
        eliminates coding regions if requested, and displays the
        resulting sequence.
        """

        # Print the original sequence
        DNASequencePrinter.print_sequence("DNA sequence", self.seq)

        # Print the unwanted patterns list
        DNASequencePrinter.print_patterns(self.unwanted_patterns)

        # Print the cost table list
        # DNASequencePrinter.print_cost_table(self.seq, self.cost_table)

        dna_highlighter = DNAHighlighter()

        # Extract coding regions from the sequence
        region_list = dna_highlighter.get_coding_and_non_coding_regions(self.seq)
        coding_regions, coding_indexes = dna_highlighter.extract_coding_regions_with_indexes(region_list)

        # Highlight coding regions and print the sequence
        highlighted_sequence = dna_highlighter.highlight_coding_regions(self.seq, coding_regions)
        DNASequencePrinter.print_highlighted_sequence(highlighted_sequence)

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(coding_regions)}")

        if len(coding_regions) > 0:
            # Ask the user if they want to eliminate coding regions
            elimination_response = UserInputHandler.handle_elimination_input_response()

            if elimination_response is False:
                # If the response is negative, ask for coding regions to eliminate
                coding_regions_to_exclude = UserInputHandler.handle_elimination_coding_regions_input(coding_regions)
                region_list = dna_highlighter.update_coding_regions(region_list, coding_indexes, coding_regions_to_exclude)

        else:
            print("Continue without coding regions")

        # Update the cost table based on coding region scores
        # Create an instance of the CodonScorer class to calculate scores for a list of regions
        scorer = CodonScorer()
        cost_table = scorer.calculate_scores(region_list)

        # Eliminate coding regions and generate the resulting sequence
        # Use the EliminateSequence class to eliminate unwanted patterns in the sequence
        # based on the calculated cost table
        target_seq = EliminateSequence.eliminate(self.seq, self.unwanted_patterns, cost_table)

        # Mark non-equal codons and print the target sequence
        # Use the DNASequencePrinter class to mark and print the unequal codons between
        # the original sequence and the target sequence
        target_seq_region_list = dna_highlighter.get_coding_and_non_coding_regions(target_seq)

        DNASequencePrinter.mark_non_equal_codons(region_list, target_seq_region_list)
        DNASequencePrinter.print_sequence("DNA target sequence", target_seq)

        # Prompt the user if they want to save the resulting sequence to a file
        # Use the UserInputHandler class to handle user input for saving the sequence
        # If the user chooses to save, handle the saving process
        saving_response = UserInputHandler.handle_saving_input_response()
        if saving_response:
            UserInputHandler.save_sequence_to_file(target_seq)

        # Return control, indicating the end of the method
        return


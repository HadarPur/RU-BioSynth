import copy

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, initialize_report
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAHighlighter
from utils.input_utils import UserInputHandler


def save_report_if_requested(seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                             original_coding_regions, selected_regions_to_exclude, region_list, selected_region_list,
                             min_cost):
    report = initialize_report(seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                               original_coding_regions, selected_regions_to_exclude, region_list,
                               selected_region_list,
                               min_cost)
    report.create_report()

    save_report = input(
        "\n\nElimination report is now available, do you want to download the report? (yes/no): ").lower()

    if save_report == 'yes' or save_report == 'y':
        report_path = report.save_report()
        print(report_path)
        print("Report saved successfully!")
    elif save_report == 'no' or save_report == 'n':
        print("Report not saved.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")


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
        print(f"\nPattern list:\n\t{SequenceUtils.get_patterns(self.unwanted_patterns)}\n")

        # Extract coding regions from the sequence
        original_region_list = DNAHighlighter.get_coding_and_non_coding_regions(self.seq)

        # Extract coding regions and their indexes from the highlighted sequence
        original_coding_regions, coding_indexes = DNAHighlighter.extract_coding_regions_with_indexes(
            original_region_list)

        # Highlight coding regions and print the sequence
        highlighted_sequence = ''.join(SequenceUtils.highlight_sequences_to_terminal(original_region_list))
        print(
            f'\nIdentify the coding regions within the given DNA sequence and mark them for emphasis:\n\t {highlighted_sequence}')

        # Print the number of coding regions found
        print(f"\nNumber of coding regions is: {len(original_coding_regions)}")

        # Handle elimination of coding regions if the user chooses to
        if len(original_coding_regions) > 0:
            original_coding_regions, selected_regions_to_exclude, selected_region_list = self.handle_coding_region_elimination(
                original_region_list,
                coding_indexes,
                original_coding_regions)
        else:
            print("Continue without coding regions...")
            selected_region_list = original_region_list
            original_coding_regions = UserInputHandler.get_coding_regions_list(original_coding_regions)
            selected_regions_to_exclude = None

        # Eliminate unwanted patterns and generate the resulting sequence
        info, target_seq, min_cost = eliminate_unwanted_patterns(self.seq, self.unwanted_patterns, selected_region_list)

        print('\n' + '=' * 50 + '\n' + '=' * 50 + '\n')
        print(info)
        print('\n' + '=' * 50 + '\n' + '=' * 50 + '\n')

        # Mark non-equal codons and print the target sequence
        marked_input_seq, marked_target_seq, marked_seq, region_list_target = mark_non_equal_codons(
            selected_region_list,
            target_seq)

        print(marked_seq)
        target_result = SequenceUtils.get_sequence("Target DNA sequence", target_seq)
        print(target_result)

        # Create a report summarizing the processing and save if the user chooses to
        save_report_if_requested(self.seq,
                                 target_seq,
                                 marked_input_seq,
                                 marked_target_seq,
                                 self.unwanted_patterns,
                                 original_coding_regions,
                                 original_region_list,
                                 selected_regions_to_exclude,
                                 selected_region_list,
                                 min_cost)

    def handle_coding_region_elimination(self, region_list, coding_indexes, coding_regions):
        selected_region_list = copy.deepcopy(region_list)

        # Ask the user if they want to eliminate coding regions
        elimination_response = UserInputHandler.handle_elimination_input()
        if elimination_response is False:
            # If the response is negative, ask for coding regions to eliminate
            original_coding_regions, selected_regions_to_exclude, coding_regions_to_exclude = UserInputHandler.handle_elimination_coding_regions_input(
                coding_regions)
            # Update the coding regions based on user input
            selected_region_list = DNAHighlighter.update_coding_regions(selected_region_list, coding_indexes,
                                                                        coding_regions_to_exclude)

            highlighted_sequence = ''.join(SequenceUtils.highlight_sequences_to_terminal(selected_region_list))
            print(f'\nThe full sequence after selection is:\n\t {highlighted_sequence}')

        else:
            original_coding_regions = UserInputHandler.get_coding_regions_list(coding_regions)
            selected_regions_to_exclude = None

        return original_coding_regions, selected_regions_to_exclude, selected_region_list

from datetime import datetime

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, initialize_report
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAHighlighter
from utils.file_utils import save_file
from utils.input_utils import UserInputHandler
from utils.text_utils import format_text_bold_for_output


class Shared:

    def __init__(self, seq, unwanted_patterns, output_path=None):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns
        self.output_path = output_path

    def run(self):
        if self.seq is None or len(self.seq) == 0:
            print("The input sequence is empty, please try again")
            return

        # Print the original DNA sequence
        print(SequenceUtils.get_sequence(format_text_bold_for_output("DNA sequence"), self.seq))

        # Print the list of unwanted patterns
        print(
            f"\n{format_text_bold_for_output('Pattern list:')}\n\t{SequenceUtils.get_patterns(self.unwanted_patterns)}\n")

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
        original_coding_regions = UserInputHandler.get_coding_regions_list(original_coding_regions)

        # Eliminate unwanted patterns and generate the resulting sequence
        info, target_seq, min_cost = eliminate_unwanted_patterns(self.seq, self.unwanted_patterns, original_region_list)

        print(format_text_bold_for_output('\n' + '_' * 100 + '\n' + '_' * 100 + '\n'))
        print(info)

        # Mark non-equal codons and print the target sequence
        marked_input_seq, marked_target_seq, marked_seq = mark_non_equal_codons(self.seq,
                                                                                target_seq,
                                                                                original_region_list)

        # print(marked_seq)
        target_result = SequenceUtils.get_sequence(format_text_bold_for_output('Target DNA sequence'), target_seq)
        print(f'{target_result}\n')

        # Create a report summarizing the processing and save if the user chooses to
        file_date = datetime.today().strftime("%d %b %Y, %H:%M:%S")
        self.save_report(target_seq,
                         marked_input_seq,
                         marked_target_seq,
                         original_coding_regions,
                         original_region_list,
                         min_cost, file_date)

        self.save_target_sequence(target_seq, file_date)

    def save_report(self, target_seq, marked_input_seq, marked_target_seq,
                    original_coding_regions, region_list, min_cost, file_date):

        report = initialize_report(self.seq, target_seq, marked_input_seq, marked_target_seq,
                                   self.unwanted_patterns, original_coding_regions, region_list,
                                   None, None, min_cost)

        report.create_report(file_date)

        path = report.download_report(self.output_path)
        print(path)

    def save_target_sequence(self, target_seq, file_date):
        filename = f'Target DNA sequence - {file_date}.txt'
        path = save_file(target_seq, self.output_path, filename)
        print(path)




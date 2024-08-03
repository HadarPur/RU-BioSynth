from datetime import datetime

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, initialize_report
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAUtils
from utils.file_utils import save_file
from utils.output_utils import Logger
from utils.text_utils import format_text_bold_for_output

app_icon_text = """\
================================================================
================================================================

             ____  _       ____  _ _         
            | __ )(_) ___ | __ )| (_)___ ___ 
            |  _ \| |/ _ \|  _ \| | / __/ __|
            | |_) | | (_) | |_) | | \__ \__ \ 
            |____/|_|\___/|____/|_|_|___/___/
                                
                                
================================================================
================================================================                                                          
"""


class CommandController:

    def __init__(self, seq, unwanted_patterns, output_path=None):
        self.seq = seq
        self.unwanted_patterns = unwanted_patterns
        self.output_path = output_path

    def run(self):
        if self.seq is None or len(self.seq) == 0:
            Logger.error("The input sequence is empty, please try again")
            return

        has_overlaps, overlaps = DNAUtils.find_overlapping_regions(self.seq)

        if has_overlaps:
            Logger.error(f"{format_text_bold_for_output('Error Occurred:')}")
            Logger.error("The input sequence contains overlapping coding regions.")
            Logger.space()
            Logger.info(DNAUtils.get_overlapping_regions(self.seq, overlaps))
            Logger.error("Please make sure that the input seq will not contains any overlapping regions.")
            return

        Logger.notice(app_icon_text)

        # Print the original DNA sequence
        Logger.debug(f"{format_text_bold_for_output('DNA sequence:')}")
        Logger.info(f"{self.seq}")
        Logger.space()

        # Print the list of unwanted patterns
        Logger.debug(f"{format_text_bold_for_output('Pattern list:')}")
        Logger.info(f"{SequenceUtils.get_patterns(self.unwanted_patterns)}")
        Logger.space()

        # Extract coding regions from the sequence
        original_region_list = DNAUtils.get_coding_and_non_coding_regions(self.seq)

        # Extract coding regions and their indexes from the highlighted sequence
        original_coding_regions, coding_indexes = DNAUtils.extract_coding_regions_with_indexes(
            original_region_list)

        # Highlight coding regions and print the sequence
        highlighted_sequence = ''.join(SequenceUtils.highlight_sequences_to_terminal(original_region_list))
        Logger.debug(f'Identify the coding regions within the given DNA sequence and mark them for emphasis:')
        Logger.info(f"{highlighted_sequence}")
        Logger.space()

        # Handle elimination of coding regions if the user chooses to
        original_coding_regions = DNAUtils.get_coding_regions_list(original_coding_regions)
        Logger.debug(f"The total number of coding regions is {len(original_coding_regions)}, identifies as follows:")
        Logger.info('\n'.join(f"[{key}] {value}" for key, value in original_coding_regions.items()))

        # Eliminate unwanted patterns and generate the resulting sequence
        info, detailed_changes, target_seq, min_cost = eliminate_unwanted_patterns(self.seq,
                                                                                   self.unwanted_patterns,
                                                                                   original_region_list)

        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n' + '_' * 100 + '\n'))
        Logger.info(info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n' + '_' * 100 + '\n'))

        # Mark non-equal codons and print the target sequence
        index_seq_str, marked_input_seq, marked_target_seq = mark_non_equal_codons(self.seq,
                                                                                   target_seq,
                                                                                   original_region_list)

        Logger.debug(format_text_bold_for_output('Target DNA Sequence'))
        Logger.info(f"{target_seq}")
        Logger.space()

        changes = '\n'.join(detailed_changes) if detailed_changes else None
        Logger.debug(format_text_bold_for_output('Detailed Changes:'))
        Logger.info(f"{changes}")
        Logger.space()

        # Create a report summarizing the processing and save if the user chooses to
        file_date = datetime.today().strftime("%d %b %Y, %H:%M:%S")
        self.save_report(target_seq,
                         index_seq_str,
                         marked_input_seq,
                         marked_target_seq,
                         original_coding_regions,
                         original_region_list,
                         min_cost,
                         detailed_changes,
                         file_date)

        self.save_target_sequence(target_seq, file_date)

    def save_report(self,
                    target_seq,
                    index_seq_str,
                    marked_input_seq,
                    marked_target_seq,
                    original_coding_regions,
                    region_list,
                    min_cost,
                    detailed_changes,
                    file_date):
        report = initialize_report(self.seq,
                                   target_seq,
                                   index_seq_str,
                                   marked_input_seq,
                                   marked_target_seq,
                                   self.unwanted_patterns,
                                   original_coding_regions,
                                   region_list,
                                   None,
                                   None,
                                   min_cost,
                                   detailed_changes)

        report.create_report(file_date)

        path = report.download_report(self.output_path)
        Logger.notice(path)

    def save_target_sequence(self, target_seq, file_date):
        filename = f'Target DNA Sequence - {file_date}.txt'
        path = save_file(target_seq, filename, self.output_path)
        Logger.notice(path)

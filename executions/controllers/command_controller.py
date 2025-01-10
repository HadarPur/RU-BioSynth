from datetime import datetime

from executions.execution_utils import eliminate_unwanted_patterns, mark_non_equal_codons, initialize_report
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAUtils
from utils.file_utils import save_file
from utils.output_utils import Logger
from utils.text_utils import format_text_bold_for_output
from executions.controllers.app_data import AppData

app_icon_text = """\
=================================================================
=================================================================

             ____  _       ____  _ _         
            | __ )(_) ___ | __ )| (_)___ ___ 
            |  _ \\| |/ _ \\|  _ \\| | / __/ __|
            | |_) | | (_) | |_) | | \\__ \\__ \\ 
            |____/|_|\\___/|____/|_|_|___/___/

=================================================================
=================================================================                                                          
"""


class CommandController:
    def __init__(self, output_path=None):
        self.output_path = output_path or AppData.download_location

    def run(self):
        if not AppData.dna_sequence:
            Logger.error("The input sequence is empty, please try again")
            return

        has_overlaps, overlaps = DNAUtils.find_overlapping_regions(AppData.dna_sequence)

        if has_overlaps:
            Logger.error(f"{format_text_bold_for_output('Error Occurred:')}")
            Logger.error("The input sequence contains overlapping coding regions.")
            Logger.space()
            Logger.info(DNAUtils.get_overlapping_regions(AppData.dna_sequence, overlaps))
            Logger.error("Please ensure the input sequence does not contain overlapping regions.")
            return

        Logger.notice(app_icon_text)

        # Print the target sequence
        Logger.debug(f"{format_text_bold_for_output('Target sequence:')}")
        Logger.info(f"{AppData.dna_sequence}")
        Logger.space()

        # Print the list of unwanted patterns
        Logger.debug(f"{format_text_bold_for_output('Pattern list:')}")
        Logger.info(f"{SequenceUtils.get_patterns(AppData.patterns)}")
        Logger.space()

        # Extract coding regions
        original_region_list = DNAUtils.get_coding_and_non_coding_regions(AppData.dna_sequence)
        original_coding_regions, coding_indexes = DNAUtils.extract_coding_regions_with_indexes(original_region_list)
        highlighted_sequence = ''.join(SequenceUtils.highlight_sequences_to_terminal(original_region_list))

        Logger.debug('Identify the coding regions within the given target sequence and mark them for emphasis:')
        Logger.info(highlighted_sequence)
        Logger.space()

        # Handle elimination of coding regions if the user chooses to
        original_coding_regions = DNAUtils.get_coding_regions_list(original_coding_regions)
        Logger.debug(f"The total number of coding regions is {len(original_coding_regions)}, identifies as follows:")
        Logger.info('\n'.join(f"[{key}] {value}" for key, value in original_coding_regions.items()))

        # Eliminate unwanted patterns
        eliminate_unwanted_patterns(AppData.dna_sequence, AppData.patterns, original_region_list)

        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n'))
        Logger.info(AppData.info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n'))

        # Mark non-equal codons
        index_seq_str, marked_input_seq, marked_optimized_seq = mark_non_equal_codons(
            AppData.dna_sequence, AppData.optimized_seq, original_region_list
        )

        Logger.debug(format_text_bold_for_output('Optimized Sequence'))
        Logger.info(AppData.optimized_seq)
        Logger.space()

        changes = '\n'.join(AppData.detailed_changes) if AppData.detailed_changes else None
        Logger.debug(format_text_bold_for_output('Detailed Changes:'))
        Logger.info(f"{changes}")
        Logger.space()

        file_date = datetime.today().strftime("%d%b%Y,%H:%M:%S")

        # Save the results
        report = initialize_report(
            AppData.dna_sequence, AppData.optimized_seq, index_seq_str, marked_input_seq,
            marked_optimized_seq, AppData.patterns, original_coding_regions, original_region_list,
            None, None, AppData.min_cost, AppData.detailed_changes
        )

        report.create_report(file_date)
        path = report.download_report(self.output_path)
        Logger.notice(path)

        filename = f"Optimized Sequence - {file_date}.txt"
        path = save_file(AppData.optimized_seq, filename, self.output_path)
        Logger.notice(path)
        Logger.space()


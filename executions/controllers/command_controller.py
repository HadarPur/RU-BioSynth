from datetime import datetime

from data.app_data import InputData, EliminationData, OutputData
from executions.execution_utils import eliminate_unwanted_patterns
from report.html_report_utils import ReportController
from utils.display_utils import SequenceUtils
from utils.dna_utils import DNAUtils
from utils.file_utils import save_file
from utils.output_utils import Logger
from utils.text_utils import format_text_bold_for_output

app_icon_text = """\
=================================================================
=================================================================
         ______  _       ______                  _     
        (____  \(_)     / _____)             _  | |    
         ____)  )_  ___( (____  _   _ ____ _| |_| |__  
        |  __  (| |/ _ \\____ \| | | |  _ (_   _)  _ \ 
        | |__)  ) | |_| |____) ) |_| | | | || |_| | | |
        |______/|_|\___(______/ \__  |_| |_| \__)_| |_|
                               (____/                                                                                          
=================================================================
=================================================================                                                          
"""



class CommandController:

    def run(self):
        if not InputData.dna_sequence:
            Logger.error("The input sequence is empty, please try again")
            return

        has_overlaps, overlaps = DNAUtils.find_overlapping_regions(InputData.dna_sequence)

        if has_overlaps:
            Logger.error(f"{format_text_bold_for_output('Error Occurred:')}")
            Logger.error("The input sequence contains overlapping coding regions.")
            Logger.space()
            Logger.info(DNAUtils.get_overlapping_regions(InputData.dna_sequence, overlaps))
            Logger.error("Please ensure the input sequence does not contain overlapping regions.")
            return

        Logger.notice(app_icon_text)

        # Print the target sequence
        Logger.debug(f"{format_text_bold_for_output('Target sequence:')}")
        Logger.info(f"{InputData.dna_sequence}")
        Logger.space()

        # Print the list of unwanted patterns
        Logger.debug(f"{format_text_bold_for_output('Pattern list:')}")
        Logger.info(f"{SequenceUtils.get_patterns(InputData.unwanted_patterns)}")
        Logger.space()

        # Extract coding regions
        InputData.coding_positions, InputData.coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(InputData.dna_sequence)
        highlighted_sequence = ''.join(SequenceUtils.highlight_sequences_to_terminal(InputData.dna_sequence, InputData.coding_indexes))

        Logger.debug('Identify the coding regions within the given target sequence and mark them for emphasis:')
        Logger.info(highlighted_sequence)
        Logger.space()

        # Handle elimination of coding regions if the user chooses to
        InputData.coding_regions_list = DNAUtils.get_coding_regions_list(InputData.coding_indexes, InputData.dna_sequence)
        if len(InputData.coding_indexes) > 0:
            Logger.debug(
                f"The total number of coding regions is {len(InputData.coding_indexes)}, identifies as follows:")
            Logger.info('\n'.join(f"[{key}] {value}" for key, value in InputData.coding_regions_list.items()))
        else:
            Logger.debug("No coding region was identified in the provided target sequence")

        # Eliminate unwanted patterns
        eliminate_unwanted_patterns(InputData.dna_sequence, InputData.unwanted_patterns, InputData.coding_positions)

        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n'))
        Logger.info(EliminationData.info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 100 + '\n'))

        Logger.debug(format_text_bold_for_output('Optimized Sequence'))
        Logger.info(OutputData.optimized_sequence)
        Logger.space()

        changes = '\n'.join(EliminationData.detailed_changes) if EliminationData.detailed_changes else None
        Logger.debug(format_text_bold_for_output('Detailed Changes:'))
        Logger.info(f"{changes}")
        Logger.space()

        file_date = datetime.today().strftime("%d%b%Y,%H:%M:%S")

        # Save the results
        report = ReportController(InputData.coding_positions)

        report.create_report(file_date)
        path = report.download_report(OutputData.output_path)
        Logger.notice(path)

        filename = f"Optimized Sequence - {file_date}.txt"
        path = save_file(OutputData.optimized_sequence, filename, OutputData.output_path)
        Logger.notice(path)
        Logger.space()


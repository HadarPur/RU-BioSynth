from datetime import datetime

from biosynth.data.app_data import InputData, EliminationData, OutputData
from biosynth.executions.execution_utils import eliminate_unwanted_patterns
from biosynth.report.html_report_utils import ReportController
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils
from biosynth.utils.file_utils import save_file
from biosynth.utils.output_utils import Logger
from biosynth.utils.text_utils import format_text_bold_for_output

app_icon_text = """
=================================================================
=================================================================

██████╗ ██╗ ██████╗ ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
██╔══██╗██║██╔═══██╗██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║
██████╔╝██║██║   ██║███████╗ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║
██╔══██╗██║██║   ██║╚════██║  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║
██████╔╝██║╚██████╔╝███████║   ██║   ██║ ╚████║   ██║   ██║  ██║
╚═════╝ ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝                                                                                                  
                                                                                                
=================================================================
=================================================================
\n
"""


class CommandController:

    def run(self):
        Logger.notice(app_icon_text)

        if not InputData.dna_sequence:
            Logger.error("The input sequence is empty, please try again")
            sys.exit(3)

        try:
            # Check for start codon
            InputData.start_codon_identified, InputData.cleaned_dna_sequence = DNAUtils.find_start_codon(InputData.dna_sequence)
        except ValueError as e:
            Logger.error(f"Start codon validation failed: {e}")
            InputData.reset()
            sys.exit(3)

        # Extract coding regions
        InputData.coding_positions, InputData.coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(
            InputData.cleaned_dna_sequence, InputData.start_codon_identified)

        Logger.debug(f"{format_text_bold_for_output('Target sequence:')}")

        if InputData.coding_indexes is not None:
            Logger.notice(f'A coding region was identified in the target sequence at positions {InputData.coding_indexes[0] + 1} - {InputData.coding_indexes[1]}:')
            Logger.info(f"{SequenceUtils.highlight_sequence_to_terminal(InputData.cleaned_dna_sequence, InputData.coding_indexes)}")
        else:
            Logger.info(f"{InputData.cleaned_dna_sequence}")

        Logger.space()

        # Print the list of unwanted patterns
        Logger.debug(f"{format_text_bold_for_output('Unwanted patterns:')}")
        Logger.info(f"{SequenceUtils.get_patterns(InputData.unwanted_patterns)}")
        Logger.space()

        # Eliminate unwanted patterns
        eliminate_unwanted_patterns(InputData.cleaned_dna_sequence, InputData.unwanted_patterns, InputData.coding_positions)

        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))
        Logger.info(EliminationData.info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))

        Logger.debug(format_text_bold_for_output('Optimized Sequence:'))
        Logger.info(OutputData.optimized_sequence)
        Logger.space()

        changes = '\n'.join(EliminationData.detailed_changes) if EliminationData.detailed_changes else None
        Logger.debug(format_text_bold_for_output('Detailed substitutions relative to the target sequence:'))
        Logger.info(f"{changes}")
        Logger.space()

        # Save the results
        report = ReportController()

        Logger.critical("The final report and optimized sequence can be found in the following paths:\n")
        file_date = datetime.today().strftime("%d-%b-%Y_%H-%M-%S")
        report.create_report(file_date)
        path = report.download_report(OutputData.output_path)
        Logger.notice(path)

        filename = f"Optimized-Sequence_{file_date}.txt"
        path = save_file(OutputData.optimized_sequence, filename, OutputData.output_path)
        Logger.notice(path)

        filename = f"Changes-Info_{file_date}.txt"
        detailed_changes = '\n'.join(EliminationData.detailed_changes) if EliminationData.detailed_changes else None
        path = save_file(detailed_changes, filename, OutputData.output_path)
        Logger.notice(path)
        Logger.space()
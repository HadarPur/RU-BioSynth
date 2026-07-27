import sys
from datetime import datetime
from tabulate import tabulate

from biosynth.data.app_data import InputData, EliminationData, OutputData, CostData
from biosynth.executions.controllers.ui.theme import HEADINGS
from biosynth.executions.execution_utils import eliminate_unwanted_patterns
from biosynth.report.report_builder import ReportBuilder
from biosynth.utils.display_utils import SequenceUtils
from biosynth.utils.coding_region import CodingRegionLocator
from biosynth.utils.file_utils import save_file
from biosynth.utils.logger import Logger
from biosynth.utils.spinner import run_with_spinner
from biosynth.utils.text_utils import format_text_bold_for_output
from biosynth.utils.cai_utils import calculate_cai

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
    """Orchestrates the core elimination workflow shared by the CLI and debug entry points."""

    def run(self):
        """Execute the full elimination pipeline against the populated app data.

        Validates the input sequence, detects the start codon and coding
        regions, logs the target sequence and unwanted-pattern occurrences,
        runs the elimination algorithm with a progress spinner, prints
        detailed cost contributions and substitutions, then writes the HTML
        report and the optimized-sequence/cost text files to the configured
        output path. Exits with code 3 if the input sequence is missing or
        start-codon validation fails.
        """
        Logger.notice(app_icon_text)

        if not InputData.dna_sequence:
            Logger.error("The input sequence is empty, please try again")
            sys.exit(3)

        try:
            # Check for start codon
            InputData.start_codon_identified, InputData.cleaned_dna_sequence = CodingRegionLocator.find_start_codon(InputData.dna_sequence)
        except ValueError as e:
            Logger.error(f"Start codon validation failed: {e}")
            InputData.reset()
            sys.exit(3)

        # Extract coding regions
        InputData.coding_positions, InputData.coding_indexes = CodingRegionLocator.get_coding_and_non_coding_regions_positions(
            InputData.cleaned_dna_sequence, InputData.start_codon_identified)

        Logger.debug(f"{format_text_bold_for_output(HEADINGS.target_sequence + ':')}")

        if InputData.coding_indexes is not None:
            Logger.info(
                HEADINGS.coding_region_identified.format(
                    start=InputData.coding_indexes[0] + 1,
                    end=InputData.coding_indexes[1],
                ) + ":"
            )
            Logger.info(f"{SequenceUtils.highlight_sequence_to_terminal(InputData.cleaned_dna_sequence, InputData.coding_indexes)}")
        else:
            Logger.info(f"{InputData.cleaned_dna_sequence}")

        Logger.space()

        # Print the list of unwanted patterns
        Logger.debug(f"{format_text_bold_for_output(HEADINGS.unwanted_patterns + ':')}")
        Logger.info(f"{SequenceUtils.get_patterns(InputData.unwanted_patterns)}")
        Logger.space()

        if InputData.unwanted_patterns:
            InputData.unwanted_patterns_occurrences = SequenceUtils.get_pattern_occurrences(
                    InputData.cleaned_dna_sequence, InputData.unwanted_patterns)

            per_line = 6
            rows_for_print = [
                {
                    "Pattern": row["Pattern"],
                    "Count": row["Count"],
                    "Positions": ",\n".join(
                        ", ".join(row["Positions"][i:i + per_line])
                        for i in range(0, len(row["Positions"]), per_line)
                    ) if row["Positions"] else "—",
                }
                for row in InputData.unwanted_patterns_occurrences
            ]

            pattern_occurrences = tabulate(
                rows_for_print,
                headers="keys",
                tablefmt="fancy_grid",
                colalign=("left", "left", "left"),
            )

            Logger.debug(format_text_bold_for_output(HEADINGS.unwanted_pattern_occurrences + ':'))
            Logger.info(pattern_occurrences)
            Logger.space()

        # Eliminate unwanted patterns — show a spinner with elapsed-time
        # counter while the algorithm runs so the terminal doesn't look
        # frozen on long sequences.
        run_with_spinner(
            "Computation in progress. This may take a few moments for long sequences",
            eliminate_unwanted_patterns,
            InputData.cleaned_dna_sequence,
            InputData.unwanted_patterns,
            InputData.coding_positions,
        )

        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))
        Logger.info(EliminationData.info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))

        if CostData.optimized_codon:
            Logger.debug(f"CAI for the optimized sequence = {OutputData.cai}")
            Logger.space()

        Logger.debug(format_text_bold_for_output(HEADINGS.optimized_sequence + ':'))
        Logger.info(OutputData.optimized_sequence)
        Logger.space()


        detailed_cost_contributions= tabulate(
            EliminationData.cost_contribution,
            headers="keys",
            tablefmt="fancy_grid",
            colalign=("left", "left", "left", "left")
        )

        Logger.debug(format_text_bold_for_output(HEADINGS.detailed_cost_contributions + ':'))
        Logger.info(detailed_cost_contributions)
        Logger.space()

        detailed_cost_substitutions = tabulate(
            EliminationData.cost_substitution,
            headers="keys",
            tablefmt="fancy_grid",
            colalign=("left", "left", "left", "left")
        )

        Logger.debug(format_text_bold_for_output(HEADINGS.detailed_cost_substitutions + ':'))
        Logger.info(detailed_cost_substitutions)

        Logger.space()

        # Save the results
        report = ReportBuilder()

        Logger.critical("The final report and optimized sequence can be found in the following paths:\n")
        file_date = datetime.today().strftime("%d-%b-%Y_%H-%M-%S")
        report.create_report(file_date)
        path = report.download_report(OutputData.output_path)
        Logger.notice(path)

        filename = f"Optimized-Sequence_{file_date}.txt"
        path = save_file(OutputData.optimized_sequence, filename, OutputData.output_path)
        Logger.notice(path)

        filename = f"Cost-Contribution_{file_date}.txt"
        path = save_file(detailed_cost_contributions, filename, OutputData.output_path)
        Logger.notice(path)

        filename = f"Cost-Substitution_{file_date}.txt"
        path = save_file(detailed_cost_substitutions, filename, OutputData.output_path)
        Logger.notice(path)
        Logger.space()
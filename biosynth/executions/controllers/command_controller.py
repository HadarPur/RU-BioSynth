import sys
from datetime import datetime

from tabulate import tabulate

from biosynth.agents import (
    AgentError,
    CodingRegionAgent,
    CodingRegionRequest,
    EliminationAgent,
    EliminationRequest,
    PreflightAgent,
    PreflightRequest,
    ReportAgent,
    ReportRequest,
    SaveArtifactsAgent,
    SaveArtifactsRequest,
)
from biosynth.data.app_data import CostData, EliminationData, InputData, OutputData
from biosynth.utils.sequence_display import SequenceUtils
from biosynth.utils.logger import Logger
from biosynth.utils.spinner import run_with_spinner
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
    """CLI orchestrator that drives the multi-agent pipeline.

    Today's CLI prints the target-sequence section before the
    elimination spinner starts (the user wants to see what's being
    processed before committing to a multi-second wait). To preserve
    that interleaved UX we don't use ``Pipeline.run()`` here — we
    invoke the agents directly so we can slot Logger output between
    stages and wrap only the heavy ``EliminationAgent`` in a spinner.

    Each agent is constructed once and reused across runs.
    """

    def __init__(self):
        self.preflight_agent = PreflightAgent()
        self.coding_region_agent = CodingRegionAgent()
        self.elimination_agent = EliminationAgent()
        self.report_agent = ReportAgent()
        self.save_agent = SaveArtifactsAgent()

    def run(self):
        Logger.notice(app_icon_text)

        # --- Preflight ------------------------------------------------------
        try:
            preflight = self.preflight_agent.handle(
                PreflightRequest(dna_sequence=InputData.dna_sequence)
            )
        except AgentError as e:
            Logger.error(e.message)
            sys.exit(e.code)

        # --- Coding-region discovery ---------------------------------------
        try:
            coding = self.coding_region_agent.handle(
                CodingRegionRequest(dna_sequence=preflight.dna_sequence)
            )
        except AgentError as e:
            Logger.error(e.message)
            # Same legacy behaviour: when start-codon validation fails we
            # clear the staged InputData so the next run starts fresh.
            InputData.reset()
            sys.exit(e.code)

        # Sync to app_data globals so anything still reading them
        # (GUI, downstream helpers) sees consistent state.
        InputData.start_codon_identified = coding.start_codon_index
        InputData.cleaned_dna_sequence = coding.cleaned_sequence
        InputData.coding_positions = coding.coding_positions
        InputData.coding_indexes = coding.coding_indexes

        # --- Presentation: target sequence + unwanted patterns -------------
        Logger.debug(f"{format_text_bold_for_output('Target sequence:')}")

        if coding.coding_indexes is not None:
            Logger.notice(
                f'A coding region was identified in the target sequence at '
                f'positions {coding.coding_indexes[0] + 1} - {coding.coding_indexes[1]}:'
            )
            Logger.info(
                SequenceUtils.highlight_sequence_to_terminal(
                    coding.cleaned_sequence, coding.coding_indexes
                )
            )
        else:
            Logger.info(coding.cleaned_sequence)

        Logger.space()

        Logger.debug(f"{format_text_bold_for_output('Unwanted patterns:')}")
        Logger.info(SequenceUtils.get_patterns(InputData.unwanted_patterns))
        Logger.space()

        # --- Elimination (spinner-wrapped) ---------------------------------
        elimination = run_with_spinner(
            "Computation in progress. This may take a few moments for long sequences",
            self.elimination_agent.handle,
            EliminationRequest(
                cleaned_sequence=coding.cleaned_sequence,
                unwanted_patterns=InputData.unwanted_patterns,
                coding_positions=coding.coding_positions,
                codon_usage=CostData.codon_usage,
                alpha=CostData.alpha,
                beta=CostData.beta,
                w=CostData.w,
                optimized_codon=CostData.optimized_codon,
            ),
        )

        # Sync elimination output to app_data globals.
        EliminationData.info = elimination.info
        EliminationData.cost_contribution = elimination.cost_contribution
        EliminationData.cost_substitution = elimination.cost_substitution
        EliminationData.min_cost = elimination.min_cost
        OutputData.optimized_sequence = elimination.optimized_sequence

        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))
        Logger.info(elimination.info)
        Logger.notice(format_text_bold_for_output('\n' + '_' * 90 + '\n'))

        Logger.debug(format_text_bold_for_output('Optimized Sequence:'))
        Logger.info(elimination.optimized_sequence)
        Logger.space()

        # --- Cost tables (rendered once, shared between display and save) --
        detailed_cost_contributions = tabulate(
            elimination.cost_contribution,
            headers="keys",
            tablefmt="fancy_grid",
            colalign=("left", "left", "left", "left"),
        )
        Logger.debug(format_text_bold_for_output(
            'Detailed cost contributions relative to the target sequence:'
        ))
        Logger.info(detailed_cost_contributions)
        Logger.space()

        detailed_cost_substitutions = tabulate(
            elimination.cost_substitution,
            headers="keys",
            tablefmt="fancy_grid",
            colalign=("left", "left", "left", "left"),
        )
        Logger.debug(format_text_bold_for_output(
            'Detailed cost substitutions relative to the target sequence:'
        ))
        Logger.info(detailed_cost_substitutions)
        Logger.space()

        # --- Report + artifact saving --------------------------------------
        Logger.critical(
            "The final report and optimized sequence can be found in the following paths:\n"
        )
        file_date = datetime.today().strftime("%d-%b-%Y_%H-%M-%S")

        report_result = self.report_agent.handle(
            ReportRequest(
                file_date=file_date,
                cleaned_sequence=coding.cleaned_sequence,
                coding_indexes=coding.coding_indexes,
                coding_positions=coding.coding_positions,
                optimized_sequence=elimination.optimized_sequence,
                unwanted_patterns=InputData.unwanted_patterns,
                cost_contribution=elimination.cost_contribution,
                cost_substitution=elimination.cost_substitution,
                min_cost=elimination.min_cost,
                output_path=OutputData.output_path,
            )
        )
        Logger.notice(report_result.downloaded_path)

        save_result = self.save_agent.handle(
            SaveArtifactsRequest(
                output_path=OutputData.output_path,
                artifacts={
                    f"Optimized-Sequence_{file_date}.txt": elimination.optimized_sequence,
                    f"Cost-Contribution_{file_date}.txt": detailed_cost_contributions,
                    f"Cost-Substitution_{file_date}.txt": detailed_cost_substitutions,
                },
            )
        )
        # Preserve the legacy print order: optimized sequence, then
        # cost-contribution, then cost-substitution. Python ≥3.7 keeps
        # insertion order on dicts so iterating ``saved_paths`` is safe.
        for path in save_result.saved_paths.values():
            Logger.notice(path)
        Logger.space()

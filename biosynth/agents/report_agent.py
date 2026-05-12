"""Stage that renders the HTML report and saves it to disk."""

from biosynth.agents.base import Agent
from biosynth.agents.messages import ReportRequest, ReportResult
from biosynth.report.report_controller import ReportController


class ReportAgent(Agent[ReportRequest, ReportResult]):
    """Wraps :class:`ReportController` with explicit per-call inputs.

    Uses the widened ``ReportController.__init__`` signature so the
    agent stays pure — no reads from module-level globals.
    """

    name = "report"

    def handle(self, request: ReportRequest) -> ReportResult:
        controller = ReportController(
            cleaned_dna_sequence=request.cleaned_sequence,
            coding_indexes=request.coding_indexes,
            coding_positions=request.coding_positions,
            optimized_sequence=request.optimized_sequence,
            unwanted_patterns=request.unwanted_patterns,
            cost_contribution=request.cost_contribution,
            cost_substitution=request.cost_substitution,
            min_cost=request.min_cost,
        )
        local_path = controller.create_report(request.file_date)
        downloaded = controller.download_report(request.output_path)

        return ReportResult(
            report_filename=controller.report_filename,
            local_report_path=local_path,
            downloaded_path=downloaded,
        )

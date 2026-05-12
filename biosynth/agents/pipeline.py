"""Linear orchestrator chaining the BioSynth pipeline agents.

The pipeline is intentionally linear because the underlying algorithm
is linear: each stage's output feeds the next. The orchestrator's job
is just message routing — no algorithmic logic lives here.
"""

from __future__ import annotations

from typing import Callable, Optional

from biosynth.agents.base import Agent
from biosynth.agents.coding_region_agent import CodingRegionAgent
from biosynth.agents.elimination_agent import EliminationAgent
from biosynth.agents.messages import (
    CodingRegionRequest,
    EliminationRequest,
    PipelineRequest,
    PipelineResult,
    PreflightRequest,
    ReportRequest,
    SaveArtifactsRequest,
)
from biosynth.agents.preflight_agent import PreflightAgent
from biosynth.agents.report_agent import ReportAgent
from biosynth.agents.save_artifacts_agent import SaveArtifactsAgent


_OPTIMIZED_SEQUENCE_PREFIX = "Optimized-Sequence"
_COST_CONTRIBUTION_PREFIX = "Cost-Contribution"
_COST_SUBSTITUTION_PREFIX = "Cost-Substitution"


class Pipeline:
    """Run a single end-to-end BioSynth pass via cooperating agents.

    Agents are injectable for testing — pass alternative implementations
    in the constructor. The default factory uses the production agents.
    """

    def __init__(
        self,
        *,
        preflight: Optional[Agent] = None,
        coding_region: Optional[Agent] = None,
        elimination: Optional[Agent] = None,
        report: Optional[Agent] = None,
        save: Optional[Agent] = None,
    ):
        self.preflight = preflight or PreflightAgent()
        self.coding_region = coding_region or CodingRegionAgent()
        self.elimination = elimination or EliminationAgent()
        self.report = report or ReportAgent()
        self.save = save or SaveArtifactsAgent()

    def run(
        self,
        request: PipelineRequest,
        *,
        on_step: Optional[Callable[[str, object], None]] = None,
    ) -> PipelineResult:
        """Execute the full pipeline and return a consolidated result.

        ``on_step`` (if provided) is invoked after each stage with
        ``(stage_name, stage_result)`` — useful for progress UIs.
        """
        # 1. Preflight — non-empty sequence check.
        preflight = self.preflight.handle(
            PreflightRequest(dna_sequence=request.dna_sequence)
        )
        self._emit(on_step, self.preflight.name, preflight)

        # 2. Coding region — start codon + per-position phase tagging.
        coding = self.coding_region.handle(
            CodingRegionRequest(dna_sequence=preflight.dna_sequence)
        )
        self._emit(on_step, self.coding_region.name, coding)

        # 3. Elimination — FSM + DP optimization.
        elimination = self.elimination.handle(
            EliminationRequest(
                cleaned_sequence=coding.cleaned_sequence,
                unwanted_patterns=request.unwanted_patterns,
                coding_positions=coding.coding_positions,
                codon_usage=request.codon_usage,
                alpha=request.alpha,
                beta=request.beta,
                w=request.w,
                optimized_codon=request.optimized_codon,
            )
        )
        self._emit(on_step, self.elimination.name, elimination)

        # 4. Report — render HTML and copy to the output dir.
        report = self.report.handle(
            ReportRequest(
                file_date=request.file_date,
                cleaned_sequence=coding.cleaned_sequence,
                coding_indexes=coding.coding_indexes,
                coding_positions=coding.coding_positions,
                optimized_sequence=elimination.optimized_sequence,
                unwanted_patterns=request.unwanted_patterns,
                cost_contribution=elimination.cost_contribution,
                cost_substitution=elimination.cost_substitution,
                min_cost=elimination.min_cost,
                output_path=request.output_path,
            )
        )
        self._emit(on_step, self.report.name, report)

        # 5. Save artifacts — optimized sequence + the two cost tables.
        artifacts = {
            f"{_OPTIMIZED_SEQUENCE_PREFIX}_{request.file_date}.txt": (
                elimination.optimized_sequence or ""
            ),
        }
        # The caller pre-renders the tabulated cost tables (so terminal
        # display and the saved files share one source of truth).
        cost_contribution_text = request.extra_artifacts.get(_COST_CONTRIBUTION_PREFIX)
        cost_substitution_text = request.extra_artifacts.get(_COST_SUBSTITUTION_PREFIX)
        if cost_contribution_text is not None:
            artifacts[f"{_COST_CONTRIBUTION_PREFIX}_{request.file_date}.txt"] = (
                cost_contribution_text
            )
        if cost_substitution_text is not None:
            artifacts[f"{_COST_SUBSTITUTION_PREFIX}_{request.file_date}.txt"] = (
                cost_substitution_text
            )

        saved = self.save.handle(
            SaveArtifactsRequest(
                output_path=request.output_path,
                artifacts=artifacts,
            )
        )
        self._emit(on_step, self.save.name, saved)

        return PipelineResult(
            cleaned_sequence=coding.cleaned_sequence,
            start_codon_index=coding.start_codon_index,
            coding_positions=coding.coding_positions,
            coding_indexes=coding.coding_indexes,
            elimination_info=elimination.info,
            optimized_sequence=elimination.optimized_sequence,
            cost_contribution=elimination.cost_contribution,
            cost_substitution=elimination.cost_substitution,
            min_cost=elimination.min_cost,
            report_filename=report.report_filename,
            local_report_path=report.local_report_path,
            downloaded_report_path=report.downloaded_path,
            saved_artifact_paths=saved.saved_paths,
        )

    @staticmethod
    def _emit(callback, name, payload):
        if callback is not None:
            callback(name, payload)

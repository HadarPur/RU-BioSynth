"""Tests for biosynth.agents.pipeline.Pipeline."""

import os
import tempfile
import unittest
from pathlib import Path

from biosynth.agents.base import Agent, AgentError
from biosynth.agents.messages import (
    CodingRegionResult,
    EliminationResult,
    PipelineRequest,
    PreflightResult,
    ReportResult,
    SaveArtifactsResult,
)
from biosynth.agents.pipeline import Pipeline
from biosynth.utils.cost_utils import normalize_codon_usage
from biosynth.utils.text_utils import OutputFormat, set_output_format


def _flat_codon_usage():
    bases = "ACGT"
    return normalize_codon_usage({a + b + c: 0.5 for a in bases for b in bases for c in bases})


def _base_request(tmpdir):
    return PipelineRequest(
        dna_sequence="ATAGTAC",
        unwanted_patterns={"TAGTAC"},
        codon_usage=_flat_codon_usage(),
        alpha=1.0,
        beta=2.0,
        w=100.0,
        optimized_codon=False,
        output_path=Path(tmpdir),
        file_date="01-Jan-1970_00-00-00",
        extra_artifacts={
            "Cost-Contribution": "fake contribution table",
            "Cost-Substitution": "fake substitution table",
        },
    )


class TestPipelineEndToEnd(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TERMINAL)

    def test_full_run_returns_consolidated_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            pipeline = Pipeline()
            result = pipeline.run(_base_request(tmp))

            # Elimination removed the pattern.
            self.assertNotIn("TAGTAC", result.optimized_sequence)
            self.assertGreaterEqual(result.min_cost, 0.0)

            # Report rendered to a local file AND copied under the
            # caller's output_path.
            self.assertTrue(os.path.exists(result.local_report_path))
            outputs_dir = Path(tmp) / "BioSynth-Outputs"
            self.assertTrue(outputs_dir.is_dir())
            saved_files = set(os.listdir(outputs_dir))
            self.assertTrue(any(n.startswith("BioSynth-Report_") for n in saved_files))
            self.assertTrue(
                any(n.startswith("Optimized-Sequence_") for n in saved_files)
            )
            self.assertTrue(
                any(n.startswith("Cost-Contribution_") for n in saved_files)
            )
            self.assertTrue(
                any(n.startswith("Cost-Substitution_") for n in saved_files)
            )

            # Cleanup the locally-rendered HTML.
            os.remove(result.local_report_path)

    def test_progress_callback_fires_for_every_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            seen = []

            def on_step(name, payload):
                seen.append((name, type(payload).__name__))

            pipeline = Pipeline()
            pipeline.run(_base_request(tmp), on_step=on_step)

            stage_names = [name for name, _ in seen]
            self.assertEqual(
                stage_names,
                ["preflight", "coding-region", "elimination", "report", "save-artifacts"],
            )
            self.assertEqual(
                [t for _, t in seen],
                [
                    "PreflightResult",
                    "CodingRegionResult",
                    "EliminationResult",
                    "ReportResult",
                    "SaveArtifactsResult",
                ],
            )

            # Clean up the local HTML the report agent wrote.
            for fname in os.listdir("output"):
                if fname.startswith("BioSynth-Report_") and fname.endswith(".html"):
                    os.remove(os.path.join("output", fname))


class TestPipelineErrorPropagation(unittest.TestCase):
    """An AgentError raised by any stage propagates out of run()."""

    def test_preflight_error_bubbles_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            pipeline = Pipeline()
            req = _base_request(tmp)
            # Replace the dna_sequence with None — preflight rejects it.
            req = PipelineRequest(
                dna_sequence=None,
                unwanted_patterns=req.unwanted_patterns,
                codon_usage=req.codon_usage,
                alpha=req.alpha,
                beta=req.beta,
                w=req.w,
                optimized_codon=req.optimized_codon,
                output_path=req.output_path,
                file_date=req.file_date,
                extra_artifacts=req.extra_artifacts,
            )
            with self.assertRaises(AgentError) as cm:
                pipeline.run(req)
            self.assertEqual(cm.exception.code, 3)


class TestPipelineInjectableAgents(unittest.TestCase):
    """Custom agent instances can be passed to Pipeline for testing /
    extension — the orchestrator doesn't hard-code production agents.
    """

    def test_custom_agents_are_invoked(self):
        class FakePreflight(Agent):
            name = "preflight"
            calls = 0

            def handle(self, request):
                FakePreflight.calls += 1
                return PreflightResult(dna_sequence="ZZZ")

        class FakeCoding(Agent):
            name = "coding-region"

            def handle(self, request):
                return CodingRegionResult(
                    cleaned_sequence=request.dna_sequence,
                    start_codon_index=None,
                    coding_positions=[0, 0, 0],
                    coding_indexes=None,
                )

        class FakeElimination(Agent):
            name = "elimination"

            def handle(self, request):
                return EliminationResult(
                    info="stub",
                    optimized_sequence=request.cleaned_sequence,
                    cost_contribution=[],
                    cost_substitution=[],
                    min_cost=0.0,
                )

        class FakeReport(Agent):
            name = "report"

            def handle(self, request):
                return ReportResult(
                    report_filename="r.html",
                    local_report_path="output/r.html",
                    downloaded_path="/tmp/r.html",
                )

        class FakeSave(Agent):
            name = "save-artifacts"

            def handle(self, request):
                return SaveArtifactsResult(
                    saved_paths={k: "/tmp/" + k for k in request.artifacts}
                )

        pipeline = Pipeline(
            preflight=FakePreflight(),
            coding_region=FakeCoding(),
            elimination=FakeElimination(),
            report=FakeReport(),
            save=FakeSave(),
        )

        with tempfile.TemporaryDirectory() as tmp:
            result = pipeline.run(_base_request(tmp))

        self.assertEqual(FakePreflight.calls, 1)
        self.assertEqual(result.optimized_sequence, "ZZZ")
        self.assertEqual(result.report_filename, "r.html")
        # Optimized-Sequence + the two extra_artifacts get saved.
        self.assertEqual(set(result.saved_artifact_paths.keys()), {
            "Optimized-Sequence_01-Jan-1970_00-00-00.txt",
            "Cost-Contribution_01-Jan-1970_00-00-00.txt",
            "Cost-Substitution_01-Jan-1970_00-00-00.txt",
        })


class TestPipelineWithoutExtraArtifacts(unittest.TestCase):
    """If the caller doesn't pre-render cost tables, only the optimized
    sequence is saved — the orchestrator never invents missing artifacts.
    """

    def test_only_optimized_sequence_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = PipelineRequest(
                dna_sequence="ATAGTAC",
                unwanted_patterns={"TAGTAC"},
                codon_usage=_flat_codon_usage(),
                alpha=1.0,
                beta=2.0,
                w=100.0,
                optimized_codon=False,
                output_path=Path(tmp),
                file_date="01-Jan-1970_00-00-00",
                # extra_artifacts defaults to {}.
            )
            pipeline = Pipeline()
            result = pipeline.run(req)

            self.assertEqual(set(result.saved_artifact_paths.keys()), {
                "Optimized-Sequence_01-Jan-1970_00-00-00.txt",
            })

            # Cleanup the report HTML that ReportAgent wrote locally.
            os.remove(result.local_report_path)
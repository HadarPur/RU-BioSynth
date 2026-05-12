"""Tests for biosynth.agents.messages.

The message types are simple frozen dataclasses; the tests confirm
construction, immutability, and the package-level re-exports.
"""

import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from biosynth.agents import messages as msgs
from biosynth.agents.messages import (
    CodingRegionRequest,
    CodingRegionResult,
    EliminationRequest,
    EliminationResult,
    PipelineRequest,
    PipelineResult,
    PreflightRequest,
    PreflightResult,
    ReportRequest,
    ReportResult,
    SaveArtifactsRequest,
    SaveArtifactsResult,
)


class TestMessagesAreFrozen(unittest.TestCase):
    def test_preflight_request_frozen(self):
        r = PreflightRequest(dna_sequence="ATG")
        with self.assertRaises(FrozenInstanceError):
            r.dna_sequence = "GCC"  # type: ignore[misc]

    def test_pipeline_request_has_default_extra_artifacts(self):
        req = PipelineRequest(
            dna_sequence="ATG",
            unwanted_patterns={"GGG"},
            codon_usage={"ATG": 0.0},
            alpha=1.0,
            beta=2.0,
            w=100.0,
            optimized_codon=False,
            output_path=Path("/tmp"),
            file_date="01-Jan-1970_00-00-00",
        )
        self.assertEqual(req.extra_artifacts, {})


class TestRoundTrip(unittest.TestCase):
    def test_construct_each_message_type(self):
        # PreflightRequest / Result
        self.assertEqual(
            PreflightRequest(dna_sequence="ATG").dna_sequence, "ATG"
        )
        self.assertEqual(PreflightResult(dna_sequence="ATG").dna_sequence, "ATG")

        # CodingRegion
        cr_req = CodingRegionRequest(dna_sequence="ATG")
        self.assertEqual(cr_req.dna_sequence, "ATG")
        cr_res = CodingRegionResult(
            cleaned_sequence="ATG",
            start_codon_index=None,
            coding_positions=[0, 0, 0],
            coding_indexes=None,
        )
        self.assertEqual(cr_res.cleaned_sequence, "ATG")

        # Elimination
        el_req = EliminationRequest(
            cleaned_sequence="ATG",
            unwanted_patterns={"GGG"},
            coding_positions=[0, 0, 0],
            codon_usage={},
            alpha=1.0,
            beta=2.0,
            w=100.0,
            optimized_codon=False,
        )
        self.assertEqual(el_req.alpha, 1.0)
        el_res = EliminationResult(
            info="ok",
            optimized_sequence="ATG",
            cost_contribution=[],
            cost_substitution=[],
            min_cost=0.0,
        )
        self.assertEqual(el_res.min_cost, 0.0)

        # Report
        rep_req = ReportRequest(
            file_date="01-Jan-1970_00-00-00",
            cleaned_sequence="ATG",
            coding_indexes=None,
            coding_positions=[0, 0, 0],
            optimized_sequence="ATG",
            unwanted_patterns={"GGG"},
            cost_contribution=[],
            cost_substitution=[],
            min_cost=0.0,
        )
        self.assertIsNone(rep_req.output_path)
        rep_res = ReportResult(
            report_filename="r.html",
            local_report_path="output/r.html",
            downloaded_path="/tmp/r.html",
        )
        self.assertEqual(rep_res.report_filename, "r.html")

        # SaveArtifacts
        sa_req = SaveArtifactsRequest(
            output_path=Path("/tmp"), artifacts={"a.txt": "hello"}
        )
        self.assertEqual(sa_req.artifacts["a.txt"], "hello")
        sa_res = SaveArtifactsResult(saved_paths={"a.txt": "/tmp/a.txt"})
        self.assertEqual(sa_res.saved_paths["a.txt"], "/tmp/a.txt")

        # PipelineResult
        pr = PipelineResult(
            cleaned_sequence="ATG",
            start_codon_index=None,
            coding_positions=[0, 0, 0],
            coding_indexes=None,
            elimination_info="ok",
            optimized_sequence="ATG",
            cost_contribution=[],
            cost_substitution=[],
            min_cost=0.0,
            report_filename="r.html",
            local_report_path="output/r.html",
            downloaded_report_path="/tmp/r.html",
            saved_artifact_paths={},
        )
        self.assertEqual(pr.elimination_info, "ok")


class TestReexports(unittest.TestCase):
    def test_all_message_classes_importable_from_package(self):
        # All message classes are exported from biosynth.agents.
        import biosynth.agents as pkg

        for name in (
            "PreflightRequest", "PreflightResult",
            "CodingRegionRequest", "CodingRegionResult",
            "EliminationRequest", "EliminationResult",
            "ReportRequest", "ReportResult",
            "SaveArtifactsRequest", "SaveArtifactsResult",
            "PipelineRequest", "PipelineResult",
        ):
            self.assertTrue(hasattr(pkg, name), f"agents.{name} missing")
            self.assertIs(getattr(pkg, name), getattr(msgs, name))
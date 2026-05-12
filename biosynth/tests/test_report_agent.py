"""Tests for biosynth.agents.report_agent."""

import os
import tempfile
import unittest
from pathlib import Path

from biosynth.agents.messages import ReportRequest
from biosynth.agents.report_agent import ReportAgent
from biosynth.utils.text_utils import OutputFormat, set_output_format


class TestReportAgent(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TERMINAL)
        self.agent = ReportAgent()

    def test_name(self):
        self.assertEqual(self.agent.name, "report")

    def test_renders_and_downloads_to_custom_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = ReportRequest(
                file_date="01-Jan-1970_00-00-00",
                cleaned_sequence="ATGAAATAA",
                coding_indexes=(0, 9),
                coding_positions=[1, 2, -3, 1, 2, 3, 1, 2, 3],
                optimized_sequence="ATGAAATAA",
                unwanted_patterns={"GGGG"},
                cost_contribution=[],
                cost_substitution=[],
                min_cost=0.0,
                output_path=Path(tmp),
            )
            result = self.agent.handle(req)

            # The locally-rendered HTML lives under ``output/``.
            self.assertTrue(os.path.exists(result.local_report_path))
            self.assertTrue(result.report_filename.endswith(".html"))
            # The downloaded path string mentions the chosen output dir.
            self.assertIn("BioSynth-Outputs", result.downloaded_path)
            # And the file actually exists there.
            outputs_dir = Path(tmp) / "BioSynth-Outputs"
            self.assertTrue(outputs_dir.is_dir())
            self.assertTrue(any(
                f.endswith(".html") for f in os.listdir(outputs_dir)
            ))

            # Cleanup the local copy too.
            os.remove(result.local_report_path)
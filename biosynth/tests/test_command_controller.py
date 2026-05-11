"""Tests for biosynth.executions.controllers.command_controller."""

import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from biosynth.data import app_data
from biosynth.executions.controllers.command_controller import CommandController
from biosynth.utils.cost_utils import normalize_codon_usage
from biosynth.utils.text_utils import OutputFormat, set_output_format


def _seed_inputs():
    """Set up InputData / CostData with a minimal valid scenario."""
    # Non-coding sequence with an unwanted pattern that forces a substitution.
    app_data.InputData.dna_sequence = "ATAGTAC"
    app_data.InputData.cleaned_dna_sequence = None  # filled by controller
    app_data.InputData.unwanted_patterns = {"TAGTAC"}
    app_data.InputData.coding_indexes = None
    app_data.InputData.coding_positions = None
    app_data.InputData.start_codon_identified = None

    bases = "ACGT"
    raw = {a + b + c: 0.5 for a in bases for b in bases for c in bases}
    app_data.CostData.codon_usage = normalize_codon_usage(raw)
    app_data.CostData.codon_usage_filename = "stub.txt"
    app_data.CostData.alpha = 1.0
    app_data.CostData.beta = 2.0
    app_data.CostData.w = 100.0
    app_data.CostData.optimized_codon = False


class TestCommandController(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TERMINAL)
        _seed_inputs()
        self._stdout = StringIO()
        self._patch_stdout = patch("sys.stdout", self._stdout)
        self._patch_stdout.start()

    def tearDown(self):
        self._patch_stdout.stop()
        # Best-effort cleanup of any output/* HTML produced.
        if os.path.isdir("output"):
            for f in os.listdir("output"):
                if f.startswith("BioSynth-Report_") and f.endswith(".html"):
                    os.remove(os.path.join("output", f))

    def test_runs_end_to_end_with_custom_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            app_data.OutputData.output_path = Path(tmp)
            CommandController().run()
            outputs_dir = Path(tmp) / "BioSynth-Outputs"
            self.assertTrue(outputs_dir.is_dir())
            names = os.listdir(outputs_dir)
            # The controller writes a report, optimized sequence, and
            # the two cost tables.
            self.assertTrue(any(n.startswith("BioSynth-Report_") for n in names))
            self.assertTrue(any(n.startswith("Optimized-Sequence_") for n in names))
            self.assertTrue(any(n.startswith("Cost-Contribution_") for n in names))
            self.assertTrue(any(n.startswith("Cost-Substitution_") for n in names))

    def test_exits_with_empty_sequence(self):
        app_data.InputData.dna_sequence = ""
        with self.assertRaises(SystemExit) as cm:
            CommandController().run()
        self.assertEqual(cm.exception.code, 3)

    def test_exits_on_invalid_start_codon_marker(self):
        app_data.InputData.dna_sequence = "AA*CCC"  # '*' but no ATG after
        with self.assertRaises(SystemExit) as cm:
            CommandController().run()
        self.assertEqual(cm.exception.code, 3)

    def test_runs_with_coding_region_logger_branch(self):
        # A sequence containing the '*ATG...TAA' marker forces the coding-
        # region rendering branch in CommandController.run. The pattern
        # must appear in the cleaned sequence so the algorithm runs through
        # the full backtrack-and-return path.
        app_data.InputData.dna_sequence = "AAA*ATGAAATAA"  # cleaned: AAAATGAAATAA
        app_data.InputData.unwanted_patterns = {"AAATAA"}
        with tempfile.TemporaryDirectory() as tmp:
            app_data.OutputData.output_path = Path(tmp)
            CommandController().run()
            outputs_dir = Path(tmp) / "BioSynth-Outputs"
            self.assertTrue(outputs_dir.is_dir())
            self.assertTrue(any(
                f.startswith("BioSynth-Report_")
                for f in os.listdir(outputs_dir)
            ))


if __name__ == "__main__":
    unittest.main()

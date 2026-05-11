"""Tests for biosynth.executions.controllers.cli_controller.

These exercise CLIController.execute via fixture files. The CommandController
called at the end is patched out so we only validate the orchestration path
(file reading + validation + state population + optional knob plumbing).
"""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from biosynth.data import app_data
from biosynth.executions.controllers.cli_controller import CLIController
from biosynth.utils.text_utils import OutputFormat, set_output_format


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _sample_codon_usage():
    bases = "ACGT"
    lines = [f"{a+b+c} 0.5" for a in bases for b in bases for c in bases]
    return "\n".join(lines) + "\n"


class _Fixtures:
    """Context that creates the three fixture files and returns their paths."""

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.seq = os.path.join(d, "seq.txt")
        self.pat = os.path.join(d, "pat.txt")
        self.cod = os.path.join(d, "cod.txt")
        _write(self.seq, "ATAGTAC\n")
        _write(self.pat, "TAGTAC\n")
        _write(self.cod, _sample_codon_usage())
        return self

    def __exit__(self, *exc):
        self.tmp.cleanup()


class TestCLIController(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TERMINAL)
        # Silence the CLI logger.
        self._stdout = StringIO()
        self._patch_stdout = patch("sys.stdout", self._stdout)
        self._patch_stdout.start()
        # Stub out the inner CommandController so we test only CLIController.
        self._patch_command = patch(
            "biosynth.executions.controllers.cli_controller.CommandController"
        )
        self.MockCommand = self._patch_command.start()

    def tearDown(self):
        self._patch_command.stop()
        self._patch_stdout.stop()

    def test_happy_path_invokes_command_controller(self):
        with _Fixtures() as f:
            argv = ["-s", f.seq, "-p", f.pat, "-c", f.cod]
            CLIController(argv).execute()
        self.MockCommand.assert_called_once()
        self.MockCommand.return_value.run.assert_called_once()
        # State should have been populated.
        self.assertEqual(app_data.InputData.dna_sequence, "ATAGTAC")
        self.assertIn("TAGTAC", app_data.InputData.unwanted_patterns)
        self.assertIsNotNone(app_data.CostData.codon_usage)

    def test_optional_knobs_plumbed_through(self):
        with _Fixtures() as f:
            argv = [
                "-s", f.seq, "-p", f.pat, "-c", f.cod,
                "-a", "1.5", "-b", "3.0", "-w", "200",
                "-oc", "no",
            ]
            with tempfile.TemporaryDirectory() as out:
                argv += ["-o", out]
                CLIController(argv).execute()
        self.assertEqual(app_data.CostData.alpha, 1.5)
        self.assertEqual(app_data.CostData.beta, 3.0)
        self.assertEqual(app_data.CostData.w, 200.0)
        self.assertFalse(app_data.CostData.optimized_codon)

    def test_invalid_input_exits(self):
        with _Fixtures() as f:
            # Overwrite sequence with invalid characters.
            _write(f.seq, "ATGN\n")
            argv = ["-s", f.seq, "-p", f.pat, "-c", f.cod]
            with self.assertRaises(SystemExit) as cm:
                CLIController(argv).execute()
            self.assertEqual(cm.exception.code, 2)
        self.MockCommand.assert_not_called()

    def test_invalid_cost_exits(self):
        with _Fixtures() as f:
            # alpha < beta violated.
            argv = [
                "-s", f.seq, "-p", f.pat, "-c", f.cod,
                "-a", "5.0", "-b", "2.0",
            ]
            with self.assertRaises(SystemExit) as cm:
                CLIController(argv).execute()
            self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()

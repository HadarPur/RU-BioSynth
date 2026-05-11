"""Tests for biosynth.executions.controllers.debug_controller.

The DebugController loads its inputs from biosynth.settings.* modules and
runs CommandController twice (once with each value of optimized_codon).
We patch the CommandController to keep the test fast and offline.
"""

import unittest
from io import StringIO
from unittest.mock import patch

from biosynth.data import app_data
from biosynth.executions.controllers.debug_controller import DebugController
from biosynth.utils.text_utils import OutputFormat, set_output_format


class TestDebugController(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TERMINAL)
        self._stdout = StringIO()
        self._patch_stdout = patch("sys.stdout", self._stdout)
        self._patch_stdout.start()
        self._patch_command = patch(
            "biosynth.executions.controllers.debug_controller.CommandController"
        )
        self.MockCommand = self._patch_command.start()

    def tearDown(self):
        self._patch_command.stop()
        self._patch_stdout.stop()

    def test_runs_command_controller_twice_for_both_optimized_codon_modes(self):
        DebugController.execute()
        # Two invocations of CommandController() — once per optimized_codon value.
        self.assertEqual(self.MockCommand.call_count, 2)
        self.assertEqual(self.MockCommand.return_value.run.call_count, 2)
        # After execution, optimized_codon should be left at True (the second run).
        self.assertTrue(app_data.CostData.optimized_codon)
        # Cost params updated to the hard-coded debug values.
        self.assertAlmostEqual(app_data.CostData.alpha, 1.02)
        self.assertAlmostEqual(app_data.CostData.beta, 1.98)
        self.assertAlmostEqual(app_data.CostData.w, 99.96)

    def test_short_circuits_on_invalid_input(self):
        # If is_valid_input returns False, DebugController returns early
        # without ever building a CommandController.
        with patch(
            "biosynth.executions.controllers.debug_controller.is_valid_input",
            return_value=False,
        ):
            DebugController.execute()
        self.MockCommand.assert_not_called()

    def test_short_circuits_on_invalid_cost(self):
        with patch(
            "biosynth.executions.controllers.debug_controller.is_valid_cost",
            return_value=False,
        ):
            DebugController.execute()
        self.MockCommand.assert_not_called()


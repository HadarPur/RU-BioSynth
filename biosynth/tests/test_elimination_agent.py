"""Tests for biosynth.agents.elimination_agent."""

import unittest

from biosynth.agents.elimination_agent import EliminationAgent
from biosynth.agents.messages import EliminationRequest
from biosynth.utils.cost_utils import normalize_codon_usage


def _flat_codon_usage():
    bases = "ACGT"
    return normalize_codon_usage({a + b + c: 0.5 for a in bases for b in bases for c in bases})


class TestEliminationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EliminationAgent()

    def test_name(self):
        self.assertEqual(self.agent.name, "elimination")

    def test_no_unwanted_patterns_returns_unchanged_sequence(self):
        # Early-return branch in eliminate(): 4-tuple result.
        result = self.agent.handle(
            EliminationRequest(
                cleaned_sequence="ATATATAT",
                unwanted_patterns={"GGGG"},
                coding_positions=[0] * 8,
                codon_usage=_flat_codon_usage(),
                alpha=1.0,
                beta=2.0,
                w=100.0,
                optimized_codon=False,
            )
        )
        self.assertEqual(result.optimized_sequence, "ATATATAT")
        self.assertEqual(result.min_cost, 0.0)
        # 4-tuple path leaves substitutions as None.
        self.assertIsNone(result.cost_substitution)

    def test_patterns_eliminated(self):
        # Normal-return branch: 5-tuple, agent fills both contribution and
        # substitution lists.
        result = self.agent.handle(
            EliminationRequest(
                cleaned_sequence="ATAGTAC",
                unwanted_patterns={"TAGTAC"},
                coding_positions=[0] * 7,
                codon_usage=_flat_codon_usage(),
                alpha=1.0,
                beta=2.0,
                w=100.0,
                optimized_codon=False,
            )
        )
        self.assertIsNotNone(result.optimized_sequence)
        self.assertNotIn("TAGTAC", result.optimized_sequence)
        self.assertIsNotNone(result.cost_contribution)
        self.assertIsNotNone(result.cost_substitution)
        self.assertGreaterEqual(result.min_cost, 0.0)

    def test_explicit_params_dont_read_globals(self):
        # The agent passes alpha/beta/w/optimized_codon explicitly. We
        # verify that by setting CostData to garbage and confirming the
        # explicit params win.
        from biosynth.data import app_data

        original = (
            app_data.CostData.alpha,
            app_data.CostData.beta,
            app_data.CostData.w,
            app_data.CostData.optimized_codon,
            app_data.CostData.codon_usage,
        )
        try:
            app_data.CostData.alpha = 99
            app_data.CostData.beta = 99
            app_data.CostData.w = 99
            app_data.CostData.optimized_codon = True
            app_data.CostData.codon_usage = None  # would crash if agent used it
            result = self.agent.handle(
                EliminationRequest(
                    cleaned_sequence="ATATATAT",
                    unwanted_patterns={"GGGG"},
                    coding_positions=[0] * 8,
                    codon_usage=_flat_codon_usage(),
                    alpha=1.0,
                    beta=2.0,
                    w=100.0,
                    optimized_codon=False,
                )
            )
            self.assertEqual(result.optimized_sequence, "ATATATAT")
        finally:
            (
                app_data.CostData.alpha,
                app_data.CostData.beta,
                app_data.CostData.w,
                app_data.CostData.optimized_codon,
                app_data.CostData.codon_usage,
            ) = original
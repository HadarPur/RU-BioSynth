"""Tests for biosynth.executions.execution_utils.

Covers the four validators (is_valid_dna / is_valid_patterns /
is_valid_codon_usage / is_valid_cost), the composite is_valid_input
helper, and the elimination/report orchestration helpers.
"""

import unittest
from unittest.mock import patch

from biosynth.data import app_data
from biosynth.executions import execution_utils as eu


def _full_codon_usage():
    """Return a 64-codon usage dict acceptable to is_valid_codon_usage."""
    bases = "ACGT"
    return {a + b + c: 0.01 for a in bases for b in bases for c in bases}


class TestIsValidDna(unittest.TestCase):
    def test_accepts_atgcu_and_star(self):
        self.assertTrue(eu.is_valid_dna("ATGCATGCU*"))

    def test_rejects_unknown_base(self):
        self.assertFalse(eu.is_valid_dna("ATGN"))

    def test_handles_lowercase(self):
        self.assertTrue(eu.is_valid_dna("atgc"))

    def test_empty_string_is_valid_alphabet(self):
        # Alphabet check passes for "". (is_valid_input handles the
        # empty-sequence error separately.)
        self.assertTrue(eu.is_valid_dna(""))


class TestIsValidPatterns(unittest.TestCase):
    def test_accepts_valid_set(self):
        self.assertTrue(eu.is_valid_patterns({"ATGC", "GGGG"}))

    def test_rejects_invalid_base(self):
        self.assertFalse(eu.is_valid_patterns({"ATGN"}))

    def test_empty_set_is_valid_alphabet(self):
        self.assertTrue(eu.is_valid_patterns(set()))


class TestIsValidCodonUsage(unittest.TestCase):
    def test_accepts_full_64_codon_table(self):
        self.assertTrue(eu.is_valid_codon_usage(_full_codon_usage()))

    def test_rejects_short_table(self):
        usage = _full_codon_usage()
        usage.pop("ATG")
        self.assertFalse(eu.is_valid_codon_usage(usage))

    def test_rejects_bad_codon_letters(self):
        usage = _full_codon_usage()
        # Replace one entry with an invalid codon
        usage.pop("ATG")
        usage["XTG"] = 0.5
        self.assertFalse(eu.is_valid_codon_usage(usage))

    def test_rejects_wrong_codon_length(self):
        usage = _full_codon_usage()
        usage.pop("ATG")
        usage["ATGG"] = 0.5
        self.assertFalse(eu.is_valid_codon_usage(usage))

    def test_rejects_negative_freq(self):
        usage = _full_codon_usage()
        usage["ATG"] = -1.0
        self.assertFalse(eu.is_valid_codon_usage(usage))

    def test_rejects_non_numeric_freq(self):
        usage = _full_codon_usage()
        usage["ATG"] = "high"
        self.assertFalse(eu.is_valid_codon_usage(usage))


class TestIsValidInput(unittest.TestCase):
    def setUp(self):
        self.usage = _full_codon_usage()

    def test_happy_path(self):
        self.assertTrue(eu.is_valid_input("ATGC", {"GGGG"}, self.usage))

    def test_missing_sequence(self):
        self.assertFalse(eu.is_valid_input(None, {"GGGG"}, self.usage))

    def test_empty_sequence(self):
        self.assertFalse(eu.is_valid_input("", {"GGGG"}, self.usage))

    def test_invalid_sequence(self):
        self.assertFalse(eu.is_valid_input("ATGN", {"GGGG"}, self.usage))

    def test_missing_patterns(self):
        self.assertFalse(eu.is_valid_input("ATGC", None, self.usage))

    def test_empty_patterns(self):
        self.assertFalse(eu.is_valid_input("ATGC", set(), self.usage))

    def test_invalid_patterns(self):
        self.assertFalse(eu.is_valid_input("ATGC", {"NNN"}, self.usage))

    def test_missing_codon_usage(self):
        self.assertFalse(eu.is_valid_input("ATGC", {"GGGG"}, None))

    def test_empty_codon_usage(self):
        self.assertFalse(eu.is_valid_input("ATGC", {"GGGG"}, {}))

    def test_invalid_codon_usage(self):
        bad = _full_codon_usage()
        bad.pop("ATG")
        bad["XXX"] = 0.5
        self.assertFalse(eu.is_valid_input("ATGC", {"GGGG"}, bad))


class TestIsValidCost(unittest.TestCase):
    def test_happy_path(self):
        self.assertTrue(eu.is_valid_cost(alpha=1.0, beta=2.0, w=100.0))

    def test_alpha_non_positive(self):
        self.assertFalse(eu.is_valid_cost(alpha=0, beta=2.0, w=100.0))

    def test_alpha_wrong_type(self):
        self.assertFalse(eu.is_valid_cost(alpha="x", beta=2.0, w=100.0))

    def test_beta_non_positive(self):
        self.assertFalse(eu.is_valid_cost(alpha=1.0, beta=-1, w=100.0))

    def test_beta_wrong_type(self):
        self.assertFalse(eu.is_valid_cost(alpha=1.0, beta=None, w=100.0))

    def test_w_non_positive(self):
        self.assertFalse(eu.is_valid_cost(alpha=1.0, beta=2.0, w=0))

    def test_w_wrong_type(self):
        self.assertFalse(eu.is_valid_cost(alpha=1.0, beta=2.0, w="x"))

    def test_alpha_must_be_less_than_beta(self):
        self.assertFalse(eu.is_valid_cost(alpha=5.0, beta=2.0, w=100.0))

    def test_w_must_be_much_greater_than_beta(self):
        # factor is 10 → 2 * 10 < 25 must hold; w=15 should fail.
        self.assertFalse(eu.is_valid_cost(alpha=1.0, beta=2.0, w=15.0))


class TestEliminateUnwantedPatterns(unittest.TestCase):
    """Smoke test: eliminate_unwanted_patterns populates the app_data
    globals via EliminationController under the hood.
    """

    def setUp(self):
        app_data.EliminationData.info = None
        app_data.EliminationData.cost_contribution = None
        app_data.EliminationData.cost_substitution = None
        app_data.EliminationData.min_cost = None
        app_data.OutputData.optimized_sequence = None
        bases = "ACGT"
        raw = {a + b + c: 0.5 for a in bases for b in bases for c in bases}
        from biosynth.utils.cost_utils import normalize_codon_usage
        app_data.CostData.codon_usage = normalize_codon_usage(raw)
        app_data.CostData.alpha = 1.0
        app_data.CostData.beta = 2.0
        app_data.CostData.w = 100.0
        app_data.CostData.optimized_codon = False

    def test_writes_app_data_for_eliminated_sequence(self):
        # Pattern is present in the sequence so the algorithm runs through to
        # completion and returns the full 5-tuple.
        eu.eliminate_unwanted_patterns("ATAGTAC", {"TAGTAC"}, [0] * 7)
        self.assertIsNotNone(app_data.OutputData.optimized_sequence)
        self.assertNotIn("TAGTAC", app_data.OutputData.optimized_sequence)
        self.assertIsNotNone(app_data.EliminationData.info)
        self.assertIsNotNone(app_data.EliminationData.min_cost)
        self.assertGreaterEqual(app_data.EliminationData.min_cost, 0.0)


class TestMarkNonEqualCodons(unittest.TestCase):
    def test_delegates_to_sequence_utils(self):
        idx, marked_in, marked_opt = eu.mark_non_equal_codons(
            "AAA", "AAT", [0, 0, 0]
        )
        # Differs at position 3 only.
        self.assertIn("[A]", marked_in)
        self.assertIn("[T]", marked_opt)
        self.assertTrue(idx)


class TestInitializeReport(unittest.TestCase):
    def test_returns_report_controller(self):
        # ReportController reads InputData / OutputData / EliminationData on
        # construction, so we populate just enough for it to build cleanly.
        app_data.InputData.cleaned_dna_sequence = "ATG"
        app_data.InputData.coding_indexes = None
        app_data.InputData.coding_positions = [0, 0, 0]
        app_data.InputData.unwanted_patterns = {"GGG"}
        app_data.OutputData.optimized_sequence = "ATG"
        app_data.EliminationData.cost_contribution = []
        app_data.EliminationData.cost_substitution = []
        app_data.EliminationData.min_cost = 0.0

        controller = eu.initialize_report()
        # Imported here to avoid a heavy import at module top.
        from biosynth.report.html_report_utils import ReportController
        self.assertIsInstance(controller, ReportController)


if __name__ == "__main__":
    unittest.main()

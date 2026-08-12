import unittest
from unittest.mock import patch

import numpy as np

from biosynth.utils.cost_utils import normalize_codon_usage, calculate_cost


class TestCalculateCost(unittest.TestCase):
    def setUp(self):
        # Mock data for testing
        self.target_sequence = "ATAATGCTTACGTAA"  # "NNN" for non-coding regions
        self.coding_positions = [0, 0, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                 3]  # Adjusted codon positions: 1, 2, 3 for each codon
        self.codon_usage = {
            # Tyrosine (TAC, TAT)
            "TAC": 0.2,
            "TAT": 0.8,  # dominant → cost 0

            # Valine (GTA, GTT)
            "GTA": 0.5,
            "GTT": 0.25,

            # Arginine (CGT, CGC)
            "CGT": 0.1,
            "CGC": 0.3,

            # Leucine (TTA, CTT)
            "TTA": 0.1,
            "CTT": 0.05,

            # Stop codons
            "TAG": 0.01,
            "TAA": 0.02,
        }

        self.codon_usage = normalize_codon_usage(self.codon_usage)

        self.alpha = 1.0
        self.beta = 2.0
        self.w = 5.0

        self.optimized_codon = True

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_non_coding_transition(self, MockAminoAcidConfig):
        MockAminoAcidConfig.is_transition.return_value = True
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 0, "", "G", self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, self.alpha)

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_non_coding_transversion(self, MockAminoAcidConfig):
        MockAminoAcidConfig.is_transition.return_value = False
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 0, "", "C", self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, self.beta)

    def test_no_substitution(self):
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 0, "", "A", self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, 0.0)

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_synonymous_substitution(self, MockAminoAcidConfig):
        MockAminoAcidConfig.get_last3.return_value = "CTT"  # Simulate the codon at the position
        MockAminoAcidConfig.get_last2.return_value = "CT"  # Partial codon setup (just for setup)
        MockAminoAcidConfig.encodes_same_amino_acid.return_value = True  # Indicate that it's a synonymous substitution
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 8, "CTT", "A",
                                 self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertAlmostEqual(cost, self.codon_usage["TTA"])

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_stop_codon_formation(self, MockAminoAcidConfig):
        MockAminoAcidConfig.get_last3.return_value = "ATG"  # Valid stop codon
        MockAminoAcidConfig.get_last2.return_value = "TG"  # Partial codon (just for setup)
        MockAminoAcidConfig.either_is_stop_codon.return_value = True  # This should confirm it's a stop codon
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 5, "ATG", "A",
                                 self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, float("inf"))

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_stop_codon_substitution(self, MockAminoAcidConfig):
        MockAminoAcidConfig.get_last3.return_value = "TAA"  # Valid stop codon
        MockAminoAcidConfig.get_last2.return_value = "TC"  # Partial codon (just for setup)
        MockAminoAcidConfig.either_is_stop_codon.return_value = True  # This should confirm it's a stop codon
        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 14, "TAC", "A",
                                 self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, float("inf"))

    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_non_synonymous_substitution(self, MockAminoAcidConfig):
        MockAminoAcidConfig.get_last3.return_value = "CGT"
        MockAminoAcidConfig.get_last2.return_value = "CG"
        MockAminoAcidConfig.encodes_same_amino_acid.return_value = False
        MockAminoAcidConfig.either_is_stop_codon.return_value = False
        MockAminoAcidConfig.edit_dist.return_value = 2

        _, cost = calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 8, "CGT", "A",
                                 self.alpha,
                                 self.beta, self.w, self.optimized_codon)
        self.assertEqual(cost, self.w + 2)

    def test_out_of_bounds_index(self):
        with self.assertRaises(IndexError):
            calculate_cost(self.target_sequence, self.coding_positions, self.codon_usage, 20, "", "A", self.alpha,
                           self.beta, self.w, self.optimized_codon)

    def test_invalid_codon_usage(self):
        invalid_codon_usage = {"TAC": -0.1}  # Invalid probability
        with self.assertRaises(ValueError):
            calculate_cost(self.target_sequence, self.coding_positions, invalid_codon_usage, 8, "", "A", self.alpha,
                           self.beta, self.w, self.optimized_codon)


    @patch("biosynth.utils.amino_acid_utils.AminoAcidConfig")
    def test_optimized_codon_flag_effect(self, MockAminoAcidConfig):
        # Setup a synonymous scenario where proposed == target
        MockAminoAcidConfig.get_last3.return_value = "CTT"
        MockAminoAcidConfig.get_last2.return_value = "CT"
        MockAminoAcidConfig.encodes_same_amino_acid.return_value = True
        MockAminoAcidConfig.either_is_stop_codon.return_value = False

        # Case 1: optimized_codon = True → should use codon usage (NOT zero)
        _, cost_true = calculate_cost(
            self.target_sequence,
            self.coding_positions,
            self.codon_usage,
            8,
            "CCT",
            "T",
            alpha=self.alpha,
            beta=self.beta,
            w=self.w,
            optimized_codon=True
        )

        # Case 2: optimized_codon = False → identical codon → cost = 0
        _, cost_false = calculate_cost(
            self.target_sequence,
            self.coding_positions,
            self.codon_usage,
            8,
            "CCT",
            "T",
            alpha=self.alpha,
            beta=self.beta,
            w=self.w,
            optimized_codon=False
        )

        self.assertNotEqual(cost_true, 0.0)
        self.assertEqual(cost_false, 0.0)


class TestNormalizeAndEdgeCases(unittest.TestCase):
    def test_normalize_codon_usage_empty_returns_empty(self):
        self.assertEqual(normalize_codon_usage({}), {})

    def test_normalize_codon_usage_none_returns_empty(self):
        self.assertEqual(normalize_codon_usage(None), {})

    def test_calculate_cost_unexpected_codon_pos_raises(self):
        # An out-of-range codon_pos (e.g. 99) shouldn't happen in normal use
        # but the function defensively raises ValueError.
        with self.assertRaises(ValueError):
            calculate_cost(
                target_sequence="ATG",
                coding_positions=[99, 0, 0],
                codon_usage={"ATG": 0.0},
                i=0, v="AT", sigma="G",
                alpha=1.0, beta=2.0, w=100.0,
                optimized_codon=False,
            )
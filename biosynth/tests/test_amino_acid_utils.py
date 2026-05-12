"""Tests for biosynth.utils.amino_acid_utils.

Existing util-style code is exercised indirectly by test_cost_utils and
test_elimination_utils; these tests pin down the explicit error paths and
small helpers that those don't cover.
"""

import unittest

from biosynth.utils.amino_acid_utils import (
    AminoAcidConfig,
    GeneticCodeTable,
    codon_to_amino_acid,
)


class TestAminoAcidConfig(unittest.TestCase):
    def test_get_last2_returns_last_two_bases(self):
        self.assertEqual(AminoAcidConfig.get_last2("CATG"), "TG")

    def test_get_last2_raises_when_too_short(self):
        with self.assertRaises(ValueError):
            AminoAcidConfig.get_last2("A")

    def test_get_last3_returns_last_three(self):
        self.assertEqual(AminoAcidConfig.get_last3("AATGCC", 4), "TGC")

    def test_get_last3_raises_when_i_too_small(self):
        with self.assertRaises(ValueError):
            AminoAcidConfig.get_last3("AATGCC", 1)

    def test_encodes_same_amino_acid_true(self):
        # Both 'TTT' and 'TTC' encode Phenylalanine.
        self.assertTrue(AminoAcidConfig.encodes_same_amino_acid("TTT", "TTC"))

    def test_encodes_same_amino_acid_false(self):
        self.assertFalse(AminoAcidConfig.encodes_same_amino_acid("TTT", "GGG"))

    def test_either_is_stop_codon(self):
        self.assertTrue(AminoAcidConfig.either_is_stop_codon("TAA", "TTT"))
        self.assertTrue(AminoAcidConfig.either_is_stop_codon("ATG", "TAG"))
        self.assertFalse(AminoAcidConfig.either_is_stop_codon("ATG", "TTT"))

    def test_is_start_codon(self):
        self.assertTrue(AminoAcidConfig.is_start_codon(-3))
        self.assertFalse(AminoAcidConfig.is_start_codon(3))
        self.assertFalse(AminoAcidConfig.is_start_codon(0))

    def test_is_transition(self):
        self.assertTrue(AminoAcidConfig.is_transition("A", "G"))
        self.assertTrue(AminoAcidConfig.is_transition("G", "A"))
        self.assertTrue(AminoAcidConfig.is_transition("C", "T"))
        self.assertTrue(AminoAcidConfig.is_transition("T", "C"))
        # Transversions
        self.assertFalse(AminoAcidConfig.is_transition("A", "T"))
        self.assertFalse(AminoAcidConfig.is_transition("A", "C"))

    def test_edit_dist_counts_mismatches(self):
        self.assertEqual(AminoAcidConfig.edit_dist("ATG", "ATG"), 0)
        self.assertEqual(AminoAcidConfig.edit_dist("ATG", "ATC"), 1)
        self.assertEqual(AminoAcidConfig.edit_dist("ATG", "GGG"), 2)
        self.assertEqual(AminoAcidConfig.edit_dist("ATG", "CCC"), 3)


class TestGeneticCodeTable(unittest.TestCase):
    def test_known_codons(self):
        self.assertEqual(GeneticCodeTable.lookup("ATG"), "M")
        self.assertEqual(GeneticCodeTable.lookup("TAA"), "*")
        self.assertEqual(GeneticCodeTable.lookup("TTT"), "F")

    def test_unknown_codon_returns_none(self):
        self.assertIsNone(GeneticCodeTable.lookup("XYZ"))

    def test_table_has_64_codons(self):
        self.assertEqual(len(codon_to_amino_acid), 64)


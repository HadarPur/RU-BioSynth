import unittest
from utils.elimination_utils import EliminationUtils


class TestEliminationUtils(unittest.TestCase):
    def setUp(self):
        self.elimination_utils = EliminationUtils()

    def test_cost_function(self):
        C = [{'A': 1, 'G': 2, 'T': 3, 'C': 4},
             {'A': 5, 'G': 6, 'T': 7, 'C': 8},
             {'A': 9, 'G': 10, 'T': 11, 'C': 12}]
        cost_func = self.elimination_utils.cost_function(C)
        self.assertEqual(cost_func(1, 'A'), 1)
        self.assertEqual(cost_func(2, 'G'), 6)
        self.assertEqual(cost_func(3, 'T'), 11)

    def test_get_suffixes(self):
        suffixes = self.elimination_utils.get_suffixes("ATGC")
        self.assertEqual(suffixes, ["ATGC", "TGC", "GC", "C", ""])

    def test_get_prefixes(self):
        prefixes = self.elimination_utils.get_prefixes({"ATG", "AGT", "A"})
        self.assertEqual(prefixes, {"", "A", "AT", "AG"})

    def test_has_suffix(self):
        P = {"AT", "GC"}
        self.assertFalse(self.elimination_utils.has_suffix("ATG", P))
        self.assertTrue(self.elimination_utils.has_suffix("GC", P))
        self.assertFalse(self.elimination_utils.has_suffix("AAA", P))

    def test_longest_suffix_in_set(self):
        arr = {"TGC", "AGC", "CGC"}
        self.assertEqual(self.elimination_utils.longest_suffix_in_set("ATGC", arr), "TGC")
        self.assertEqual(self.elimination_utils.longest_suffix_in_set("AGC", arr), "AGC")
        self.assertEqual(self.elimination_utils.longest_suffix_in_set("CGC", arr), "CGC")
        self.assertIsNone(self.elimination_utils.longest_suffix_in_set("AAA", arr))
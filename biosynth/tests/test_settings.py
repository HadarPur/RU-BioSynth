"""Smoke tests for the biosynth.settings.* example fixtures.

These modules are loaded by the DebugController and other example flows.
They mostly hold static data; testing them keeps the assertions trivial
but ensures the module-level dictionaries remain well-formed.
"""

import unittest

from biosynth.settings.codon_usage_settings import C
from biosynth.settings.pattern_settings import P
from biosynth.settings.sequence_settings import S


class TestSettingsFixtures(unittest.TestCase):
    def test_codon_usage_table_is_64_codons(self):
        self.assertIsInstance(C, dict)
        self.assertEqual(len(C), 64)
        for codon, freq in C.items():
            self.assertEqual(len(codon), 3)
            self.assertTrue(set(codon).issubset(set("ACGT")))
            self.assertIsInstance(freq, (int, float))
            self.assertGreaterEqual(freq, 0.0)

    def test_pattern_set_is_non_empty_strings(self):
        self.assertIsInstance(P, set)
        self.assertGreater(len(P), 0)
        for pattern in P:
            self.assertIsInstance(pattern, str)
            self.assertGreater(len(pattern), 0)

    def test_sequence_is_non_empty_string(self):
        self.assertIsInstance(S, str)
        self.assertGreater(len(S), 0)
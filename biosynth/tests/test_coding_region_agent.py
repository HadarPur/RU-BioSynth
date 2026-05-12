"""Tests for biosynth.agents.coding_region_agent."""

import unittest

from biosynth.agents.base import AgentError
from biosynth.agents.coding_region_agent import CodingRegionAgent
from biosynth.agents.messages import CodingRegionRequest


class TestCodingRegionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CodingRegionAgent()

    def test_name(self):
        self.assertEqual(self.agent.name, "coding-region")

    def test_no_marker_returns_all_zero_positions(self):
        result = self.agent.handle(CodingRegionRequest(dna_sequence="ATGCATGC"))
        self.assertEqual(result.cleaned_sequence, "ATGCATGC")
        self.assertIsNone(result.start_codon_index)
        self.assertEqual(result.coding_positions, [0] * 8)
        self.assertIsNone(result.coding_indexes)

    def test_full_coding_region_marker(self):
        # '*ATG' marks the start codon; the trailing TAA stop closes the
        # in-frame coding region. After cleaning the '*' is gone.
        result = self.agent.handle(
            CodingRegionRequest(dna_sequence="AAA*ATGCCCTAA")
        )
        self.assertEqual(result.cleaned_sequence, "AAAATGCCCTAA")
        self.assertEqual(result.start_codon_index, 3)
        self.assertEqual(result.coding_indexes, (3, 12))
        # Three non-coding leading bases, then 1/2/-3 for the start codon
        # marker followed by 1/2/3 phase tags for each subsequent codon.
        self.assertEqual(result.coding_positions[:3], [0, 0, 0])
        self.assertEqual(result.coding_positions[3:6], [1, 2, -3])

    def test_malformed_marker_raises_exit_3(self):
        with self.assertRaises(AgentError) as cm:
            self.agent.handle(CodingRegionRequest(dna_sequence="AA*CCCC"))
        self.assertEqual(cm.exception.code, 3)
        self.assertIn("Start codon", cm.exception.message)
"""Tests for biosynth.agents.preflight_agent."""

import unittest

from biosynth.agents.base import AgentError
from biosynth.agents.messages import PreflightRequest
from biosynth.agents.preflight_agent import PreflightAgent


class TestPreflightAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PreflightAgent()

    def test_name(self):
        self.assertEqual(self.agent.name, "preflight")

    def test_non_empty_sequence_passes(self):
        result = self.agent.handle(PreflightRequest(dna_sequence="ATGC"))
        self.assertEqual(result.dna_sequence, "ATGC")

    def test_none_sequence_raises_exit_3(self):
        with self.assertRaises(AgentError) as cm:
            self.agent.handle(PreflightRequest(dna_sequence=None))
        self.assertEqual(cm.exception.code, 3)
        self.assertIn("empty", cm.exception.message.lower())

    def test_empty_string_raises_exit_3(self):
        with self.assertRaises(AgentError) as cm:
            self.agent.handle(PreflightRequest(dna_sequence=""))
        self.assertEqual(cm.exception.code, 3)
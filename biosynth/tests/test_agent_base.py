"""Tests for biosynth.agents.base."""

import unittest

from biosynth.agents.base import Agent, AgentError


class TestAgentError(unittest.TestCase):
    def test_stores_code_and_message(self):
        err = AgentError(code=3, message="bad input")
        self.assertEqual(err.code, 3)
        self.assertEqual(err.message, "bad input")
        # Exception message preserved for str(err).
        self.assertEqual(str(err), "bad input")

    def test_is_an_exception(self):
        # Catchable as Exception so existing handler chains keep working.
        try:
            raise AgentError(code=2, message="nope")
        except Exception as caught:
            self.assertIsInstance(caught, AgentError)
            self.assertEqual(caught.code, 2)


class TestAgentABC(unittest.TestCase):
    def test_subclass_without_handle_cannot_instantiate(self):
        class Incomplete(Agent):
            name = "incomplete"

        with self.assertRaises(TypeError):
            Incomplete()  # missing abstract method

    def test_minimal_subclass_works(self):
        class Echo(Agent):
            name = "echo"

            def handle(self, request):
                return request

        a = Echo()
        self.assertEqual(a.name, "echo")
        self.assertEqual(a.handle({"x": 1}), {"x": 1})
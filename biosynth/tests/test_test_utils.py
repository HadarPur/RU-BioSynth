"""Tests for biosynth.utils.test_utils — the tabular unittest runner.

The runner is itself a test harness, so we drive it with synthetic test
cases and check that it tabulates pass / fail / error / skip outcomes.
"""

import io
import unittest

from biosynth.utils.test_utils import TableTestResult, TableTestRunner


def _build_suite():
    """Build a tiny TestSuite with a mix of outcomes."""

    class Sample(unittest.TestCase):
        def test_pass(self):
            self.assertTrue(True)

        def test_fail(self):
            self.assertEqual(1, 2)

        def test_error(self):
            raise RuntimeError("boom")

        @unittest.skip("not yet")
        def test_skip(self):
            pass

    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(Sample)


class TestTableTestRunner(unittest.TestCase):
    def test_runner_records_all_outcomes(self):
        runner = TableTestRunner(stream=io.StringIO(), verbosity=0)
        suite = _build_suite()
        result = runner.run(suite)
        self.assertIsInstance(result, TableTestResult)

        # One row per loaded test.
        statuses = {row[1] for row in result.rows}
        self.assertIn("PASS", statuses)
        self.assertIn("FAIL", statuses)
        self.assertIn("ERROR", statuses)
        self.assertIn("SKIPPED", statuses)
        # Skipped tests are counted in testsRun in unittest, so all four
        # cases of the synthetic suite are accounted for.
        self.assertEqual(result.testsRun, 4)
        self.assertEqual(len(result.rows), 4)


if __name__ == "__main__":
    unittest.main()

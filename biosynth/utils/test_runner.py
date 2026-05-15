import os
import time
import unittest
import sys
from tabulate import tabulate
from biosynth.utils.logger import Logger


# =========================
# RESULT COLLECTOR
# =========================
class TableTestResult(unittest.TextTestResult):
    """Collects unittest results with per-test timing for tabular reporting."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = []

    def startTest(self, test):
        """Record the test start timestamp before running the test."""
        super().startTest(test)
        test._start_time = time.time()

    def stopTest(self, test):
        """Compute and store the test duration after it finishes."""
        super().stopTest(test)
        test._duration = time.time() - test._start_time

    def addSuccess(self, test):
        """Append a PASS row with the test's measured duration."""
        super().addSuccess(test)
        self.rows.append((
            test,
            "PASS",
            "",
            getattr(test, "_duration", 0.0)
        ))

    def addFailure(self, test, err):
        """Append a FAIL row including the formatted exception details."""
        super().addFailure(test, err)
        self.rows.append((
            test,
            "FAIL",
            self._exc_info_to_string(err, test),
            getattr(test, "_duration", 0.0)
        ))

    def addError(self, test, err):
        """Append an ERROR row including the formatted exception details."""
        super().addError(test, err)
        self.rows.append((
            test,
            "ERROR",
            self._exc_info_to_string(err, test),
            getattr(test, "_duration", 0.0)
        ))

    def addSkip(self, test, reason):
        """Append a SKIPPED row with the provided skip reason."""
        super().addSkip(test, reason)
        self.rows.append((
            test,
            "SKIPPED",
            reason,
            0.0
        ))


# =========================
# RUNNER
# =========================
class TableTestRunner(unittest.TextTestRunner):
    """unittest runner that prints results and a summary as formatted tables."""

    resultclass = TableTestResult

    def _format_test_name(self, test):
        test_id = test.id()
        parts = test_id.split(".")
        return parts[-2], parts[-1]  # class, method

    def run(self, test):
        """Run the test suite and print a results table followed by a summary table."""
        result = super().run(test)

        # =========================
        # MAIN RESULTS TABLE
        # =========================
        table_rows = []

        for test_obj, status, details, duration in result.rows:
            cls, method = self._format_test_name(test_obj)

            short_details = ""
            if details:
                short_details = details.split("\n")[-1]  # last line only

            table_rows.append([
                cls,
                method,
                status,
                f"{duration:.4f}s",
                short_details
            ])

        Logger.space()
        Logger.info("===================================================================")
        Logger.info("========================= UNITEST RESULTS =========================")
        Logger.info("===================================================================")
        Logger.space()

        print(tabulate(
            table_rows,
            headers=["Class", "Test", "Status", "Time", "Details"],
            tablefmt="simple",
            colalign=("left", "left", "center", "left", "left")
        ))

        # =========================
        # SUMMARY TABLE
        # =========================
        summary = [
            ["Tests run", result.testsRun],
            ["Failures", len(result.failures)],
            ["Errors", len(result.errors)],
            ["Skipped", len(result.skipped)],
            ["Success", result.wasSuccessful()],
        ]

        Logger.space()
        Logger.info("===================================================================")
        Logger.info("========================= UNITEST SUMMARY =========================")
        Logger.info("===================================================================")
        Logger.space()

        Logger.info(tabulate(
            summary,
            headers=["Metric", "Value"],
            tablefmt="fancy_grid",
            colalign=("left", "left")
        ))
        Logger.space()

        return result
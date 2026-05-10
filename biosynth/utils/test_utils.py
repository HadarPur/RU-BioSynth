import os
import time
import unittest
import sys
from tabulate import tabulate
from biosynth.utils.output_utils import Logger


# =========================
# RESULT COLLECTOR
# =========================
class TableTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = []

    def startTest(self, test):
        super().startTest(test)
        test._start_time = time.time()

    def stopTest(self, test):
        super().stopTest(test)
        test._duration = time.time() - test._start_time

    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append((
            test,
            "PASS",
            "",
            getattr(test, "_duration", 0.0)
        ))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.rows.append((
            test,
            "FAIL",
            self._exc_info_to_string(err, test),
            getattr(test, "_duration", 0.0)
        ))

    def addError(self, test, err):
        super().addError(test, err)
        self.rows.append((
            test,
            "ERROR",
            self._exc_info_to_string(err, test),
            getattr(test, "_duration", 0.0)
        ))

    def addSkip(self, test, reason):
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
    resultclass = TableTestResult

    def _format_test_name(self, test):
        test_id = test.id()
        parts = test_id.split(".")
        return parts[-2], parts[-1]  # class, method

    def run(self, test):
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

        Logger.debug("\nUNIT TEST RESULTS")

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

        Logger.debug("\nSUMMARY")
        Logger.info(tabulate(
            summary,
            headers=["Metric", "Value"],
            tablefmt="fancy_grid",
            colalign=("left", "left")
        ))
        Logger.space()

        return result
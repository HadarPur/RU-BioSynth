import os
import time
import unittest
import sys

class TableTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append((test, "PASS", ""))  # ← store test object

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.rows.append((test, "FAIL", self._exc_info_to_string(err, test)))

    def addError(self, test, err):
        super().addError(test, err)
        self.rows.append((test, "ERROR", self._exc_info_to_string(err, test)))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.rows.append((test, "SKIPPED", reason))

class TableTestRunner(unittest.TextTestRunner):
    resultclass = TableTestResult

    def _format_test_name(self, test):
        test_id = test.id()  # now this works
        parts = test_id.split(".")
        return parts[-2], parts[-1]  # class, method

    def _truncate(self, text, max_len):
        return text if len(text) <= max_len else text[:max_len - 3] + "..."

    def run(self, test):
        result = super().run(test)

        cls_w = 28
        method_w = 60
        status_w = 10

        print("\n" + "="*110)
        print(f"{'CLASS':<{cls_w}} {'TEST':<{method_w}} {'STATUS':<{status_w}} DETAILS")
        print("-"*110)

        for test_obj, status, details in result.rows:
            cls, method = self._format_test_name(test_obj)

            cls = self._truncate(cls, cls_w)
            method = self._truncate(method, method_w)
            short_details = details.split("\n")[0] if details else ""

            print(f"{cls:<{cls_w}} {method:<{method_w}} {status:<{status_w}} {short_details}")

        print("="*110)

        return result
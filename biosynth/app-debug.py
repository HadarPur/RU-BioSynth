import os
import time
import unittest
import sys

from biosynth.executions.controllers.debug_controller import DebugController
from biosynth.utils.file_utils import delete_dir
from biosynth.utils.output_utils import Logger
from biosynth.utils.text_utils import OutputFormat, set_output_format

def execute_unittests():
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), "tests")
    suite = loader.discover(start_dir)

    print(f"\n{'='*60}")
    print(f"Running {suite.countTestCases()} tests...")
    print(f"{'='*60}\n")

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print(f"\n{'='*60}")
    print(f"Tests run:    {result.testsRun}")
    print(f"Failures:     {len(result.failures)}")
    print(f"Errors:       {len(result.errors)}")
    print(f"Skipped:      {len(result.skipped)}")
    print(f"Success:      {result.wasSuccessful()}")
    print(f"{'='*60}\n")

    if result.errors:
        print("ERRORS:")
        for test, err in result.errors:
            print(f"  {test}: {err}")

if __name__ == "__main__":
    try:
        delete_dir('output')

        # DEBUG
        set_output_format(OutputFormat.TEST)
        execute_unittests()

        time.sleep(2.2)

        set_output_format(OutputFormat.TERMINAL)
        DebugController.execute()

    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")
        sys.exit(4)

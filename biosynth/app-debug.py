import os
import time
import unittest
import sys
from tabulate import tabulate

from biosynth.executions.controllers.debug_controller import DebugController
from biosynth.utils.file_utils import delete_dir
from biosynth.utils.output_utils import Logger
from biosynth.utils.text_utils import OutputFormat, set_output_format

from biosynth.utils.test_utils import TableTestRunner

def execute_unittests():
    """Discover and run all unit tests under the ``tests`` directory using TableTestRunner."""
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), "tests")
    suite = loader.discover(start_dir)

    runner = TableTestRunner(verbosity=0, stream=sys.stdout)
    runner.run(suite)

if __name__ == "__main__":
    try:
        delete_dir('output')

        execute_unittests()

        time.sleep(2.2)

        set_output_format(OutputFormat.TERMINAL)
        DebugController.execute()

    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")
        sys.exit(4)

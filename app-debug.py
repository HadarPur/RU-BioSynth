import time
import unittest

from executions.controllers.debug_controller import DebugController
from utils.file_utils import delete_dir
from utils.output_utils import Logger
from utils.text_utils import OutputFormat, set_output_format


def execute_unittests():
    loader = unittest.TestLoader()
    start_dir = 'test/'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    try:
        delete_dir('output')

        # DEBUG
        execute_unittests()
        time.sleep(0.2)
        set_output_format(OutputFormat.TERMINAL)
        DebugController().execute()

    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")

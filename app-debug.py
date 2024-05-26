import time
import unittest

from executions.console.ide_execution import App
from utils.file_utils import delete_dir
from utils.text_utils import OutputFormat, set_output_format


def execute_unittests():
    loader = unittest.TestLoader()
    start_dir = 'test/'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    try:
        delete_dir('report_output')

        # DEBUG
        execute_unittests()
        time.sleep(0.2)
        set_output_format(OutputFormat.TERMINAL)
        App().execute()

    except KeyboardInterrupt:
        print("\nProgram stopped by the user.")
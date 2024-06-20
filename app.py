import sys
import unittest

from executions.console.terminal_execution import Terminal
from utils.file_utils import delete_dir
from utils.text_utils import OutputFormat, set_output_format
from utils.output_utils import Logger


def execute_unittests():
    loader = unittest.TestLoader()
    start_dir = 'test/'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    try:
        delete_dir('output')

        set_output_format(OutputFormat.TERMINAL)
        Terminal(sys.argv[1:]).execute()

    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")

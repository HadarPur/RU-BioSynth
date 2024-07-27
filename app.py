import sys
import unittest

from executions.console.terminal_execution import Terminal
from executions.ui.gui_execution import GUI
from utils.file_utils import delete_dir
from utils.input_utils import ArgumentParser
from utils.output_utils import Logger
from utils.text_utils import OutputFormat, set_output_format

if __name__ == "__main__":
    try:
        delete_dir('output')

        parser = ArgumentParser()
        gui, _, _, _ = parser.parse_args(sys.argv[1:])
        if gui:
            set_output_format(OutputFormat.GUI)
            GUI().execute()
        else:
            set_output_format(OutputFormat.TERMINAL)
            Terminal(sys.argv[1:]).execute()

    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")

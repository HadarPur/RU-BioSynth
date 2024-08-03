import sys

from executions.controllers.terminal_controller import TerminalController
from executions.controllers.ui_controller import UIController
from utils.file_utils import delete_dir
from utils.input_utils import ArgumentParser
from utils.output_utils import Logger
from utils.text_utils import OutputFormat, set_output_format


class BioBliss:
    @staticmethod
    def execute(args):
        try:
            delete_dir('output')

            parser = ArgumentParser()
            gui, _, _, _ = parser.parse_args(args)
            if gui:
                set_output_format(OutputFormat.GUI)
                UIController().execute()
            else:
                set_output_format(OutputFormat.TERMINAL)
                TerminalController(args).execute()

        except KeyboardInterrupt:
            Logger.error("\nProgram stopped by the user.")


if __name__ == "__main__":
    BioBliss.execute(sys.argv[1:])


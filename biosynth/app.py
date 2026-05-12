import sys
from biosynth.executions.controllers.cli_controller import CLIController
from biosynth.executions.controllers.gui_controller import GUIController
from biosynth.utils.file_utils import delete_dir
from biosynth.utils.argument_parser import ArgumentParser
from biosynth.utils.logger import Logger
from biosynth.utils.text_utils import OutputFormat, set_output_format


class BioSynthApp:
    @staticmethod
    def execute(args):
        try:
            delete_dir('output')

            parser = ArgumentParser()
            gui, _, _, _, _, _, _, _, _ = parser.parse_args(args)

            if gui:
                set_output_format(OutputFormat.GUI)
                GUIController().execute()
            else:
                set_output_format(OutputFormat.TERMINAL)
                CLIController(args).execute()
        except Exception as e:
            Logger.error(e)
            sys.exit(5)
        except KeyboardInterrupt:
            Logger.error("\nProgram stopped by the user.")
            sys.exit(4)

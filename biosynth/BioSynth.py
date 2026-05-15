import sys
from biosynth.executions.controllers.cli_controller import CLIController
from biosynth.executions.controllers.gui_controller import GUIController
from biosynth.utils.file_utils import delete_dir
from biosynth.utils.input_utils import ArgumentParser
from biosynth.utils.output_utils import Logger
from biosynth.utils.text_utils import OutputFormat, set_output_format


class BioSynthApp:
    """Application entry point that dispatches to the CLI or GUI controller."""

    @staticmethod
    def execute(args):
        """Parse arguments and run BioSynth in either GUI or CLI mode.

        Clears the output directory, parses CLI args to detect GUI mode, sets
        the global output format accordingly, and delegates to the matching
        controller. Logs errors and exits with a non-zero code on failure or
        user interrupt.
        """
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

from executions.ui.gui_execution import GUI
from utils.file_utils import delete_dir
from utils.text_utils import OutputFormat, set_output_format
from utils.output_utils import Logger

if __name__ == "__main__":
    try:
        delete_dir('output')

        set_output_format(OutputFormat.GUI)
        GUI().execute()
    except KeyboardInterrupt:
        Logger.error("\nProgram stopped by the user.")

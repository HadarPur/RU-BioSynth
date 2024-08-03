from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from utils.file_utils import SequenceReader, PatternReader
from utils.input_utils import ArgumentParser


class TerminalController:
    def __init__(self, argv):
        self.argv = argv
        self.seq = None
        self.unwanted_patterns = None

    def execute(self):
        parser = ArgumentParser()

        _, s_path, p_path, o_path = parser.parse_args(self.argv)

        self.seq = SequenceReader(s_path).read_sequence()
        self.unwanted_patterns = PatternReader(p_path).read_patterns()

        if is_valid_input(self.seq, self.unwanted_patterns):
            CommandController(self.seq, self.unwanted_patterns, o_path).run()

        return

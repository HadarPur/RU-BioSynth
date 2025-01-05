from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from utils.file_utils import SequenceReader, PatternReader, CodonUsageReader
from utils.input_utils import ArgumentParser


class TerminalController:
    def __init__(self, argv):
        self.argv = argv
        self.seq = None
        self.unwanted_patterns = None
        self.codon_usage_table = None

    def execute(self):
        parser = ArgumentParser()

        _, s_path, p_path, c_path, o_path = parser.parse_args(self.argv)

        self.seq = SequenceReader(s_path).read_sequence()
        self.unwanted_patterns = PatternReader(p_path).read_patterns()
        self.codon_usage_table = CodonUsageReader(c_path).read_codon_usage()

        if is_valid_input(self.seq, self.unwanted_patterns, self.codon_usage_table):
            CommandController(self.seq, self.unwanted_patterns, self.codon_usage_table, o_path).run()

        return

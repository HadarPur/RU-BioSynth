from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from utils.file_utils import SequenceReader, PatternReader, CodonUsageReader
from utils.input_utils import ArgumentParser
from executions.controllers.app_data import AppData


class TerminalController:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = ArgumentParser()

        _, s_path, p_path, c_path, o_path = parser.parse_args(self.argv)

        seq = SequenceReader(s_path).read_sequence()
        unwanted_patterns = PatternReader(p_path).read_patterns()
        codon_usage_table = CodonUsageReader(c_path).read_codon_usage()

        if is_valid_input(seq, unwanted_patterns, codon_usage_table):
            AppData.dna_sequence = seq
            AppData.patterns = unwanted_patterns
            AppData.codon_usage = codon_usage_table
            AppData.download_location = o_path

            controller = CommandController()
            controller.run()

        return

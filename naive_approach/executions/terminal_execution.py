from naive_approach.utils.file_utils import SequenceReader, PatternReader, CostReader
from naive_approach.executions.shared_execution import Shared
from naive_approach.utils.input_utils import CommandLineParser


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = CommandLineParser()

        s_file_path, p_file_path, c_file_path = parser.handle_initial_input_params(self.argv)
        seq = SequenceReader(s_file_path).read_sequence()
        unwanted_patterns = PatternReader(p_file_path).read_patterns()
        cost_table = CostReader(c_file_path).read_costs()

        Shared(seq, unwanted_patterns, cost_table).run()
        return


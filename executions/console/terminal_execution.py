from utils.file_utils import SequenceReader, PatternReader
from executions.console.console_execution import Console
from utils.input_utils import CommandLineParser


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = CommandLineParser()

        s_file_path, p_file_path = parser.parse_args(self.argv)
        seq = SequenceReader(s_file_path).read_sequence()
        unwanted_patterns = PatternReader(p_file_path).read_patterns()

        Console(seq, unwanted_patterns).run()
        return


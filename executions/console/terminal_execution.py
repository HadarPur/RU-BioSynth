from utils.file_utils import SequenceReader, PatternReader
from executions.console.shared_execution import Shared
from utils.input_utils import CommandLineParser
from executions.execution_utils import is_valid_dna, is_valid_patterns

class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = CommandLineParser()

        s_file_path, p_file_path = parser.parse_args(self.argv)
        seq = SequenceReader(s_file_path).read_sequence()
        unwanted_patterns = PatternReader(p_file_path).read_patterns()

        if seq is None:
            print("There is an issue with the sequence file, please check and try again later.")
            return

        if not is_valid_dna(seq):
            print(f"The sequence:\n{seq}\n\nis not valid, please check and try again later.")
            return

        if unwanted_patterns is None or len(unwanted_patterns) == 0:
            print("There is an issue with the patterns file, please check and try again later.")
            return

        if not is_valid_patterns(unwanted_patterns):
            print(f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
            return

        Shared(seq, unwanted_patterns).run()
        return


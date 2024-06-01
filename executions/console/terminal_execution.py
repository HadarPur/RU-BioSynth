from executions.console.shared_execution import Shared
from executions.execution_utils import is_valid_dna, is_valid_patterns
from utils.file_utils import SequenceReader, PatternReader
from utils.input_utils import CommandLineParser


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = CommandLineParser()

        s_path, p_path, o_path = parser.parse_args(self.argv)
        seq = SequenceReader(s_path).read_sequence()
        unwanted_patterns = PatternReader(p_path).read_patterns()

        if seq is None:
            print("\033[91mUnfortunately, we couldn't find any sequence file. Please insert one and try again.\033[0m")
            return

        if len(seq) == 0:
            print("\033[91mUnfortunately, the sequence file is empty. Please insert fully one and try again.\033[0m")
            return

        if not is_valid_dna(seq):
            print(f"\033[91mThe sequence:\n{seq}\n\nis not valid, please check and try again later.\033[0m")
            return

        if unwanted_patterns is None:
            print("\033[91mUnfortunately, we couldn't find any patterns file. Please insert one and try again.\033[0m")
            return

        if len(seq) == 0:
            print("\033[91mUnfortunately, the patterns file is empty. Please insert fully one and try again.\033[0m")
            return

        if not is_valid_patterns(unwanted_patterns):
            print(f"\033[91mThe patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.\033[0m")
            return

        Shared(seq, unwanted_patterns, o_path).run()
        return

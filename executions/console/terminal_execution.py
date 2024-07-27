from executions.console.shared_execution import Shared
from executions.execution_utils import is_valid_dna, is_valid_patterns
from utils.file_utils import SequenceReader, PatternReader
from utils.input_utils import ArgumentParser
from utils.output_utils import Logger


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = ArgumentParser()

        _, s_path, p_path, o_path = parser.parse_args(self.argv)
        seq = SequenceReader(s_path).read_sequence()
        unwanted_patterns = PatternReader(p_path).read_patterns()

        if seq is None:
            Logger.error("Unfortunately, we couldn't find any sequence file. Please insert one and try again.")
            return

        if len(seq) == 0:
            Logger.error("Unfortunately, the sequence file is empty. Please insert fully one and try again.")
            return

        if not is_valid_dna(seq):
            Logger.error(f"The sequence:\n{seq}\n\nis not valid, please check and try again later.")
            return

        if unwanted_patterns is None:
            Logger.error("Unfortunately, we couldn't find any patterns file. Please insert one and try again.")
            return

        if len(seq) == 0:
            Logger.error("Unfortunately, the patterns file is empty. Please insert fully one and try again.")
            return

        if not is_valid_patterns(unwanted_patterns):
            Logger.error(f"The patterns:\n{unwanted_patterns}\n\nare not valid, please check and try again later.")
            return

        Shared(seq, unwanted_patterns, o_path).run()
        return

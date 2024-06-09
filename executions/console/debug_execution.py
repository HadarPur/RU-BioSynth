from executions.console.shared_execution import Shared
from executions.execution_utils import is_valid_dna, is_valid_patterns
from settings.pattern_settings import P
from settings.sequence_settings import S


class Debug:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P

    def execute(self):
        if self.seq is None:
            print("There is an issue with the sequence file, please check and try again later.")
            return

        if not is_valid_dna(self.seq):
            print(f"The sequence:\n{self.seq}\n\nis not valid, please check and try again later.")
            return

        if self.unwanted_patterns  is None or len(self.unwanted_patterns ) == 0:
            print("There is an issue with the patterns file, please check and try again later.")
            return

        if not is_valid_patterns(self.unwanted_patterns ):
            print(f"The patterns:\n{self.unwanted_patterns }\n\nare not valid, please check and try again later.")
            return

        Shared(self.seq, self.unwanted_patterns, '/Users/hadar.pur/Downloads').run()
        return

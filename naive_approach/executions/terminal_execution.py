from naive_approach.utils.file_utils import SequenceReader, PatternReader, CostReader
from naive_approach.executions.shared_execution import Shared
from naive_approach.utils.input_utils import CommandLineParser
from naive_approach.utils.dna_utils import CodonScorer
from naive_approach.settings.costs_settings import C


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        parser = CommandLineParser()

        s_file_path, p_file_path = parser.parse_args(self.argv)
        seq = SequenceReader(s_file_path).read_sequence()
        unwanted_patterns = PatternReader(p_file_path).read_patterns()

        scorer = CodonScorer(C)
        scores = scorer.calculate_scores(seq)
        cost_table = scores

        Shared(seq, unwanted_patterns, cost_table).run()
        return


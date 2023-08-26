from naive_approach.executions.shared_execution import Shared
from naive_approach.settings.sequence_settings import S
from naive_approach.settings.pattern_settings import P
from naive_approach.settings.costs_settings import C

from naive_approach.utils.dna_utils import CodonScorer


class App:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P

        scorer = CodonScorer(C)
        scores = scorer.calculate_scores(self.seq)
        self.cost_table = scores

    def execute(self):
        Shared(self.seq, self.unwanted_patterns, self.cost_table).run()
        return

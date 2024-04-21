from executions.console.shared_execution import Shared
from settings.pattern_settings import P
from settings.sequence_settings import S


class App:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P

    def execute(self):
        Shared(self.seq, self.unwanted_patterns).run()
        return

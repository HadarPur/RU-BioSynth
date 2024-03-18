from executions.console.console_execution import Console
from settings.sequence_settings import S
from settings.pattern_settings import P


class App:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P

    def execute(self):
        Console(self.seq, self.unwanted_patterns).run()
        return

from executions.shared_execution import *
from settings.app_settings import S, P, C


class App:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P
        self.cost_table = C

    def execute(self):
        Shared(self.seq, self.unwanted_patterns, self.cost_table).run()
        return

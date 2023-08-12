from naive_approach.executions.shared_execution import *
# from naive_approach.settings.app_settings import S, P, C
from naive_approach.settings.naive_settings import S, P, C


class App:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P
        self.cost_table = C

    def execute(self):
        print(type(self.unwanted_patterns))
        Shared(self.seq, self.unwanted_patterns, self.cost_table).run()
        return

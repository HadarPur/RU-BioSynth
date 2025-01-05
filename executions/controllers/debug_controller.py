from pathlib import Path

from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from settings.pattern_settings import P
from settings.sequence_settings import S
from settings.codon_usage_settings import C


class DebugController:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P
        self.codon_usage_table = C

    def execute(self):
        if is_valid_input(self.seq, self.unwanted_patterns, self.codon_usage_table):
            CommandController(self.seq, self.unwanted_patterns, self.codon_usage_table, Path.home() / 'Downloads').run()
        return

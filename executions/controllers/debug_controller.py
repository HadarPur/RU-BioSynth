from pathlib import Path

from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from settings.pattern_settings import P
from settings.sequence_settings import S


class DebugController:
    def __init__(self):
        self.seq = S
        self.unwanted_patterns = P

    def execute(self):
        if is_valid_input(self.seq, self.unwanted_patterns):
            CommandController(self.seq, self.unwanted_patterns, Path.home() / 'Downloads').run()
        return

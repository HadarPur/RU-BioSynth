from pathlib import Path

from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from settings.pattern_settings import P
from settings.sequence_settings import S
from settings.codon_usage_settings import C
from executions.controllers.app_data import AppData


class DebugController:
    @staticmethod
    def execute():
        if is_valid_input(S, P, C):
            AppData.dna_sequence = S
            AppData.patterns = P
            AppData.codon_usage = C
            AppData.download_location = Path.home() / 'Downloads'

            controller = CommandController()
            controller.run()

            return

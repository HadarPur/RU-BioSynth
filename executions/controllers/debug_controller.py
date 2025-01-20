
from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from settings.pattern_settings import P
from settings.sequence_settings import S
from settings.codon_usage_settings import C
from data.app_data import InputData, CostData, OutputData


class DebugController:
    @staticmethod
    def execute():
        if is_valid_input(S, P, C):
            InputData.dna_sequence = S
            InputData.patterns = P

            CostData.codon_usage = C

            controller = CommandController()
            controller.run()

            return

from data.app_data import InputData, CostData
from executions.controllers.command_controller import CommandController
from executions.execution_utils import is_valid_input
from settings.codon_usage_settings import C
from settings.pattern_settings import P
from settings.sequence_settings import S


class DebugController:
    @staticmethod
    def execute():
        if is_valid_input(S, P, C, alpha=2, beta=4, w=140):
            InputData.dna_sequence = S
            InputData.unwanted_patterns = P
            CostData.codon_usage = C
            CostData.alpha = 2
            CostData.beta = 4
            CostData.w = 140

            controller = CommandController()
            controller.run()

            return

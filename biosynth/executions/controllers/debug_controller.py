from biosynth.data.app_data import InputData, CostData
from biosynth.executions.controllers.command_controller import CommandController
from biosynth.executions.controllers.gui_controller import GUIController
from biosynth.executions.execution_utils import is_valid_input, is_valid_cost
from biosynth.settings.codon_usage_settings import C
from biosynth.settings.pattern_settings import P
from biosynth.settings.sequence_settings import S
from biosynth.utils.logger import Logger

class DebugController:
    """Development-only controller that runs the pipeline twice using hardcoded debug settings."""

    @staticmethod
    def execute():
        """Run the elimination pipeline with the bundled debug inputs.

        Loads the hardcoded sequence, patterns, and codon-usage from
        ``biosynth.settings``, validates them along with fixed cost
        parameters (alpha=1.02, beta=1.98, w=99.96), populates the shared
        ``InputData``/``CostData`` state, and then invokes
        ``CommandController.run`` twice - once with ``optimized_codon=False``
        and once with ``optimized_codon=True`` - to compare both modes.
        Returns early without running if any validation step fails.
        """
        if not is_valid_input(S, P, C):
            return

        InputData.dna_sequence = S
        InputData.unwanted_patterns = P
        CostData.codon_usage = C

        alpha = 1.02
        beta = 1.98
        w = 99.96

        if not is_valid_cost(alpha=alpha, beta=beta, w=w):
            return

        CostData.alpha = alpha
        CostData.beta = beta
        CostData.w = w

        Logger.critical("Starting DebugController execution with optimized_codon = False ...")
        CostData.optimized_codon = False
        controller = CommandController()
        controller.run()

        Logger.critical("Starting DebugController execution with optimized_codon = True ...")
        CostData.optimized_codon = True
        controller = CommandController()
        controller.run()

        return

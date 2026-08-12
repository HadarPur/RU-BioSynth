import sys
from biosynth.data.app_data import InputData, CostData, OutputData
from biosynth.executions.controllers.command_controller import CommandController
from biosynth.executions.execution_utils import is_valid_input, is_valid_cost
from biosynth.utils.file_utils import SequenceReader, PatternReader, CodonUsageReader
from biosynth.utils.input_utils import ArgumentParser
from biosynth.utils.cost_utils import normalize_codon_usage
from biosynth.utils.logger import Logger


class CLIController:
    """Command-line entry controller that loads inputs from disk and runs the elimination pipeline."""

    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        """Drive the full CLI run end to end.

        Parses CLI arguments, reads the sequence/patterns/codon-usage files,
        validates inputs and cost parameters, populates the shared
        ``InputData``/``CostData``/``OutputData`` state (including optional
        overrides for alpha/beta/w, optimized codon flag, and output path),
        and finally delegates execution to ``CommandController``. Exits with
        code 2 on validation failure.
        """
        parser = ArgumentParser()

        _, s_path, p_path, c_path, o_path, alpha, beta, w, optimized_codon = parser.parse_args(self.argv)

        seq = SequenceReader(s_path).read_sequence()
        unwanted_patterns = PatternReader(p_path).read_patterns()
        codon_usage_table = CodonUsageReader(c_path).read_codon_usage()
        codon_usage_file_name = CodonUsageReader(c_path).get_filename()

        if not is_valid_input(seq, unwanted_patterns, codon_usage_table):
            sys.exit(2)

        InputData.dna_sequence = seq
        InputData.unwanted_patterns = unwanted_patterns
        CostData.codon_usage = normalize_codon_usage(codon_usage_table)
        CostData.codon_usage_filename = codon_usage_file_name

        # optional values
        if alpha is not None:
            CostData.alpha = alpha

        if beta is not None:
            CostData.beta = beta

        if w is not None:
            CostData.w = w

        if not is_valid_cost(CostData.alpha, CostData.beta, CostData.w):
            sys.exit(2)

        if optimized_codon is not None:
            CostData.optimized_codon = optimized_codon

        if o_path is not None:
            OutputData.output_path = o_path

        controller = CommandController()
        controller.run()

        return

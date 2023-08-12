from naive_approach.utils.file_utils import *
from naive_approach.executions.shared_execution import *


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def execute(self):
        s_file_path, p_file_path, c_file_path = handle_initial_input_params(self.argv)
        seq = read_seq_from_file(s_file_path)
        unwanted_patterns = read_patterns_from_file(p_file_path)
        cost_table = read_costs_from_file(c_file_path)

        Shared(seq, unwanted_patterns, cost_table).run()
        return


from utils.input_utils import *
from utils.file_utils import *
from utils.dna_utils import *


class Terminal:
    def __init__(self, argv):
        self.argv = argv

    def run(self):
        s_file_path, p_file_path = handle_initial_input_params(self.argv)
        seq = read_seq_from_file(s_file_path)
        # patterns = read_seq_from_file(p_file_path)

        # Print the coding regions and their translations
        print(f"DNA sequence:\n{seq}\n")

        patterns = ""
        coding_regions = get_coding_region(seq)

        highlighted_sequence = highlight_coding_regions(seq, coding_regions)
        print(f"Highlighted conding regions for the above DNA sequence:\n{highlighted_sequence}\n")

        elimination_response = handle_elimination_input_response()

        if elimination_response is False:
            coding_regions_response = handle_elimination_coding_regions_input(coding_regions)
            print(coding_regions_response)

        return

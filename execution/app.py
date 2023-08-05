from utils.input_utils import *
from utils.dna_utils import *


class App:
    def __init__(self):
        self.seq = "ATGTTAGTAGTGAAGCGAATGTAAATGACCTAGTAGCCCTAGTGA"

    def run(self):
        # Print the coding regions and their translations
        print(f"DNA sequence:\n{self.seq}\n")

        patterns = ""
        coding_regions = get_coding_region(self.seq)

        highlighted_sequence = highlight_coding_regions(self.seq, coding_regions)
        print(f"Highlighted conding regions for the above DNA sequence:\n{highlighted_sequence}\n")

        elimination_response = handle_elimination_input_response()

        if elimination_response is False:
            coding_regions_response = handle_elimination_coding_regions_input(coding_regions)
            print(coding_regions_response)

        return

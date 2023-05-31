from input_utils import *
from file_utils import *
from dna_utils import *


def terminal(argv):
    s_file_path, p_file_path = handle_input_params(argv)
    seq = read_seq_from_file(s_file_path)
    # patterns = read_seq_from_file(p_file_path)

    coding_regions = get_coding_region(seq)

    # Print the coding regions and their translations
    print(f"DNA sequence:\n{seq}\n")
    for i, region in enumerate(coding_regions):
        print(f"Coding region {i + 1}:\n{region}\nTranslation:\n{region.translate()}\n")

    return


def gui():
    return


# for development testing
def app():
    seq = "ATGTTAGTAGTGAAGCGAATGTAAATGACCTAGTAGCCCTAGTGA"

    patterns = ""
    coding_regions = get_coding_region(seq)

    # Print the coding regions and their translations
    print(f"DNA sequence:\n{seq}\n")
    for i, region in enumerate(coding_regions):
        print(f"Coding region {i + 1}:\n{region}\nTranslation:\n{region.translate()}\n")

    return


if __name__ == "__main__":
    # app()
    terminal(sys.argv[1:])
    # gui()


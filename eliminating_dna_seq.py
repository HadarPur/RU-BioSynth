from input_utils import *
from file_utils import *
from dna_utils import *


def terminal(argv):
    s_file_path, p_file_path = handle_initial_input_params(argv)
    seq = read_seq_from_file(s_file_path)
    # patterns = read_seq_from_file(p_file_path)

    # Print the coding regions and their translations
    print(f"DNA sequence:\n{seq}\n")

    patterns = ""
    coding_regions = get_coding_region(seq)

    highlighted_sequence = highlight_coding_regions(seq, coding_regions)
    print(f"Highlighted conding regions for the above DNA sequence:\n{highlighted_sequence}\n")

    elimination_response = get_elimination_response_from_user()

    if elimination_response is False:
        coding_regions_response = get_elimination_coding_regions_from_user(coding_regions)
        print(coding_regions_response)

    return


def gui():
    return


# for development testing
def app():
    seq = "ATGTTAGTAGTGAAGCGAATGTAAATGACCTAGTAGCCCTAGTGA"

    # Print the coding regions and their translations
    print(f"DNA sequence:\n{seq}\n")

    patterns = ""
    coding_regions = get_coding_region(seq)

    highlighted_sequence = highlight_coding_regions(seq, coding_regions)
    print(f"Highlighted conding regions for the above DNA sequence:\n{highlighted_sequence}\n")

    elimination_response = get_elimination_response_from_user()

    if elimination_response is False:
        coding_regions_response = get_elimination_coding_regions_from_user(coding_regions)
        print(coding_regions_response)

    return


def main():
    if __name__ == "__main__":
        app()
    else:
        terminal(sys.argv[1:])


if __name__ == "__main__":
    main()
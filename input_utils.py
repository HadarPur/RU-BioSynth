import getopt
import sys


def handle_input_params(argv):
    p_file_path = None
    s_file_path = None

    try:
        opts, args = getopt.getopt(argv, "hp:s:r:c:t", ["p_file=", "s_file="])
    except getopt.GetoptError:
        print("Error while getting elimination arguments")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("-p <patterns_file> -s <sequence_file>")
            sys.exit()
        elif opt in ("-s", "--s_file"):
            s_file_path = arg
        elif opt in ("-p", "--p_file"):
            p_file_path = arg

    if s_file_path is None:
        print("The sequence file is none ")
        sys.exit()
    if p_file_path is None:
        print("The pattern file is none ")
        sys.exit()

    return s_file_path, p_file_path

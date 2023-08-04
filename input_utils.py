import getopt
import sys


def handle_initial_input_params(argv):
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
    # if p_file_path is None:
    #     print("The pattern file is none ")
    #     sys.exit()

    return s_file_path, p_file_path


def get_elimination_response_from_user():
    while True:
        response = input("Would you like to proceed with all of the code sections? (yes/no/exit): ")

        if response.lower() == "yes":
            return True
        elif response.lower() == "no":
            return False
        elif response.lower() == "exit":
            print("Program terminated.")
            exit(1)
        else:
            print("Invalid input. Please enter 'yes', 'no', or 'exit'.")


def get_elimination_coding_regions_from_user(coding_regions):
    print("Please choose the areas you wish to exclude: ")
    for i, region in enumerate(coding_regions):
        print(f"[{i + 1}]: {region}")

    response = input("Your response should be with the appropriate format ('1,2,3', ... or '1 2 3 ...'): ")

    # Remove spaces and split response into segments
    response_segments = response.replace(" ", "").split(",")

    # Validate segments as digits and within valid range
    valid_indices = set(str(i) for i in range(1, len(coding_regions) + 1))
    if all(segment in valid_indices for segment in response_segments):
        selected_regions = [coding_regions[int(segment) - 1] for segment in response_segments]
        print("Selected regions:", selected_regions)
    else:
        print("Invalid input. Please provide valid indices separated by commas or spaces.")


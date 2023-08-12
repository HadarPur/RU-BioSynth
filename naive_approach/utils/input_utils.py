import getopt
import sys
import re


class CommandLineParser:
    def __init__(self):
        self.p_file_path = None
        self.s_file_path = None
        self.c_file_path = None

    def parse_args(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hp:s:r:c:t", ["p_file=", "s_file=", "c_file="])
        except getopt.GetoptError:
            print("\033[91mError while getting elimination arguments.\033[0m")
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print("-p <patterns_file> -s <sequence_file> -c <cost>")
                sys.exit()
            elif opt in ("-s", "--s_file"):
                self.s_file_path = arg
            elif opt in ("-p", "--p_file"):
                self.p_file_path = arg
            elif opt in ("-c", "--c_file"):
                self.c_file_path = arg

        if self.s_file_path is None or self.p_file_path is None or self.c_file_path is None:
            print("\033[91mOne or more input files are missing.\033[0m")
            sys.exit()

        return self.s_file_path, self.p_file_path, self.c_file_path


class UserInputHandler:
    @staticmethod
    def handle_elimination_input_response():
        while True:
            response = input("Would you like to proceed with all of the code sections? (yes/no/exit): ")
            response = response.strip()

            if response.lower() == "yes":
                return True
            elif response.lower() == "no":
                return False
            elif response.lower() == "exit":
                print("Program terminated.")
                exit(1)
            else:
                print("\033[91mInvalid input. Please enter 'yes', 'no', or 'exit'.\033[0m")

    @staticmethod
    def handle_elimination_coding_regions_input(coding_regions):
        print("Please choose the areas you wish to exclude: ")
        for i, region in enumerate(coding_regions):
            print(f"[{i + 1}]: {region}")

        while True:
            response = input("Your response should be with the appropriate format ('1,2,3', ... or '1 2 3 ...'): ")

            if response.lower() == "exit":
                print("Program terminated.")
                exit(1)

            response = response.strip()
            segments = re.split(r"[,\s]\s*", response)
            segments = list(filter(None, segments))

            valid_indices = all(item.isdigit() for item in segments)
            if valid_indices:
                segments = list(dict.fromkeys(segments))
                if len(segments) > len(coding_regions) or \
                        min(int(item) for item in segments) <= 0 or \
                        max(int(item) for item in segments) > len(coding_regions):
                    print("\033[91mInvalid selection. Please try again.\033[0m")
                else:
                    selected_regions = [coding_regions[int(segment) - 1] for segment in segments]
                    print("Selected regions:", selected_regions)
                    return selected_regions
            else:
                print("\033[91mInvalid input. Please provide valid indices separated by commas or spaces.\033[0m")

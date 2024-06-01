import getopt
import re
import sys

from utils.text_utils import format_text_bold_for_output


class CommandLineParser:
    def __init__(self):
        """
        Initializes a CommandLineParser object with attributes for storing file paths.
        """
        self.p_path = None
        self.s_path = None
        self.o_path = None

    def parse_args(self, argv):
        """
        Parses command-line arguments and extracts file paths from them.

        Parameters:
            argv (list): List of command-line arguments.

        Returns:
            tuple: A tuple containing the paths to the patterns file and sequence file.
        """
        try:
            opts, args = getopt.getopt(argv, "hp:s:r:c:t", ["help", "p_file=", "s_file="])
        except getopt.GetoptError as err:
            print("\033[91mError:", err, "\033[0m")
            self.print_usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.print_usage()
                sys.exit()
            elif opt in ("-s", "--s_path"):
                self.s_path = arg
            elif opt in ("-p", "--p_path"):
                self.p_path = arg
            elif opt in ("-o", "--o_path"):
                self.o_path = arg

        return self.s_path, self.p_path, self.o_path

    def print_usage(self):
        print(
            f"{format_text_bold_for_output('Usage:')}\n"
            "\t$ python ./app.py -s <seq_file_path> -p <pattern_file_path> -o <output_path_dir>\n\n"
            "\tThe elimination program, which allow design synthetic DNA sequences without unwanted patterns.\n\n"
            f"{format_text_bold_for_output('Options:')}\n"
            "\t-s --s_path\tSequence file path (mandatory)\n"
            "\t-p --p_path\tPatterns file path (mandatory)\n"
            "\t-o --o_path\tOutput directory path (optional-default is downloads directory)\n\n"
            f"{format_text_bold_for_output('Info:')}\n"
        )


class UserInputHandler:
    @staticmethod
    def handle_elimination_input():
        """
        Handles user input for proceeding with code elimination.

        Returns:
            bool: True if the user wants to proceed, False if not.
        """
        while True:
            response = input("Would you like to proceed with all of the code sections? (yes/no/exit): ")
            response = response.strip()

            if response.lower() == "yes" or response.lower() == "y":
                return True
            elif response.lower() == "no" or response.lower() == "n":
                return False
            elif response.lower() == "exit" or response.lower() == "e":
                print("Program terminated.")
                exit(1)
            else:
                print("\033[91mInvalid input. Please enter 'yes', 'no', or 'exit'.\033[0m")

    @staticmethod
    def handle_elimination_coding_regions_input(coding_regions):
        """
        Handles user input for choosing coding regions to exclude.

        Parameters:
            coding_regions (list): List of coding regions to choose from.

        Returns:
            list: List of selected coding regions.
        """
        print("Please choose the areas you wish to exclude: ")
        original_coding_regions = UserInputHandler.get_coding_regions_list(coding_regions)
        print('\n'.join(f"[{key}] {value}" for key, value in original_coding_regions.items()))

        while True:
            response = input("\nYour response should be with the appropriate format ('1,2,3', ... or '1 2 3 ...'): ")

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
                    print("\nSelected regions to exclude:")
                    selected_regions = {}
                    selected_regions_to_exclude = {}
                    for segment in segments:
                        coding_region = coding_regions[int(segment) - 1]
                        selected_regions_to_exclude[f'{int(segment)}'] = coding_region
                        print(f"[{int(segment)}] {coding_region}")
                        selected_regions[int(segment) - 1] = coding_region
                    print("\nThese coding regions will be classified as non-coding areas.")
                    return original_coding_regions, selected_regions_to_exclude, selected_regions
            else:
                print("\033[91mInvalid input. Please provide valid indices separated by commas or spaces.\033[0m")

    @staticmethod
    def get_coding_regions_list(coding_regions):
        original_coding_regions = {}
        for i, region in enumerate(coding_regions):
            original_coding_regions[f'{i + 1}'] = region
        return original_coding_regions

    @staticmethod
    def handle_saving_input_response():
        """
        Handles user input for deciding whether to save the target sequence to a file.

        Returns:
            bool: True if the user chooses to save, False if not.
        """
        while True:
            response = input("\nWould you like to save the target sequence to a file? (yes/no/exit): ")
            response = response.strip()

            if response.lower() == "yes" or response.lower() == "y":
                return True
            elif response.lower() == "no" or response.lower() == "n" or response.lower() == "exit" or response.lower() == "e":
                print("Program terminated.\n")
                exit(1)
                return False
            else:
                print("\033[91mInvalid input. Please enter 'yes', 'no', or 'exit'.\033[0m")

    @staticmethod
    def save_sequence_to_file(sequence):
        """
        Saves a sequence to a file specified by the user.

        Parameters:
            sequence (str): The sequence to save.

        Returns:
            None
        """

        while True:
            file_path = input("\nPlease provide the file path for saving: ")

            if file_path.lower() == "exit" or file_path.lower() == "e":
                print("Program terminated.")
                exit(1)

            try:
                file_path += "/results.txt"
                with open(file_path, 'w') as file:
                    file.write(sequence)
                print(f"Sequence saved to {file_path}\n")
                break
            except OSError:
                print("\033[91mError: Unable to save the sequence to the specified file path. Please try again.\033[0m")

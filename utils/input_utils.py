import getopt
import sys

from utils.output_utils import Logger
from utils.text_utils import format_text_bold_for_output
from utils.text_utils import set_output_format, OutputFormat


def get_terminal_usage():
    return f"\n{format_text_bold_for_output('Usage:')}\n" \
           "\t$ python ./BioSynth.py -s <seq_file_path> -p <pattern_file_path> -o <output_path_dir> -c <codon_usage_file> [-g] [-a <alpha>] [-b <beta>] [-w <w>]\n\n" \
           "\tThis application is designed for the elimination of unwanted patterns from synthetic DNA sequences.\n\n" \
           f"{format_text_bold_for_output('Options:')}\n" \
           "\t-g --gui\tOption to run the program via user interface. If using this option, there is no need to specify any -s, -p, or -o options.\n" \
           "\t-s --s_path\tSpecifies the sequence file path (mandatory)\n" \
           "\t-p --p_path\tSpecifies the unwanted patterns file path (mandatory)\n" \
           "\t-c --c_path\tSpecifies the codon usage table file path (mandatory). This parameter allows the program to prioritize codon usage based on the provided table.\n\n" \
           "\t-o --o_path\tSpecifies the output directory path (optional - default is the downloads directory)\n" \
           "\t-a --alpha\tSpecifies the value for transition substitution cost (optional - default is 1.0)\n" \
           "\t-b --beta\tSpecifies the value for transversion substitution cost (optional - default is 2.0)\n" \
           "\t-w --w\t\tSpecifies the value for non-synonymous substitution cost (optional - default is 100.0)\n\n" \
           f"{format_text_bold_for_output('Info:')}\n" \
           "\tThe elimination program via terminal is designed to run automatically without any user intervention.\n" \
           "\tPlease note the following rules enforced by the program:\n" \
           "\t - Minimum Codon Length: Each coding region must contain at least 5 internal codons " \
           "(excluding start and stop codons). This ensures only substantial ORFs are analyzed.\n" \
           "\t - Overlap Resolution Strategy:\n" \
           "\t\t • Fully overlapping ORFs – the first valid ORF is retained; the rest are discarded.\n" \
           "\t\t • Partially overlapping ORFs – considered ambiguous; the program halts execution with an error message.\n"

class ArgumentParser:
    def __init__(self):
        self.gui = False

        self.s_path = None
        self.p_path = None
        self.c_path = None
        self.o_path = None
        self.alpha = None
        self.beta = None
        self.w = None

    def parse_args(self, argv):
        """
        Parses command-line arguments and extracts file paths from them.

        Parameters:
            argv (list): List of command-line arguments.

        Returns:
            tuple: A tuple containing the paths to the patterns file and sequence file, and a flag for GUI.
        """
        try:
            opts, args = getopt.getopt(argv, "hs:p:c:o:ga:b:w:",
                                       ["help", "s_path=", "p_path=", "c_path=", "o_path=", "gui", "alpha=", "beta=",
                                        "w="])
        except getopt.GetoptError as err:
            set_output_format(OutputFormat.TERMINAL)
            Logger.error(err)
            Logger.info(get_terminal_usage())
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                set_output_format(OutputFormat.TERMINAL)
                Logger.info(get_terminal_usage())
                sys.exit(1)
            elif opt in ("-g", "--gui"):
                self.gui = True
                break
            elif opt in ("-s", "--s_path"):
                self.s_path = arg
            elif opt in ("-p", "--p_path"):
                self.p_path = arg
            elif opt in ("-c", "--c_path"):
                self.c_path = arg
            elif opt in ("-a", "--alpha"):
                self.alpha = float(arg)  # Ensure alpha is treated as a float
            elif opt in ("-b", "--beta"):
                self.beta = float(arg)  # Ensure beta is treated as a float
            elif opt in ("-w", "--w"):
                self.w = float(arg)  # Ensure w is treated as a float
            elif opt in ("-o", "--o_path"):
                self.o_path = arg

        return self.gui, self.s_path, self.p_path, self.c_path, self.o_path, self.alpha, self.beta, self.w

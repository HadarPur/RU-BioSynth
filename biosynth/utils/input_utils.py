import argparse
import sys

from biosynth.utils.logger import Logger
from biosynth.utils.text_utils import format_text_bold_for_output
from biosynth.utils.text_utils import set_output_format, OutputFormat
from biosynth.utils.descriptions import get_info_usage, get_elimination_info

try:
    from importlib.metadata import version as package_version
    VERSION = package_version("biosynth-tool")
except ImportError:
    VERSION = "1.0.0-local"
except Exception:
    VERSION = "1.0.0-local"


def get_terminal_information():
    """Return the bolded usage and elimination information block for terminal display."""
    return f"{format_text_bold_for_output('Information:')}\n" \
           f"{get_info_usage()}\n\n" \
           f"{get_elimination_info()}"


class CompactHelpFormatter(argparse.HelpFormatter):
    """Shows metavar only once, next to the long option. No line wrapping."""
    def __init__(self, prog):
        super().__init__(prog, width=200, max_help_position=40)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        option_string = ", ".join(action.option_strings)
        return option_string.ljust(30) + args_string

    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(usage, actions, groups, "Usage:\n  ")


class ArgumentParser:
    """Command-line argument parser for the BioSynth elimination tool."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="biosynth",
            description="\n  This application is designed for the elimination of unwanted patterns from synthetic DNA sequences.\n",
            formatter_class=CompactHelpFormatter,
            add_help=False,
        )
        self.parser._optionals.title = "Options"
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            "-h", "--help",
            action="store_true",
            default=False,
            help="Show this help message and exit."
        )
        self.parser.add_argument(
            "-v", "--version",
            action="store_true",
            default=False,
            help="Show the program version and exit."
        )
        self.parser.add_argument(
            "-g", "--gui",
            action="store_true",
            default=False,
            help="Run the program via user interface. If using this option, there is no need to specify -s, -p, or -o."
        )
        self.parser.add_argument(
            "-s", "--target_sequence",
            metavar="PATH",
            default=None,
            help="Specifies the sequence file path (mandatory)."
        )
        self.parser.add_argument(
            "-p", "--unwanted_patterns",
            metavar="PATH",
            default=None,
            help="Specifies the unwanted patterns file path (mandatory)."
        )
        self.parser.add_argument(
            "-c", "--codon_usage",
            metavar="PATH",
            default=None,
            help="Specifies the codon usage table file path (mandatory)."
        )
        self.parser.add_argument(
            "-o", "--out_dir",
            metavar="PATH",
            default=None,
            help="Specifies the output directory path (optional - default is the downloads directory)."
        )
        self.parser.add_argument(
            "-a", "--alpha",
            metavar="FLOAT",
            type=float,
            default=None,
            help="Specifies the value for transition substitution cost (optional - default is 1.0)."
        )
        self.parser.add_argument(
            "-b", "--beta",
            metavar="FLOAT",
            type=float,
            default=None,
            help="Specifies the value for transversion substitution cost (optional - default is 2.0)."
        )
        self.parser.add_argument(
            "-w", "--non_synonymous_w",
            metavar="FLOAT",
            type=float,
            default=None,
            help="Specifies the value for non-synonymous substitution cost (optional - default is 100.0)."
        )
        self.parser.add_argument(
            "-oc", "--optimized_codon",
            metavar="BOOL",
            default=None,
            help="Enable/Disable codon optimization based on codon usage (optional - default is true)."
        )

    def parse_args(self, argv):
        """
        Parses command-line arguments and extracts file paths from them.

        Parameters:
            argv (list): List of command-line arguments.

        Returns:
            tuple: A tuple containing the paths to the patterns file and sequence file, and a flag for GUI.
        """
        try:
            args = self.parser.parse_args(argv)
        except SystemExit:
            set_output_format(OutputFormat.TERMINAL)
            Logger.error(
                "The specified argument is not valid. "
                "For assistance, please use the help option '--help' or '-h' to review the accepted parameters."
            )
            sys.exit(2)

        if args.help:
            set_output_format(OutputFormat.TERMINAL)
            Logger.help(self.parser.format_help())
            Logger.help(get_terminal_information())
            sys.exit(1)

        if args.version:
            set_output_format(OutputFormat.TERMINAL)
            Logger.info(f"BioSynth version {VERSION}")
            sys.exit(0)

        # Parse optimized_codon string -> bool
        optimized_codon = None
        if args.optimized_codon is not None:
            if args.optimized_codon.strip().lower() in ("false", "0", "no"):
                optimized_codon = False
            elif args.optimized_codon.strip().lower() in ("true", "1", "yes"):
                optimized_codon = True

        return (
            args.gui,
            args.target_sequence,
            args.unwanted_patterns,
            args.codon_usage,
            args.out_dir,
            args.alpha,
            args.beta,
            args.non_synonymous_w,
            optimized_codon,
        )
from enum import Enum


class OutputFormat(Enum):
    NONE = 0
    TERMINAL = 1
    GUI = 2


output_format = OutputFormat.NONE


def set_output_format(o_format):
    global output_format
    try:
        output_format = o_format
    except KeyError:
        print("Invalid output format. Supported formats: 'none', 'terminal', and 'html'.")


def format_text_bold_for_output(text):
    if output_format == OutputFormat.TERMINAL:
        return f"\033[1m{text}\033[0m"
    elif output_format == OutputFormat.GUI:
        return f"<b>{text}</b>"
    else:
        raise ValueError("Invalid output format. Supported formats: 'terminal' and 'html'.")

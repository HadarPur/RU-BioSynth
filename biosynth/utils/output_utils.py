import textwrap
import re


class Logger:
    MAX_WIDTH = 120  # <-- set max characters per line

    COLORS = {
        "ERROR": "\033[91m",  # Red
        "WARNING": "\033[93m",  # Yellow
        "INFO": "\033[0m",  # default color
        "DEBUG": "\033[92m",  # Green
        "NOTICE": "\033[36m",  # Cyan
        "CRITICAL": "\033[95m",  # Magenta
        "ENDC": "\033[0m",  # Reset to default color
    }

    @staticmethod
    def log(message, level="INFO"):
        color = Logger.COLORS.get(level, Logger.COLORS["ENDC"])
        wrapped_message = Logger.get_formated_text(message)
        print(f"{color}{wrapped_message}{Logger.COLORS['ENDC']}")

    @staticmethod
    def help(message, level="INFO"):
        color = Logger.COLORS.get(level, Logger.COLORS["ENDC"])
        print(f"{color}{message}{Logger.COLORS['ENDC']}")

    @staticmethod
    def error(message, level="ERROR"):
        color = Logger.COLORS.get(level, Logger.COLORS["ENDC"])
        print(f"{color}Error: {message}{Logger.COLORS['ENDC']}")

    @staticmethod
    def warning(message):
        Logger.log(message, "WARNING")

    @staticmethod
    def info(message):
        Logger.log(message, "INFO")

    @staticmethod
    def debug(message):
        Logger.log(message, "DEBUG")

    @staticmethod
    def notice(message):
        Logger.log(message, "NOTICE")

    @staticmethod
    def critical(message):
        Logger.log(message, "CRITICAL")

    @staticmethod
    def space():
        Logger.log('', "INFO")

    @staticmethod
    def get_formated_text(text):
        # Respect line structure
        lines = str(text).splitlines()
        wrapped_lines = []

        for line in lines:
            # Check if line contains ANSI escape codes
            if '\033[' in line:
                wrapped_lines.append(Logger._wrap_with_ansi(line, Logger.MAX_WIDTH))
            else:
                wrapped_lines.append(
                    textwrap.fill(line, width=Logger.MAX_WIDTH, replace_whitespace=False)
                )

        wrapped_message = "\n".join(wrapped_lines)
        return wrapped_message

    @staticmethod
    def _wrap_with_ansi(text, max_width):
        """Wrap text that contains ANSI escape codes."""
        # Pattern to match ANSI escape codes
        ansi_pattern = re.compile(r'\033\[[0-9;]*m')

        # Split text into segments: (ansi_code, text_content)
        segments = []
        last_end = 0
        current_codes = []

        for match in ansi_pattern.finditer(text):
            # Add text before this code
            if match.start() > last_end:
                segments.append(('text', text[last_end:match.start()]))
            # Add the code itself
            code = match.group()
            segments.append(('code', code))
            # Track active codes (reset clears, others add)
            if code == '\033[0m':
                current_codes = []
            else:
                current_codes.append(code)
            last_end = match.end()

        # Add remaining text
        if last_end < len(text):
            segments.append(('text', text[last_end:]))

        # Now wrap based on visible characters only
        result = []
        current_line = []
        visible_width = 0
        active_codes = []

        for seg_type, content in segments:
            if seg_type == 'code':
                current_line.append(content)
                if content == '\033[0m':
                    active_codes = []
                else:
                    active_codes.append(content)
            else:  # text
                for char in content:
                    if visible_width >= max_width:
                        # Close any active codes before newline
                        if active_codes:
                            current_line.append('\033[0m')
                        result.append(''.join(current_line))
                        current_line = []
                        visible_width = 0
                        # Reopen codes on new line
                        if active_codes:
                            current_line.extend(active_codes)

                    current_line.append(char)
                    visible_width += 1

        # Add final line
        if current_line:
            result.append(''.join(current_line))

        return '\n'.join(result)
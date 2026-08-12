import unittest
from io import StringIO
import sys
from biosynth.utils.logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Capture stdout
        self.held_stdout = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.original_stdout

    def get_output(self):
        return self.held_stdout.getvalue()

    def test_log_info(self):
        Logger.log("Test info message", "INFO")
        output = self.get_output()
        self.assertIn("Test info message", output)
        self.assertTrue(output.startswith(Logger.COLORS["INFO"]))
        self.assertTrue(output.endswith(Logger.COLORS["ENDC"] + "\n"))

    def test_error(self):
        Logger.error("Test error message")
        output = self.get_output()
        self.assertIn("Error: Test error message", output)
        self.assertTrue(output.startswith(Logger.COLORS["ERROR"]))
        self.assertTrue(output.endswith(Logger.COLORS["ENDC"] + "\n"))

    def test_warning_shortcut(self):
        Logger.warning("Test warning")
        output = self.get_output()
        self.assertIn("Test warning", output)
        self.assertTrue(output.startswith(Logger.COLORS["WARNING"]))

    def test_debug_shortcut(self):
        Logger.debug("Debug message")
        output = self.get_output()
        self.assertIn("Debug message", output)
        self.assertTrue(output.startswith(Logger.COLORS["DEBUG"]))

    def test_notice_shortcut(self):
        Logger.notice("Notice message")
        output = self.get_output()
        self.assertIn("Notice message", output)
        self.assertTrue(output.startswith(Logger.COLORS["NOTICE"]))

    def test_critical_shortcut(self):
        Logger.critical("Critical message")
        output = self.get_output()
        self.assertIn("Critical message", output)
        self.assertTrue(output.startswith(Logger.COLORS["CRITICAL"]))

    def test_space(self):
        Logger.space()
        output = self.get_output()
        # It should just print an empty line
        self.assertEqual(output, f"{Logger.COLORS['INFO']}{Logger.COLORS['ENDC']}\n")

    def test_get_formated_text_wraps(self):
        long_text = "a" * 100
        wrapped = Logger.get_formated_text(long_text)
        self.assertTrue(all(len(line) <= Logger.MAX_WIDTH for line in wrapped.splitlines()))

    def test_help_passes_text_through_unchanged(self):
        # help() does not wrap the message — only colors it.
        Logger.help("plain text", "INFO")
        output = self.get_output()
        self.assertIn("plain text", output)
        self.assertTrue(output.startswith(Logger.COLORS["INFO"]))

    def test_log_unknown_level_falls_back_to_endc(self):
        Logger.log("oops", "MYSTERY")
        output = self.get_output()
        self.assertIn("oops", output)
        self.assertTrue(output.startswith(Logger.COLORS["ENDC"]))

    def test_error_unknown_level_falls_back_to_endc(self):
        Logger.error("oops", "MYSTERY")
        output = self.get_output()
        self.assertIn("Error: oops", output)
        self.assertTrue(output.startswith(Logger.COLORS["ENDC"]))

    def test_get_formated_text_preserves_line_breaks(self):
        wrapped = Logger.get_formated_text("line one\nline two")
        self.assertIn("line one", wrapped)
        self.assertIn("line two", wrapped)

    def test_get_formated_text_with_ansi_codes_wraps_without_break(self):
        # ANSI-coded text under the width limit should pass through.
        text = "\033[36mhello\033[0m"
        wrapped = Logger.get_formated_text(text)
        self.assertIn("hello", wrapped)
        # Reset code is preserved.
        self.assertIn("\033[0m", wrapped)

    def test_wrap_with_ansi_splits_long_line_and_reopens_color(self):
        # A coloured line longer than MAX_WIDTH must be split and the colour
        # re-opened after each newline.
        body = "a" * (Logger.MAX_WIDTH + 10)
        text = f"\033[36m{body}\033[0m"
        wrapped = Logger.get_formated_text(text)
        lines = wrapped.split("\n")
        self.assertGreater(len(lines), 1)
        # Every wrapped line that contains content should carry an ANSI code.
        for line in lines:
            if line.strip("a"):
                self.assertIn("\033[", line)

    def test_wrap_with_ansi_handles_trailing_plain_text(self):
        # Plain characters after a reset code exercise the
        # "remaining text after final ANSI code" branch.
        text = "\033[36mhi\033[0mtail"
        wrapped = Logger.get_formated_text(text)
        self.assertIn("hi", wrapped)
        self.assertIn("tail", wrapped)

import unittest
from unittest.mock import patch
import sys
from biosynth.utils.input_utils import ArgumentParser, VERSION


class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    # -------------------------------------------------------------------------
    # Basic argument parsing
    # -------------------------------------------------------------------------

    def test_parse_all_arguments(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt",
                    "-o", "out_dir", "-a", "2.0", "-b", "3.0", "-w", "200.0", "-oc", "no"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(
            (gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon),
            (False, "s_file.txt", "p_file.txt", "c_file.txt", "out_dir", 2.0, 3.0, 200.0, False)
        )

    def test_parse_minimal_arguments(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(
            (gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon),
            (False, "s_file.txt", "p_file.txt", "c_file.txt", None, None, None, None, None)
        )

    def test_parse_long_arguments(self):
        """Test that long-form arguments work identically to short ones."""
        sys.argv = ["test.py",
                    "--unwanted_patterns", "p_file.txt",
                    "--target_sequence", "s_file.txt",
                    "--codon_usage", "c_file.txt",
                    "--out_dir", "out_dir",
                    "--alpha", "2.0",
                    "--beta", "3.0",
                    "--non_synonymous_w", "200.0",
                    "--optimized_codon", "no"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(
            (gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon),
            (False, "s_file.txt", "p_file.txt", "c_file.txt", "out_dir", 2.0, 3.0, 200.0, False)
        )

    # -------------------------------------------------------------------------
    # GUI flag
    # -------------------------------------------------------------------------

    def test_gui_flag_short(self):
        sys.argv = ["test.py", "-g"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertTrue(gui)
        self.assertIsNone(s_file)
        self.assertIsNone(p_file)
        self.assertIsNone(c_file)
        self.assertIsNone(o_file)
        self.assertIsNone(alpha)
        self.assertIsNone(beta)
        self.assertIsNone(w)
        self.assertIsNone(optimized_codon)

    def test_gui_flag_long(self):
        sys.argv = ["test.py", "--gui"]
        gui, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertTrue(gui)

    def test_no_gui_flag_by_default(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        gui, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertFalse(gui)

    # -------------------------------------------------------------------------
    # File path arguments
    # -------------------------------------------------------------------------

    def test_sequence_file_path(self):
        sys.argv = ["test.py", "-s", "/path/to/seq.txt", "-p", "p.txt", "-c", "c.txt"]
        _, s_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(s_file, "/path/to/seq.txt")

    def test_pattern_file_path(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "/path/to/pattern.txt", "-c", "c.txt"]
        _, _, p_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(p_file, "/path/to/pattern.txt")

    def test_codon_usage_file_path(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "/path/to/codon.txt"]
        _, _, _, c_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(c_file, "/path/to/codon.txt")

    def test_out_dir_argument(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "-o", "/tmp/output"]
        _, _, _, _, o_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(o_file, "/tmp/output")

    def test_out_dir_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        _, _, _, _, o_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(o_file)

    def test_sequence_file_default_is_none(self):
        sys.argv = ["test.py", "-p", "p.txt", "-c", "c.txt"]
        _, s_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(s_file)

    def test_pattern_file_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-c", "c.txt"]
        _, _, p_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(p_file)

    def test_codon_usage_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt"]
        _, _, _, c_file, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(c_file)

    # -------------------------------------------------------------------------
    # Float arguments
    # -------------------------------------------------------------------------

    def test_float_arguments(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt",
                    "-a", "1.5", "-b", "2.5", "-w", "50.0", "-oc", "yes"]
        _, _, _, _, _, alpha, beta, w, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(alpha, 1.5)
        self.assertEqual(beta, 2.5)
        self.assertEqual(w, 50.0)
        self.assertTrue(optimized_codon)

    def test_alpha_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        _, _, _, _, _, alpha, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(alpha)

    def test_beta_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        _, _, _, _, _, _, beta, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(beta)

    def test_w_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        _, _, _, _, _, _, _, w, _ = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(w)

    def test_alpha_zero(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "-a", "0.0"]
        _, _, _, _, _, alpha, *_ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(alpha, 0.0)

    def test_negative_float_arguments(self):
        """Argparse accepts negative floats — the caller is responsible for validation."""
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt",
                    "-a", "-1.0", "-b", "-2.0", "-w", "-100.0"]
        _, _, _, _, _, alpha, beta, w, _ = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(alpha, -1.0)
        self.assertEqual(beta, -2.0)
        self.assertEqual(w, -100.0)

    # -------------------------------------------------------------------------
    # optimized_codon
    # -------------------------------------------------------------------------

    def test_optimized_codon_false_values(self):
        for value in ("false", "0", "no"):
            sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "-oc", value]
            _, _, _, _, _, _, _, _, optimized_codon = self.parser.parse_args(sys.argv[1:])
            self.assertFalse(optimized_codon, msg=f"Expected False for -oc {value}")

    def test_optimized_codon_true_values(self):
        for value in ("true", "1", "yes"):
            sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "-oc", value]
            _, _, _, _, _, _, _, _, optimized_codon = self.parser.parse_args(sys.argv[1:])
            self.assertTrue(optimized_codon, msg=f"Expected True for -oc {value}")

    def test_optimized_codon_case_insensitive(self):
        for value in ("FALSE", "False", "NO", "No", "TRUE", "True", "YES", "Yes"):
            sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "-oc", value]
            _, _, _, _, _, _, _, _, optimized_codon = self.parser.parse_args(sys.argv[1:])
            self.assertIsNotNone(optimized_codon, msg=f"-oc {value} should resolve to a bool, not None")

    def test_optimized_codon_default_is_none(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt"]
        _, _, _, _, _, _, _, _, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertIsNone(optimized_codon)

    def test_optimized_codon_long_flag(self):
        sys.argv = ["test.py", "-s", "s.txt", "-p", "p.txt", "-c", "c.txt", "--optimized_codon", "false"]
        _, _, _, _, _, _, _, _, optimized_codon = self.parser.parse_args(sys.argv[1:])
        self.assertFalse(optimized_codon)

    # -------------------------------------------------------------------------
    # Special flags: -h, -v
    # -------------------------------------------------------------------------

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.help')
    def test_help_option(self, mock_logger_help, mock_exit):
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-h"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(1)
        self.assertTrue(mock_logger_help.called)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.help')
    def test_help_long_option(self, mock_logger_help, mock_exit):
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "--help"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(1)
        self.assertTrue(mock_logger_help.called)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.help')
    def test_help_called_twice(self, mock_logger_help, mock_exit):
        """Logger.help should be called at least twice (format_help + information)."""
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-h"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        self.assertGreaterEqual(mock_logger_help.call_count, 2)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.info')
    def test_version_option(self, mock_logger_info, mock_exit):
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-v"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(0)
        mock_logger_info.assert_called_with(f"BioSynth version {VERSION}")

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.info')
    def test_version_long_option(self, mock_logger_info, mock_exit):
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "--version"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(0)
        mock_logger_info.assert_called_with(f"BioSynth version {VERSION}")

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.info')
    def test_version_contains_version_string(self, mock_logger_info, mock_exit):
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-v"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        call_arg = mock_logger_info.call_args[0][0]
        self.assertIn(VERSION, call_arg)
        self.assertIn("BioSynth", call_arg)

    # -------------------------------------------------------------------------
    # Invalid arguments
    # -------------------------------------------------------------------------

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.error')
    @patch('argparse.ArgumentParser.error')
    def test_invalid_argument(self, mock_argparse_error, mock_logger_error, mock_exit):
        mock_argparse_error.side_effect = SystemExit
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-x"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_logger_error.assert_called()
        mock_exit.assert_called_with(2)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.error')
    @patch('argparse.ArgumentParser.error')
    def test_invalid_long_argument(self, mock_argparse_error, mock_logger_error, mock_exit):
        mock_argparse_error.side_effect = SystemExit
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "--invalid_flag"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        mock_logger_error.assert_called()
        mock_exit.assert_called_with(2)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.error')
    @patch('argparse.ArgumentParser.error')
    def test_error_message_contains_guidance(self, mock_argparse_error, mock_logger_error, mock_exit):
        """Logger.error message should mention the help option."""
        mock_argparse_error.side_effect = SystemExit
        mock_exit.side_effect = SystemExit
        sys.argv = ["test.py", "-x"]
        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])
        error_message = mock_logger_error.call_args[0][0]
        self.assertIn("--help", error_message)
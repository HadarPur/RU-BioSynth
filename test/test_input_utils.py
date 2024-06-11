import sys
import unittest
from io import StringIO
from unittest.mock import patch

from utils.input_utils import CommandLineParser


class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandLineParser()

    def test_parse_args(self):
        # Simulate command-line arguments
        sys.argv = ["test.py", "-p", "files/mult_coding/p_file.txt", "-s", "files/mult_coding/s_file.txt"]

        # Check if parsing arguments works correctly
        self.assertEqual(self.parser.parse_args(sys.argv[1:]),
                         ("files/mult_coding/s_file.txt", "files/mult_coding/p_file.txt", None))

    @patch('sys.stderr', new_callable=StringIO)
    def assert_stderr(self, expected_output, mock_stderr):
        self.parser.parse_args(["invalid"])
        self.assertEqual(mock_stderr.getvalue().strip(), expected_output)
